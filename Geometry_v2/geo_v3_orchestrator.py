#!/usr/bin/env python3
"""
Manim Animation Orchestrator (v3 - Enhanced)

This enhanced orchestrator handles the complete pipeline with improvements:
1. Better error handling and recovery mechanisms
2. Enhanced parallel processing with progress tracking
3. Improved audio file handling and validation
4. More robust JSON parsing and validation
5. Better logging and debugging capabilities
6. Optimized memory usage and resource management
7. Enhanced code generation with better patching
8. Improved video rendering with quality options
9. Better cleanup and temporary file management
10. Configuration validation and setup verification
"""

import json
import os
import subprocess
import logging
import re
import time
import shutil
from pathlib import Path
import sys
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from dataclasses import dataclass
import hashlib
from threading import Lock
import tempfile
from PIL import Image
from openai import OpenAI

# --- Robustly add project root to Python path ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))
    from Geometry_v2.orchestrator_prompts import (
        Animator_Phase_1_Blueprint_Balanced, 
        Animator_Phase_2_Code_Generation_v2 as Animator_Phase_2_Code_Generation
    )
except ImportError:
    print("\n--- ERROR ---")
    print("Could not import prompts from 'Geometry_v2.orchestrator_prompts'.")
    print("Please ensure you have the latest prompt named 'Animator_Phase_2_Code_Generation_v2' in that file.")
    sys.exit(1)

# --- Basic Setup ---
try:
    import google.generativeai as genai
    from google.genai import types
except ImportError:
    print("Error: google-generativeai package not found. Please run 'pip install google-generativeai'.")
    sys.exit(1)

# Configure enhanced logging
def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup enhanced logging with file output option."""
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=handlers,
        force=True
    )

logger = logging.getLogger(__name__)
load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")

@dataclass
class RenderConfig:
    """Configuration for video rendering."""
    quality: str = "medium_quality"  # low_quality, medium_quality, high_quality, production_quality
    format: str = "mp4"
    frame_rate: int = 30
    resolution: str = "480p"  # 480p, 720p, 1080p, 1440p, 2160p
    timeout: int = 600  # seconds
    max_workers: int = 4

@dataclass
class SceneMetadata:
    """Metadata for tracking scene processing."""
    step_id: str
    index: int
    duration: float
    audio_file: Optional[str]
    status: str = "pending"  # pending, processing, completed, failed
    error: Optional[str] = None
    retry_count: int = 0

class ProgressTracker:
    """Thread-safe progress tracking."""
    def __init__(self, total_items: int):
        self.total_items = total_items
        self.completed_items = 0
        self.failed_items = 0
        self.lock = Lock()
    
    def update(self, completed: bool = True):
        with self.lock:
            if completed:
                self.completed_items += 1
            else:
                self.failed_items += 1
    
    def get_progress(self) -> Tuple[int, int, int]:
        with self.lock:
            return self.completed_items, self.failed_items, self.total_items

class ManimOrchestrator:
    """Enhanced orchestrator for creating Manim animations from structured data."""

    def __init__(self,
                 api_key: str,
                 input_file: str,
                 styler_file: str,
                 output_dir: str,
                 blueprint_dir: str,
                 manim_code_dir: str,
                 audio_dir: str,
                 temp_dir: str = "temp",
                 image_path: Optional[str] = None,
                 render_config: Optional[RenderConfig] = None,
                 log_file: Optional[str] = None):
        """Initialize the enhanced orchestrator."""
        
        # Setup logging first
        if log_file:
            setup_logging(log_file=log_file)
        
        # Validate and set paths
        self.api_key = api_key
        self.input_file = Path(input_file)
        self.styler_file = Path(styler_file)
        self.output_dir = Path(output_dir)
        self.blueprint_dir = Path(blueprint_dir)
        self.manim_code_dir = Path(manim_code_dir)
        self.audio_dir = Path(audio_dir)
        self.temp_dir = Path(temp_dir)
        self.image_path = image_path
        self.render_config = render_config or RenderConfig()
        
        # Validate required files exist
        self._validate_setup()
        
        # Configure OpenRouter API (Claude Sonnet 4)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        self.model = "anthropic/claude-sonnet-4"

        # Load prompts
        self.blueprint_prompt = Animator_Phase_1_Blueprint_Balanced
        self.code_generator_prompt = Animator_Phase_2_Code_Generation
        logger.info("Loaded prompts from 'orchestrator_prompts.py'.")
        
        # Load and validate style configuration
        self._load_style_config()
        
        # Initialize tracking
        self.scene_metadata: List[SceneMetadata] = []
        self.progress_tracker: Optional[ProgressTracker] = None
        self.api_call_times = []  # List of (step, duration)
        self.phase_times = {}     # Dict of {phase: duration}

    def _validate_setup(self):
        """Validate that all required files and directories can be accessed."""
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        
        if not self.styler_file.exists():
            raise FileNotFoundError(f"Styler file not found: {self.styler_file}")
        
        if not self.audio_dir.exists():
            logger.warning(f"Audio directory not found: {self.audio_dir}. Audio files will be skipped.")
        
        if self.image_path and not Path(self.image_path).exists():
            logger.warning(f"Image file not found: {self.image_path}. Image will be skipped.")
        
        # Test API key
        if not self.api_key:
            raise ValueError("API key is required but not provided.")
        
        logger.info("Setup validation completed successfully.")

    def _load_style_config(self):
        """Load and validate style configuration."""
        try:
            with open(self.styler_file, 'r', encoding='utf-8') as f:
                self.style_config = json.load(f)
            logger.info(f"Loaded style configuration from '{self.styler_file}'.")
            
            # Validate style config structure
            required_keys = ['colors', 'fonts', 'animations']
            for key in required_keys:
                if key not in self.style_config:
                    logger.warning(f"Style config missing recommended key: '{key}'")
                    
        except FileNotFoundError:
            logger.error(f"Error: Styler file not found at {self.styler_file}.")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error: Could not decode JSON from styler file {self.styler_file}: {e}")
            raise

    def run(self, cleanup: bool = True, max_retries: int = 2) -> str:
        """Run the complete orchestration pipeline with enhanced error handling."""
        logger.info("🚀 Starting Enhanced Manim Orchestration Pipeline...")
        pipeline_start = time.time()
        try:
            # Step 1: Setup
            phase_start = time.time()
            self._setup_directories()
            self.phase_times['setup'] = time.time() - phase_start
            
            # Step 2: Load and validate data
            phase_start = time.time()
            solution_steps = self._load_solution_steps()
            self._initialize_scene_metadata(solution_steps)
            self.phase_times['load_data'] = time.time() - phase_start
            
            # Step 3: Generate blueprints
            phase_start = time.time()
            blueprint_paths = self._generate_blueprints_with_retry(solution_steps, max_retries)
            self.phase_times['blueprint_generation'] = time.time() - phase_start
            
            # --- Commented out for blueprint testing ---
            # phase_start = time.time()
            # scripts = self._generate_manim_code_with_retry(blueprint_paths, max_retries)
            # self.phase_times['manim_code_generation'] = time.time() - phase_start
            # phase_start = time.time()
            # video_files = self._render_scenes_with_retry(scripts, max_retries)
            # self.phase_times['rendering'] = time.time() - phase_start
            # if not video_files:
            #     raise RuntimeError("No scenes were rendered successfully. Aborting.")
            # phase_start = time.time()
            # final_video_path = self._concatenate_videos(video_files)
            # self.phase_times['concatenation'] = time.time() - phase_start
            # self._generate_summary_report(final_video_path, start_time)
            # logger.info(f" Pipeline complete! Final video available at: {final_video_path}")
            # return final_video_path
            # --- End comment ---
            logger.info("Blueprint generation complete. Skipping Manim code generation and rendering.")
            total_time = time.time() - pipeline_start
            self.phase_times['total_pipeline'] = total_time
            self._log_timing_summary()
            return "Blueprints generated."
        except Exception as e:
            logger.error(f" Pipeline failed with an unrecoverable error: {e}", exc_info=True)
            self._generate_error_report(e, pipeline_start)
            raise
        finally:
            if cleanup:
                self._cleanup_temp_files()

    def _setup_directories(self):
        """Setup directories with better error handling."""
        directories_to_clean = [self.output_dir, self.manim_code_dir, self.blueprint_dir, self.temp_dir]
        
        for directory in directories_to_clean:
            try:
                if directory.exists():
                    shutil.rmtree(directory)
                directory.mkdir(exist_ok=True, parents=True)
            except PermissionError as e:
                logger.error(f"Permission denied when setting up directory {directory}: {e}")
                raise
            except Exception as e:
                logger.error(f"Failed to setup directory {directory}: {e}")
                raise
        
        logger.info(f" Cleaned and prepared output directories:")
        logger.info(f"  - Blueprints: {self.blueprint_dir}")
        logger.info(f"  - Manim Code: {self.manim_code_dir}")
        logger.info(f"  - Videos: {self.output_dir}")
        logger.info(f"  - Audio Source: {self.audio_dir}")
        logger.info(f"  - Temporary files: {self.temp_dir}")

    def _load_solution_steps(self) -> List[Dict[str, Any]]:
        """Load and validate solution steps."""
        logger.info(f"[1/6] Loading solution steps from '{self.input_file}'...")
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in input file: {e}")
        
        steps = data.get('solution_steps')
        if not steps or not isinstance(steps, list):
            raise ValueError("Input file must contain a 'solution_steps' list.")
        
        # Validate each step has required fields
        for i, step in enumerate(steps):
            required_fields = ['step_id', 'sentences']
            for field in required_fields:
                if field not in step:
                    raise ValueError(f"Step {i} missing required field: '{field}'")
            
            # Validate sentences structure
            if not isinstance(step['sentences'], list) or not step['sentences']:
                raise ValueError(f"Step {i} has invalid 'sentences' field")
        
        logger.info(f"✅ Loaded and validated {len(steps)} solution steps.")
        return steps

    def _initialize_scene_metadata(self, steps: List[Dict]):
        """Initialize metadata tracking for all scenes."""
        self.scene_metadata = []
        for i, step in enumerate(steps):
            duration = step.get('duration_scene_seconds', self._calculate_step_duration(step))
            audio_file = step.get('audio_file_scene')
            
            metadata = SceneMetadata(
                step_id=step['step_id'],
                index=i,
                duration=duration,
                audio_file=audio_file
            )
            self.scene_metadata.append(metadata)
        
        self.progress_tracker = ProgressTracker(len(steps))

    def _calculate_step_duration(self, step: Dict) -> float:
        """Calculate step duration from sentences."""
        sentences = step.get('sentences', [])
        if not sentences:
            return 10.0
        
        max_end = 0
        for sentence in sentences:
            end_time = sentence.get('end_time_seconds', sentence.get('duration_seconds', 0))
            max_end = max(max_end, end_time)
        
        return max_end if max_end > 0 else 10.0

    def _generate_blueprints_with_retry(self, steps: List[Dict], max_retries: int) -> List[Path]:
        """Generate blueprints with retry logic and progress tracking."""
        logger.info(f"[2/6] Generating {len(steps)} blueprints in parallel...")
        
        blueprint_paths = [None] * len(steps)
        retry_queue = list(range(len(steps)))
        
        for attempt in range(max_retries + 1):
            if not retry_queue:
                break
                
            current_batch = retry_queue.copy()
            retry_queue = []
            
            logger.info(f"Blueprint generation attempt {attempt + 1}/{max_retries + 1} for {len(current_batch)} items")
            
            with ThreadPoolExecutor(max_workers=min(8, len(current_batch))) as executor:
                future_to_index = {
                    executor.submit(self._generate_single_blueprint_safe, steps[i], i): i 
                    for i in current_batch
                }
                
                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        blueprint_dict = future.result()
                        if blueprint_dict:
                            scene_id = blueprint_dict.get('scene_id', f'scene_{index}')
                            bp_path = self.blueprint_dir / f"{index:02d}_{scene_id}.json"
                            
                            with open(bp_path, 'w', encoding='utf-8') as f:
                                json.dump(blueprint_dict, f, indent=2, ensure_ascii=False)
                            
                            blueprint_paths[index] = bp_path
                            self.scene_metadata[index].status = "completed"
                            logger.info(f" Blueprint {index}: {scene_id}")
                        else:
                            retry_queue.append(index)
                            self.scene_metadata[index].retry_count += 1
                            
                    except Exception as e:
                        logger.error(f" Error processing blueprint for step {index}: {e}")
                        retry_queue.append(index)
                        self.scene_metadata[index].retry_count += 1
                        self.scene_metadata[index].error = str(e)
        
        successful_paths = [p for p in blueprint_paths if p]
        failed_count = len(steps) - len(successful_paths)
        
        logger.info(f" Successfully generated {len(successful_paths)}/{len(steps)} blueprints")
        if failed_count > 0:
            logger.warning(f"  {failed_count} blueprints failed after {max_retries + 1} attempts")
        
        if not successful_paths:
            raise RuntimeError("Failed to generate any blueprints.")
        
        return successful_paths

    def _generate_single_blueprint_safe(self, step: Dict, index: int) -> Optional[Dict]:
        """Safely generate a single blueprint with better error handling."""
        try:
            return self._generate_single_blueprint(step, index)
        except Exception as e:
            logger.error(f"Blueprint generation failed for step {index}: {e}")
            return None

    def _generate_single_blueprint(self, step: Dict, index: int) -> Optional[Dict]:
        """Generate a single blueprint (enhanced version)."""
        step_id = step.get('step_id', f'step_{index}')
        logger.debug(f"  > Requesting blueprint for step {index}: {step_id}")
        
        # Create enhanced prompt with better context
        prompt = self._create_blueprint_prompt(step, index)
        
        # Get response from Gemini
        response_text = self._make_claude_request(prompt)
        
        # Parse and validate response
        parsed_json = self._extract_and_validate_json(response_text, "blueprint")
        
        if parsed_json and 'blueprint' in parsed_json and parsed_json['blueprint']:
            blueprint = parsed_json['blueprint'][0] if isinstance(parsed_json['blueprint'], list) else parsed_json['blueprint']
            
            # Enhance blueprint with additional metadata
            blueprint.update({
                'generated_at': time.time(),
                'step_index': index,
                'original_step_id': step_id,
                'audio_file_scene': step.get('audio_file_scene'),
                'duration_scene_seconds': step.get('duration_scene_seconds', self._calculate_step_duration(step))
            })
            
            return blueprint
        
        logger.warning(f"Could not parse valid blueprint from response for step {index}")
        return None

    def _create_blueprint_prompt(self, step: Dict, index: int) -> str:
        """Create an enhanced blueprint generation prompt."""
        return f"""{self.blueprint_prompt}

**Enhanced Context:**
- Scene Index: {index}
- Step ID: {step.get('step_id', 'unknown')}
- Duration: {step.get('duration_scene_seconds', 'auto-calculated')} seconds
- Audio Available: {'Yes' if step.get('audio_file_scene') else 'No'}

**Input Solution Step:**
```json
{json.dumps({'solution_steps': [step]}, indent=2, ensure_ascii=False)}
```

**Additional Instructions:**
- Ensure the blueprint is self-contained and can be rendered independently
- Include precise timing information for animations
- Consider the mathematical complexity and provide appropriate visual emphasis
- Ensure smooth transitions between visual elements
"""

    def _load_image_bytes(self) -> Optional[Image.Image]:
        """Load image as PIL.Image.Image for Gemini API."""
        if not self.image_path:
            return None
        try:
            image_path = Path(self.image_path)
            if not image_path.exists():
                logger.warning(f"Image file not found: {self.image_path}")
                return None
            img = Image.open(image_path)
            logger.debug(f"Loaded image: {self.image_path} (size: {img.size}, mode: {img.mode})")
            return img
        except Exception as e:
            logger.error(f"Failed to load image at {self.image_path}: {e}")
            return None

    def _make_claude_request(self, prompt: str) -> str:
        """Make an OpenRouter Claude API request and return the response text."""
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://yoursite.com",
                    "X-Title": "Your App Name",
                },
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8000,
                temperature=0.2
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Claude API request failed: {e}")
            raise

    def _extract_and_validate_json(self, text: str, expected_type: str = None) -> Optional[Dict]:
        """Extract and validate JSON from response with better error handling."""
        # Try multiple extraction patterns
        patterns = [
            r"```json\s*(\{.*?\})\s*```",
            r"```\s*(\{.*?\})\s*```",
            r"(\{[^{}]*\{.*?\}[^{}]*\})",  # Nested JSON
            r"(\{.*?\})"  # Simple JSON
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                json_str = match.group(1)
                try:
                    parsed = json.loads(json_str)
                    
                    # Basic validation
                    if expected_type and expected_type not in parsed:
                        continue
                    
                    return parsed
                except json.JSONDecodeError:
                    continue
        
        logger.warning(f"Could not find valid JSON in response. Text preview: {text[:200]}...")
        return None

    def _generate_manim_code_with_retry(self, blueprint_paths: List[Path], max_retries: int) -> List[Dict]:
        """Generate Manim code with retry logic."""
        logger.info(f"[3/6] Generating {len(blueprint_paths)} Manim scripts from blueprint files...")
        
        scripts = [None] * len(blueprint_paths)
        retry_queue = list(range(len(blueprint_paths)))
        
        for attempt in range(max_retries + 1):
            if not retry_queue:
                break
                
            current_batch = retry_queue.copy()
            retry_queue = []
            
            logger.info(f"Code generation attempt {attempt + 1}/{max_retries + 1} for {len(current_batch)} items")
            
            with ThreadPoolExecutor(max_workers=min(6, len(current_batch))) as executor:
                future_to_index = {
                    executor.submit(self._generate_single_manim_script_safe, blueprint_paths[i], i): i 
                    for i in current_batch
                }
                
                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        script_info = future.result()
                        if script_info:
                            scripts[index] = script_info
                            logger.info(f" Manim script {index}: {script_info['scene_id']}")
                        else:
                            retry_queue.append(index)
                            
                    except Exception as e:
                        logger.error(f" Error generating Manim code for blueprint at index {index}: {e}")
                        retry_queue.append(index)
        
        successful_scripts = [s for s in scripts if s]
        failed_count = len(blueprint_paths) - len(successful_scripts)
        
        logger.info(f" Successfully generated {len(successful_scripts)}/{len(blueprint_paths)} Manim scripts")
        if failed_count > 0:
            logger.warning(f"  {failed_count} scripts failed after {max_retries + 1} attempts")
        
        if not successful_scripts:
            raise RuntimeError("Failed to generate any Manim scripts.")
        
        return successful_scripts

    def _generate_single_manim_script_safe(self, blueprint_path: Path, index: int) -> Optional[Dict]:
        """Safely generate a single Manim script."""
        try:
            return self._generate_single_manim_script(blueprint_path, index)
        except Exception as e:
            logger.error(f"Manim script generation failed for {blueprint_path.name}: {e}")
            return None

    def _generate_single_manim_script(self, blueprint_path: Path, index: int) -> Optional[Dict]:
        """Generate a single Manim script with enhanced assembly logic."""
        logger.debug(f"  > Assembling Manim script for '{blueprint_path.name}'...")
        
        # Load and validate blueprint
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                blueprint = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Could not read or parse blueprint file at {blueprint_path}: {e}")
            return None
        
        scene_id = blueprint.get('scene_id', f'scene_{index}')
        class_name = self._scene_id_to_class_name(scene_id)
        
        # Prepare scene script with enhanced metadata
        scene_script = {
            "duration_seconds": self._calculate_scene_duration(blueprint),
            "scene_id": scene_id,
            "index": index,
            "timestamp": time.time()
        }
        
        # Handle audio file with better validation
        audio_file = self._find_audio_file(scene_id)
        scene_script['audio_file_path'] = str(audio_file.resolve()) if audio_file else None
        
        if audio_file:
            logger.debug(f"    - Found audio file: {audio_file.name}")
        else:
            logger.warning(f"    - Audio file not found for scene: {scene_id}")
        
        # Generate code using AI
        prompt = self._create_code_generation_prompt(blueprint, scene_script)
        response_text = self._make_claude_request(prompt)
        construct_body = self._extract_and_process_python_code(response_text)
        
        if not construct_body:
            logger.warning(f"Could not extract Python code from response for scene {scene_id}")
            return None
        
        # Assemble final script
        full_script_content = self._assemble_final_script(
            blueprint, scene_script, construct_body, class_name
        )
        
        # Save script
        script_path = self.manim_code_dir / f"{index:02d}_{scene_id}.py"
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(full_script_content)
        except Exception as e:
            logger.error(f"Failed to save script to {script_path}: {e}")
            return None
        
        return {
            'index': index,
            'scene_id': scene_id,
            'script_path': script_path,
            'class_name': class_name,
            'duration': scene_script['duration_seconds'],
            'has_audio': scene_script['audio_file_path'] is not None
        }

    def _find_audio_file(self, scene_id: str) -> Optional[Path]:
        """Find audio file with multiple naming patterns."""
        audio_patterns = [
            f"{scene_id}_scene.mp3",
            f"{scene_id}.mp3",
            f"{scene_id}_audio.mp3"
        ]
        
        for pattern in audio_patterns:
            audio_file = self.audio_dir / pattern
            if audio_file.exists():
                return audio_file
        
        return None

    def _create_code_generation_prompt(self, blueprint: Dict, scene_script: Dict) -> str:
        """Create enhanced code generation prompt."""
        return f"""{self.code_generator_prompt}

**Enhanced Generation Context:**
- Scene ID: {scene_script.get('scene_id', 'unknown')}
- Duration: {scene_script.get('duration_seconds', 10)} seconds
- Audio Available: {'Yes' if scene_script.get('audio_file_path') else 'No'}
- Render Quality: {self.render_config.quality}

**Scene Plan JSON:**
```json
{json.dumps(blueprint, ensure_ascii=False, indent=2)}
```

**Scene Script JSON:**
```json
{json.dumps(scene_script, ensure_ascii=False, indent=2)}
```

**Style Config JSON:**
```json
{json.dumps(self.style_config, ensure_ascii=False, indent=2)}
```

**Important Code Generation Guidelines:**
1. Generate ONLY the construct method body (no class definition, no imports)
2. Use proper timing for animations based on audio timestamps
3. Ensure all animations fit within the specified duration
4. Use the provided style configuration for consistent theming
5. Handle cases where audio might be missing gracefully
6. Include proper error handling for mathematical operations
7. Ensure smooth transitions between animation phases
"""

    def _extract_and_process_python_code(self, text: str) -> Optional[str]:
        """Extract and process Python code with enhanced logic."""
        # Try multiple extraction patterns
        code_patterns = [
            r"```python\s*(.*?)\s*```",
            r"```\s*(.*?)\s*```",
            r"def construct\(self\):\s*\n(.*?)(?=\n\s*(?:def|class|#|$))",
        ]
        
        extracted_code = None
        for pattern in code_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                extracted_code = match.group(1).strip()
                break
        
        if not extracted_code:
            logger.warning("Could not find Python code in response")
            return None
        
        # Process the extracted code
        processed_code = self._process_extracted_code(extracted_code)
        return processed_code

    def _process_extracted_code(self, code: str) -> str:
        """Process extracted code with enhanced patching."""
        # Remove import statements
        code = self._patch_imports(code)
        
        # Extract construct method body if full class was provided
        code = self._extract_construct_body(code)
        
        # Fix common indentation issues
        code = self._fix_indentation(code)
        
        # Add safety checks
        code = self._add_safety_checks(code)
        
        return code

    def _patch_imports(self, code: str) -> str:
        """Remove import statements with enhanced pattern matching."""
        patterns = [
            r'^\s*(import\s+.*)\n?',
            r'^\s*(from\s+.*import\s+.*)\n?',
            r'^\s*(#.*import.*)\n?'  # Comment imports
        ]
        
        patched_code = code
        total_removed = 0
        
        for pattern in patterns:
            patched_code, count = re.subn(pattern, '', patched_code, flags=re.MULTILINE)
            total_removed += count
        
        if total_removed > 0:
            logger.debug(f"    - Removed {total_removed} import statement(s)")
        
        return patched_code

    def _extract_construct_body(self, code: str) -> str:
        """Extract construct method body if full class definition provided."""
        # Look for construct method definition
        construct_pattern = r'def\s+construct\s*\(\s*self\s*\)\s*:\s*\n(.*?)(?=\n\s*def|\n\s*class|\Z)'
        match = re.search(construct_pattern, code, re.DOTALL)
        
        if match:
            logger.debug("    - Extracted construct method body from full class definition")
            return match.group(1)
        
        return code
    def _fix_indentation(self, code: str) -> str:
        """Fix common indentation issues."""
        lines = code.split('\n')
        if not lines:
            return code
        
        # Find minimum indentation (excluding empty lines)
        min_indent = float('inf')
        for line in lines:
            if line.strip():  # Skip empty lines
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)
        
        if min_indent == float('inf') or min_indent == 0:
            return code
        
        # Remove common indentation
        fixed_lines = []
        for line in lines:
            if line.strip():
                fixed_lines.append(line[min_indent:])
            else:
                fixed_lines.append('')
        
        return '\n'.join(fixed_lines)

    def _add_safety_checks(self, code: str) -> str:
        """Add safety checks to prevent common errors."""
        # Add try-catch for mathematical operations
        if 'sqrt(' in code or 'log(' in code or '/' in code:
            code = f"""try:
{self._indent_code(code, 4)}
except (ZeroDivisionError, ValueError) as e:
    logger.warning(f"Mathematical operation error: {{e}}")
    self.add(Text("Mathematical Error", color=RED).move_to(ORIGIN))"""
        
        return code

    def _indent_code(self, code: str, spaces: int) -> str:
        """Indent code by specified number of spaces."""
        indent = ' ' * spaces
        return '\n'.join(indent + line if line.strip() else line for line in code.split('\n'))

    def _assemble_final_script(self, blueprint: Dict, scene_script: Dict, 
                              construct_body: str, class_name: str) -> str:
        """Assemble the final Manim script."""
        imports = """from manim import *
import numpy as np
import math
import logging

logger = logging.getLogger(__name__)
"""
        
        # Add audio file path if available
        audio_path = scene_script.get('audio_file_path')
        audio_line = f'    audio_file = "{audio_path}"' if audio_path else '    audio_file = None'
        
        class_definition = f"""
class {class_name}(Scene):
{audio_line}
    
    def construct(self):
{self._indent_code(construct_body, 8)}
        self.wait(1)
"""
        
        return imports + class_definition

    def _scene_id_to_class_name(self, scene_id: str) -> str:
        """Convert scene ID to valid Python class name."""
        # Replace non-alphanumeric characters with underscores
        clean_id = re.sub(r'[^a-zA-Z0-9]', '_', scene_id)
        # Ensure it starts with a letter
        if clean_id and not clean_id[0].isalpha():
            clean_id = 'Scene_' + clean_id
        # Capitalize first letter of each word
        class_name = ''.join(word.capitalize() for word in clean_id.split('_'))
        return class_name or 'DefaultScene'

    def _calculate_scene_duration(self, blueprint: Dict) -> float:
        """Calculate scene duration from blueprint."""
        duration = blueprint.get('duration_scene_seconds')
        if duration:
            return float(duration)
        
        # Try to calculate from sentences
        sentences = blueprint.get('sentences', [])
        if sentences:
            max_end = 0
            for sentence in sentences:
                end_time = sentence.get('end_time_seconds', sentence.get('duration_seconds', 0))
                max_end = max(max_end, end_time)
            if max_end > 0:
                return max_end
        
        return 10.0  # Default duration

    def _render_scenes_with_retry(self, scripts: List[Dict], max_retries: int) -> List[Path]:
        """Render scenes with retry logic and progress tracking."""
        logger.info(f"[4/6] Rendering {len(scripts)} scenes in parallel...")
        
        video_files = [None] * len(scripts)
        retry_queue = list(range(len(scripts)))
        
        for attempt in range(max_retries + 1):
            if not retry_queue:
                break
                
            current_batch = retry_queue.copy()
            retry_queue = []
            
            logger.info(f"Rendering attempt {attempt + 1}/{max_retries + 1} for {len(current_batch)} scenes")
            
            with ThreadPoolExecutor(max_workers=self.render_config.max_workers) as executor:
                future_to_index = {
                    executor.submit(self._render_single_scene_safe, scripts[i]): i 
                    for i in current_batch
                }
                
                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        video_path = future.result()
                        if video_path and video_path.exists():
                            video_files[index] = video_path
                            logger.info(f"✅ Rendered scene {index}: {scripts[index]['scene_id']}")
                        else:
                            retry_queue.append(index)
                            logger.warning(f"❌ Failed to render scene {index}")
                            
                    except Exception as e:
                        logger.error(f"❌ Error rendering scene {index}: {e}")
                        retry_queue.append(index)
        
        successful_videos = [v for v in video_files if v]
        failed_count = len(scripts) - len(successful_videos)
        
        logger.info(f"🎬 Successfully rendered {len(successful_videos)}/{len(scripts)} scenes")
        if failed_count > 0:
            logger.warning(f"⚠️  {failed_count} scenes failed after {max_retries + 1} attempts")
        
        return successful_videos

    def _render_single_scene_safe(self, script_info: Dict) -> Optional[Path]:
        """Safely render a single scene."""
        try:
            return self._render_single_scene(script_info)
        except Exception as e:
            logger.error(f"Scene rendering failed for {script_info['scene_id']}: {e}")
            return None

    def _render_single_scene(self, script_info: Dict) -> Optional[Path]:
        """Render a single Manim scene."""
        scene_id = script_info['scene_id']
        script_path = script_info['script_path']
        class_name = script_info['class_name']
        index = script_info['index']
        
        output_file = self.output_dir / f"{index:02d}_{scene_id}.{self.render_config.format}"
        
        # Build manim command
        cmd = self._build_manim_command(script_path, class_name, output_file)
        
        logger.debug(f"Rendering command: {' '.join(cmd)}")
        
        try:
            # Run manim with timeout
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.render_config.timeout,
                cwd=self.output_dir
            )
            
            if result.returncode == 0:
                # Find the actual output file (manim might change the name)
                actual_output = self._find_rendered_file(output_file, scene_id)
                if actual_output and actual_output.exists():
                    return actual_output
                else:
                    logger.error(f"Rendered file not found for scene {scene_id}")
                    logger.debug(f"Manim stdout: {result.stdout}")
                    return None
            else:
                logger.error(f"Manim rendering failed for scene {scene_id}")
                logger.error(f"Return code: {result.returncode}")
                logger.error(f"Stderr: {result.stderr}")
                logger.debug(f"Stdout: {result.stdout}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"Manim rendering timed out for scene {scene_id} (>{self.render_config.timeout}s)")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during rendering of scene {scene_id}: {e}")
            return None

    def _build_manim_command(self, script_path: Path, class_name: str, output_file: Path) -> List[str]:
        """Build the manim command with appropriate quality settings."""
        cmd = ["manim"]
        
        # Quality settings
        quality_flags = {
            "low_quality": ["-ql", "--fps", "15"],
            "medium_quality": ["-qm", "--fps", str(self.render_config.frame_rate)],
            "high_quality": ["-qh", "--fps", str(self.render_config.frame_rate)],
            "production_quality": ["-qk", "--fps", str(self.render_config.frame_rate)]
        }
        
        cmd.extend(quality_flags.get(self.render_config.quality, quality_flags["medium_quality"]))
        
        # Output settings
        cmd.extend([
            "--format", self.render_config.format,
            "--output_file", output_file.name,
            str(script_path),
            class_name
        ])
        
        return cmd

    def _find_rendered_file(self, expected_path: Path, scene_id: str) -> Optional[Path]:
        """Find the actual rendered file (manim sometimes changes filenames)."""
        # Check exact expected path first
        if expected_path.exists():
            return expected_path
        
        # Search for files with similar names
        search_patterns = [
            f"*{scene_id}*.{self.render_config.format}",
            f"*{expected_path.stem}*.{self.render_config.format}",
            f"*.{self.render_config.format}"
        ]
        
        for pattern in search_patterns:
            matches = list(self.output_dir.glob(pattern))
            if matches:
                # Return the most recently modified file
                return max(matches, key=lambda f: f.stat().st_mtime)
        
        return None

    def _concatenate_videos(self, video_files: List[Path]) -> str:
        """Concatenate video files into final output."""
        logger.info(f"[5/6] Concatenating {len(video_files)} video files...")
        
        if len(video_files) == 1:
            final_path = self.output_dir / f"final_animation.{self.render_config.format}"
            shutil.copy2(video_files[0], final_path)
            logger.info(f"✅ Single video copied to: {final_path}")
            return str(final_path)
        
        # Create file list for ffmpeg
        file_list_path = self.temp_dir / "file_list.txt"
        with open(file_list_path, 'w') as f:
            for video_file in sorted(video_files):
                f.write(f"file '{video_file.resolve()}'\n")
        
        final_path = self.output_dir / f"final_animation.{self.render_config.format}"
        
        # Use ffmpeg to concatenate
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(file_list_path),
            "-c", "copy",
            str(final_path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0 and final_path.exists():
                logger.info(f"✅ Successfully concatenated videos to: {final_path}")
                return str(final_path)
            else:
                logger.error(f"FFmpeg concatenation failed: {result.stderr}")
                raise RuntimeError("Video concatenation failed")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Video concatenation timed out")
        except Exception as e:
            logger.error(f"Error during video concatenation: {e}")
            raise

    def _generate_summary_report(self, final_video_path: str, start_time: float):
        """Generate a summary report of the orchestration process."""
        duration = time.time() - start_time
        
        report = {
            "orchestration_summary": {
                "total_duration_seconds": round(duration, 2),
                "final_video_path": final_video_path,
                "total_scenes": len(self.scene_metadata),
                "successful_scenes": len([m for m in self.scene_metadata if m.status == "completed"]),
                "failed_scenes": len([m for m in self.scene_metadata if m.status == "failed"]),
                "render_config": {
                    "quality": self.render_config.quality,
                    "format": self.render_config.format,
                    "frame_rate": self.render_config.frame_rate,
                    "resolution": self.render_config.resolution
                },
                "scene_details": [
                    {
                        "step_id": m.step_id,
                        "index": m.index,
                        "status": m.status,
                        "duration": m.duration,
                        "has_audio": m.audio_file is not None,
                        "retry_count": m.retry_count,
                        "error": m.error
                    }
                    for m in self.scene_metadata
                ]
            }
        }
        
        report_path = self.output_dir / "orchestration_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Orchestration completed in {duration:.1f} seconds")
        logger.info(f"📄 Summary report saved to: {report_path}")

    def _generate_error_report(self, error: Exception, start_time: float):
        """Generate an error report for failed orchestration."""
        duration = time.time() - start_time
        
        error_report = {
            "orchestration_error": {
                "error_type": type(error).__name__,
                "error_message": str(error),
                "duration_before_failure": round(duration, 2),
                "scene_statuses": [
                    {
                        "step_id": m.step_id,
                        "index": m.index,
                        "status": m.status,
                        "retry_count": m.retry_count,
                        "error": m.error
                    }
                    for m in self.scene_metadata
                ] if hasattr(self, 'scene_metadata') else []
            }
        }
        
        error_report_path = self.output_dir / "error_report.json"
        try:
            with open(error_report_path, 'w', encoding='utf-8') as f:
                json.dump(error_report, f, indent=2, ensure_ascii=False)
            logger.info(f"💥 Error report saved to: {error_report_path}")
        except Exception as e:
            logger.error(f"Failed to save error report: {e}")

    def _cleanup_temp_files(self):
        """Clean up temporary files and directories."""
        logger.info("[6/6] Cleaning up temporary files...")
        
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            
            # Clean up individual script files if requested
            cleanup_scripts = os.getenv("CLEANUP_SCRIPTS", "false").lower() == "true"
            if cleanup_scripts and self.manim_code_dir.exists():
                shutil.rmtree(self.manim_code_dir)
                logger.info("🗑️  Cleaned up generated scripts")
            
            # Clean up blueprints if requested
            cleanup_blueprints = os.getenv("CLEANUP_BLUEPRINTS", "false").lower() == "true"
            if cleanup_blueprints and self.blueprint_dir.exists():
                shutil.rmtree(self.blueprint_dir)
                logger.info("🗑️  Cleaned up generated blueprints")
                
            logger.info("✅ Cleanup completed")
            
        except Exception as e:
            logger.warning(f"⚠️  Cleanup failed: {e}")

    def _log_timing_summary(self):
        logger.info("\n===== TIMING SUMMARY =====")
        for phase, duration in self.phase_times.items():
            logger.info(f"Phase '{phase}': {duration:.2f} seconds")
        if self.api_call_times:
            logger.info("Claude API call durations:")
            for i, (step, duration) in enumerate(self.api_call_times):
                logger.info(f"  Call {i+1} ({step}): {duration:.2f} seconds")
        logger.info("==========================\n")


def main():
    """Main entry point for the orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manim Animation Orchestrator")
    parser.add_argument("--input", required=True, help="Input JSON file with solution steps")
    parser.add_argument("--styler", required=True, help="Style configuration JSON file")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--blueprints", default="blueprints", help="Blueprint directory")
    parser.add_argument("--scripts", default="manim_scripts", help="Manim scripts directory")
    parser.add_argument("--audio", default="audio", help="Audio files directory")
    parser.add_argument("--image", help="Optional image file to include in prompts")
    parser.add_argument("--quality", choices=["low_quality", "medium_quality", "high_quality", "production_quality"], 
                       default="medium_quality", help="Render quality")
    parser.add_argument("--format", choices=["mp4", "mov", "avi"], default="mp4", help="Output format")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate")
    parser.add_argument("--workers", type=int, default=4, help="Maximum parallel workers")
    parser.add_argument("--retries", type=int, default=2, help="Maximum retry attempts")
    parser.add_argument("--no-cleanup", action="store_true", help="Skip cleanup of temporary files")
    parser.add_argument("--log-file", help="Log file path")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       default="INFO", help="Logging level")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    
    # Get API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY environment variable is required")
        sys.exit(1)
    
    # Create render config
    render_config = RenderConfig(
        quality=args.quality,
        format=args.format,
        frame_rate=args.fps,
        max_workers=args.workers
    )
    
    try:
        # Initialize orchestrator
        orchestrator = ManimOrchestrator(
            api_key=api_key,
            input_file=args.input,
            styler_file=args.styler,
            output_dir=args.output,
            blueprint_dir=args.blueprints,
            manim_code_dir=args.scripts,
            audio_dir=args.audio,
            image_path=args.image,
            render_config=render_config,
            log_file=args.log_file
        )
        
        # Run orchestration
        final_video = orchestrator.run(
            cleanup=not args.no_cleanup,
            max_retries=args.retries
        )
        
        print(f"\n🎉 SUCCESS! Final video created at: {final_video}")
        
    except Exception as e:
        logger.error(f"Orchestration failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()