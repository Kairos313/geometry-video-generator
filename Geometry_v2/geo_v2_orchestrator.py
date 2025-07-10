#!/usr/bin/env python3
"""
Manim Animation Orchestrator (v2 - Refactored)

This orchestrator handles the complete pipeline:
1.  Loads prompts from external files.
2.  Generates blueprints for each scene in parallel, saving each to a separate file.
3.  Generates, PATCHES, and intelligently ASSEMBLES self-contained Manim code for each scene.
4.  Renders each scene independently in parallel.
5.  Concatenates all rendered videos into a final combined video.
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
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from google.genai import types

# --- Robustly add project root to Python path ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))
    from Geometry_v2.orchestrator_prompts import Animator_Phase_1_Blueprint_Balanced, Animator_Phase_2_Code_Generation_v2 as Animator_Phase_2_Code_Generation
except ImportError:
    print("\n--- ERROR ---")
    print("Could not import prompts from 'Geometry_v2.orchestrator_prompts'.")
    print("Please ensure you have the latest prompt named 'Animator_Phase_2_Code_Generation_v2' in that file.")
    sys.exit(1)

# --- Basic Setup ---
try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai package not found. Please run 'pip install google-generativeai'.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()


class ManimOrchestrator:
    """Orchestrates the creation of Manim animations from structured data."""

    def __init__(self,
                 api_key: str,
                 input_file: str,
                 styler_file: str,
                 output_dir: str,
                 blueprint_dir: str,
                 manim_code_dir: str,
                 audio_dir: str,
                 temp_dir: str = "temp",
                 image_path: Optional[str] = None):
        """
        Initializes the orchestrator.
        """
        self.api_key = api_key
        self.input_file = Path(input_file)
        self.styler_file = Path(styler_file)
        self.output_dir = Path(output_dir)
        self.blueprint_dir = Path(blueprint_dir)
        self.manim_code_dir = Path(manim_code_dir)
        self.audio_dir = Path(audio_dir)
        self.temp_dir = Path(temp_dir)
        self.image_path = image_path
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')

        self.blueprint_prompt = Animator_Phase_1_Blueprint_Balanced
        self.code_generator_prompt = Animator_Phase_2_Code_Generation
        logger.info("Loaded prompts from 'orchestrator_prompts.py'.")
        
        try:
            with open(self.styler_file, 'r') as f:
                self.style_config = json.load(f)
            logger.info(f"Loaded style configuration from '{self.styler_file}'.")
        except FileNotFoundError:
            logger.error(f"Error: Styler file not found at {self.styler_file}.")
            raise
        except json.JSONDecodeError:
            logger.error(f"Error: Could not decode JSON from styler file {self.styler_file}.")
            raise

    def run(self, cleanup: bool = True):
        logger.info("🚀 Starting Manim Orchestration Pipeline...")
        self._setup_directories()
        try:
            solution_steps = self._load_solution_steps()
            blueprint_paths = self._generate_blueprints(solution_steps)
            scripts = self._generate_manim_code(blueprint_paths)
            video_files = self._render_scenes(scripts)
            if not video_files:
                raise RuntimeError("No scenes were rendered successfully. Aborting.")
            final_video_path = self._concatenate_videos(video_files)
            logger.info(f" Pipeline complete! Final video available at: {final_video_path}")
            return final_video_path
        except Exception as e:
            logger.error(f"Pipeline failed with an unrecoverable error: {e}", exc_info=True)
            raise
        finally:
            if cleanup:
                self._cleanup_temp_files()

    def _setup_directories(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)
        shutil.rmtree(self.manim_code_dir, ignore_errors=True)
        shutil.rmtree(self.blueprint_dir, ignore_errors=True)
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.manim_code_dir.mkdir(exist_ok=True, parents=True)
        self.blueprint_dir.mkdir(exist_ok=True, parents=True)
        self.temp_dir.mkdir(exist_ok=True)
        
        logger.info(f"Cleaned and prepared output directories:")
        logger.info(f"  - Blueprints: {self.blueprint_dir}")
        logger.info(f"  - Manim Code: {self.manim_code_dir}")
        logger.info(f"  - Videos: {self.output_dir}")
        logger.info(f"  - Audio Source: {self.audio_dir}")
        logger.info(f"  - Temporary files: {self.temp_dir}")

    def _load_solution_steps(self) -> List[Dict[str, Any]]:
        logger.info(f"[1/5] Loading solution steps from '{self.input_file}'...")
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        steps = data.get('solution_steps')
        if not steps or not isinstance(steps, list):
            raise ValueError("Input file must contain a 'solution_steps' list.")
        
        logger.info(f"Loaded {len(steps)} solution steps.")
        return steps

    def _generate_blueprints(self, steps: List[Dict]) -> List[Path]:
        logger.info(f"[2/5] Generating {len(steps)} blueprints in parallel...")
        blueprint_paths = [None] * len(steps)
        with ThreadPoolExecutor() as executor:
            future_to_index = {executor.submit(self._generate_single_blueprint, step, i): i for i, step in enumerate(steps)}
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
                except Exception as e:
                    logger.error(f"Error processing blueprint for step {index}: {e}")
        
        successful_paths = [p for p in blueprint_paths if p]
        logger.info(f"Successfully generated and saved {len(successful_paths)}/{len(steps)} blueprint files to '{self.blueprint_dir}'.")
        
        if not successful_paths:
            raise RuntimeError("Failed to generate any blueprints.")
        return successful_paths

    def _load_image_bytes(self) -> Optional[bytes]:
        if not self.image_path:
            return None
        try:
            with open(self.image_path, "rb") as img_file:
                return img_file.read()
        except Exception as e:
            logger.error(f"Failed to load image at {self.image_path}: {e}")
            return None

    def _generate_single_blueprint(self, step: Dict, index: int) -> Optional[Dict]:
        logger.info(f"  > Requesting blueprint for step {index}: {step.get('step_id', 'N/A')}")
        prompt = f"{self.blueprint_prompt}\n\n**Input Solution Step:**\n```json\n{json.dumps({'solution_steps': [step]}, indent=2)}\n```"
        image_bytes = self._load_image_bytes()
        if image_bytes:
            contents = [
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/png',
                ),
                prompt
            ]
            response = self.model.generate_content(contents)
            response_text = response.text
        else:
            response_text = self._make_gemini_request(prompt)
        parsed_json = self._extract_json_from_response(response_text)
        if parsed_json and 'blueprint' in parsed_json and parsed_json['blueprint']:
            return parsed_json['blueprint'][0]
        logger.warning(f"Could not parse valid blueprint from response for step {index}. Response text: {response_text[:500]}...")
        return None

    def _generate_manim_code(self, blueprint_paths: List[Path]) -> List[Dict]:
        logger.info(f"[3/5] Generating {len(blueprint_paths)} Manim scripts from blueprint files...")
        scripts = [None] * len(blueprint_paths)
        with ThreadPoolExecutor() as executor:
            future_to_index = {executor.submit(self._generate_single_manim_script, bp_path, i): i for i, bp_path in enumerate(blueprint_paths)}
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    script_info = future.result()
                    if script_info:
                        scripts[index] = script_info
                except Exception as e:
                    logger.error(f"Error generating Manim code for blueprint at index {index}: {e}")

        successful_scripts = [s for s in scripts if s]
        logger.info(f"Successfully generated {len(successful_scripts)}/{len(blueprint_paths)} Manim scripts. They are saved in '{self.manim_code_dir}'.")
        if not successful_scripts:
            raise RuntimeError("Failed to generate any Manim scripts.")
        return successful_scripts
        
    def _patch_imports(self, code: str) -> str:
        """Removes `import` and `from ... import` statements from the AI-generated code block."""
        pattern = re.compile(r'^\s*(import\s.*|from\s.*import\s.*)\n?', re.MULTILINE)
        patched_code, count = re.subn(pattern, '', code)
        if count > 0:
            logger.info(f"    - Patched code: Removed {count} redundant import statement(s).")
        return patched_code

    def _generate_single_manim_script(self, blueprint_path: Path, index: int) -> Optional[Dict]:
        """
        Generates a Manim script by intelligently assembling it, asking the AI only for specific code blocks.
        """
        logger.info(f"  > Assembling Manim script for '{blueprint_path.name}'...")
        
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                blueprint = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Could not read or parse blueprint file at {blueprint_path}: {e}")
            return None
        
        scene_id = blueprint.get('scene_id', f'scene_{index}')
        class_name = self._scene_id_to_class_name(scene_id)
        
        scene_script = {"duration_seconds": self._calculate_scene_duration(blueprint)}
        audio_file = self.audio_dir / f"{scene_id}_scene.mp3" 
        
        if audio_file.exists():
            scene_script['audio_file_path'] = str(audio_file.resolve())
            logger.info(f"    - Found audio file: {audio_file.name}")
        else:
            scene_script['audio_file_path'] = None
            logger.warning(f"    - Audio file not found at '{audio_file}'. No sound will be added.")
            
        prompt = (
            f"{self.code_generator_prompt}\n\n"
            f"**Scene Plan JSON:**\n```json\n{json.dumps(blueprint, ensure_ascii=False)}\n```\n\n"
            f"**Scene Script JSON:**\n```json\n{json.dumps(scene_script)}\n```\n\n"
            f"**Style Config JSON:**\n```json\n{json.dumps(self.style_config)}\n```"
        )
        
        response_text = self._make_gemini_request(prompt)
        construct_body = self._extract_python_code(response_text)

        if not construct_body:
            logger.warning(f"Could not extract Python code from response for scene {scene_id}.")
            return None
        
        # Patch the generated code to remove any stray import statements
        construct_body = self._patch_imports(construct_body)
        
        indented_construct_body = "\n".join(["        " + line for line in construct_body.splitlines()])
        
        def safe_json_str(obj):
            return json.dumps(obj, ensure_ascii=False).replace('\\', '\\\\')
        
        full_script_content = f"""# -*- coding: utf-8 -*-
from manim import *
import json

# --- Data injected by orchestrator (Correctly Escaped) ---
scene_plan_json = '''{safe_json_str(blueprint)}'''
scene_script_json = '''{safe_json_str(scene_script)}'''
style_config_json = '''{safe_json_str(self.style_config)}'''

class {class_name}(Scene):
    def construct(self):
        # --- Start of AI-generated and Patched code block ---
{indented_construct_body}
        # --- End of AI-generated code block ---
"""
        script_path = self.manim_code_dir / f"{index:02d}_{scene_id}.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(full_script_content)
            
        return {'index': index, 'scene_id': scene_id, 'script_path': script_path, 'class_name': class_name}

    def _render_scenes(self, scripts: List[Dict]) -> List[str]:
        logger.info(f"[4/5] Rendering {len(scripts)} scenes in parallel...")
        video_files = [None] * len(scripts)
        max_workers = min(os.cpu_count() or 1, 4)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_index = {executor.submit(self._render_single_scene, script): script['index'] for script in scripts if script}
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    video_path = future.result()
                    if video_path:
                        video_files[index] = video_path
                except Exception as e:
                    logger.error(f"Error rendering scene at index {index}: {e}")
        successful_renders = [v for v in video_files if v]
        logger.info(f"Successfully rendered {len(successful_renders)}/{len(scripts)} scenes to '{self.output_dir}'.")
        return successful_renders
        
    def _render_single_scene(self, script_info: Dict) -> Optional[str]:
        index, scene_id, script_path, class_name = script_info['index'], script_info['scene_id'], script_info['script_path'], script_info['class_name']
        media_dir = self.output_dir
        output_filename = f"{index:02d}_{scene_id}"
        final_render_path = media_dir / f"{output_filename}.mp4"
        logger.info(f"  > Rendering scene {index}: {class_name}...")
        command = ["manim", str(script_path), class_name, "--format", "mp4", "--media_dir", str(media_dir), "-ql", "--progress_bar", "none", "--output_file", output_filename]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=300)
            if result.returncode == 0 and final_render_path.exists():
                logger.info(f"  > Finished rendering scene {index}: {scene_id}")
                return str(final_render_path)
            else:
                log_path = media_dir / f"{output_filename}.log"
                error_message = f"Failed to render scene {index}: {scene_id}."
                if not final_render_path.exists(): error_message += " Output file not found."
                logger.error(error_message)
                logger.debug(f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}")
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.write(f"COMMAND: {' '.join(command)}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout expired while rendering scene {index}: {scene_id}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while rendering scene {index}: {e}", exc_info=True)
            return None

    def _concatenate_videos(self, video_files: List[str]) -> str:
        logger.info("[5/5] Concatenating videos...")
        valid_video_files = sorted([f for f in video_files if f])
        if not valid_video_files:
            raise RuntimeError("Concatenation failed: No valid video files to process.")
        filelist_path = self.temp_dir / "filelist.txt"
        with open(filelist_path, "w", encoding='utf-8') as f:
            for video_file in valid_video_files:
                f.write(f"file '{Path(video_file).resolve()}'\n")
        final_video_path = self.output_dir / "final_animation.mp4"
        command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(filelist_path), "-c", "copy", "-y", str(final_video_path)]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg concatenation failed:\n{result.stderr}")
        logger.info("Video concatenation successful.")
        return str(final_video_path)

    def _make_gemini_request(self, prompt: str, max_retries: int = 3) -> str:
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.warning(f"Gemini API call attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2 ** (attempt + 1))
        raise RuntimeError(f"Gemini API call failed after {max_retries} retries.")

    def _extract_json_from_response(self, text: str) -> Optional[Dict]:
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON found inside markdown block: {e}")
                logger.debug(f"Problematic JSON string: {json_str}")
                return None
        logger.warning("Could not find a JSON markdown block in the response.")
        return None

    ### CHANGE: NEW, MORE ROBUST EXTRACTION LOGIC ###
    def _extract_python_code(self, text: str) -> Optional[str]:
        """
        Safely extracts Python code from a string, handling cases where the AI
        incorrectly includes a full class definition.
        """
        # First, try to find a standard python markdown block
        code_block_match = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
        if not code_block_match:
            # Fallback for responses that are just code without fences
            if "def construct(self):" in text:
                code_block = text.strip()
            else:
                logger.warning("Could not find a Python code block in the response.")
                return None
        else:
            code_block = code_block_match.group(1).strip()

        # Now, check if the extracted block contains a full class definition
        construct_body_match = re.search(
            r"def\s+construct\s*\(\s*self\s*\):\s*\n(.*?)\n\s*(?=\n|# --- End of AI-generated code block ---|$)",
            code_block,
            re.DOTALL
        )

        if construct_body_match:
            # We found a `construct` method, extract its body
            logger.info("    - Extracted construct method body from a full class definition.")
            # Un-indent the captured body
            body = construct_body_match.group(1)
            lines = body.split('\n')
            if not lines:
                return ""
            
            # Determine the indentation of the first line
            first_line_indent = len(lines[0]) - len(lines[0].lstrip())
            
            # Remove that amount of indentation from all lines
            unindented_lines = [line[first_line_indent:] if len(line) >= first_line_indent else line for line in lines]
            return "\n".join(unindented_lines)

        # If no `construct` method was found, assume the whole block is the body
        return code_block
    ### END CHANGE ###


    def _calculate_scene_duration(self, blueprint: Dict) -> float:
        timestamps = blueprint.get('sentence_timestamps', [])
        if not timestamps:
            return 10.0
        
        all_ends = []
        for ts in timestamps:
            if isinstance(ts, dict) and 'end' in ts:
                all_ends.append(ts.get('end', 0))
            elif isinstance(ts, list) and len(ts) > 1:
                all_ends.append(ts[1])
        
        return max(all_ends) if all_ends else 10.0

    def _scene_id_to_class_name(self, scene_id: str) -> str:
        clean_id = re.sub(r'[^a-zA-Z0-9_]', '', scene_id)
        if not clean_id or not clean_id[0].isalpha():
            clean_id = 'Scene' + clean_id
        return "".join(word.capitalize() for word in clean_id.split('_'))

    def _cleanup_temp_files(self):
        logger.info(f"Cleaning up temporary directory: {self.temp_dir}")
        shutil.rmtree(self.temp_dir, ignore_errors=True)


def main():
    import argparse
    
    BASE_PATH = "/Users/kairos/Desktop/Prompt Generation"
    INPUT_JSON_FILE = f"{BASE_PATH}/Geometry_v2/deconstruct_parallel.json"
    STYLER_JSON_FILE = f"{BASE_PATH}/Geometry_v1/geo_styler_v1.json"
    
    BLUEPRINT_DIR = f"{BASE_PATH}/Geometry_v2/Blueprint"
    MANIM_CODE_DIR = f"{BASE_PATH}/Geometry_v2/Manim Code"
    VIDEO_OUTPUT_DIR = f"{BASE_PATH}/Geometry_v2/Video"
    AUDIO_DIR = f"{BASE_PATH}/Geometry_v2/Scene"
    IMAGE_PATH = f"{BASE_PATH}/Geometry_v2/math_question.png"
    
    parser = argparse.ArgumentParser(description="Manim Animation Orchestrator v2 (with configured paths)")
    
    parser.add_argument("-k", "--api-key", default=os.getenv("GOOGLE_API_KEY"), help="Google Gemini API key (overrides .env).")
    parser.add_argument("--no-cleanup", action="store_true", help="Do not delete the temporary directory after execution.")

    args = parser.parse_args()

    if not args.api_key:
        logger.error("API Key not found. Please provide it via the --api-key argument or a GOOGLE_API_KEY in a .env file.")
        return

    orchestrator = ManimOrchestrator(
        api_key=args.api_key,
        input_file=INPUT_JSON_FILE,
        styler_file=STYLER_JSON_FILE,
        output_dir=VIDEO_OUTPUT_DIR,
        blueprint_dir=BLUEPRINT_DIR,
        manim_code_dir=MANIM_CODE_DIR,
        audio_dir=AUDIO_DIR,
        temp_dir="temp",
        image_path=IMAGE_PATH
    )

    orchestrator.run(cleanup=not args.no_cleanup)


if __name__ == "__main__":
    main()