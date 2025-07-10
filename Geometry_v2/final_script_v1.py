import os
import json
import sys
import time
import base64
import re
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

# Add the prompt directory to the path to import the prompts
sys.path.append('/Users/kairos/Desktop/Prompt Generation/Geometry_v2')
from final_animation_prompt import Final_Animation_Scene_1_v4, Final_Animation_Other_Scenes_v4

# Set up OpenRouter client using OpenAI SDK
load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

class ClaudeAnimationGenerator:
    def __init__(self, api_key=None, site_url=None, site_title=None):
        """
        Initialize the OpenRouter API client.
        Args:
            api_key (str, optional): OpenRouter API key. If not provided, will look for OPENROUTER_API_KEY environment variable.
            site_url (str, optional): For OpenRouter rankings.
            site_title (str, optional): For OpenRouter rankings.
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or OPENROUTER_API_KEY environment variable")
        self.client = client
        self.site_url = site_url or "https://your-site-url.com"
        self.site_title = site_title or "Your Site Name"
        self.system_prompt = "You are an expert Manim programmer specializing in educational animations in the style of 3Blue1Brown."
        self.token_usage = []  # Track token usage per scene

    def load_image(self, image_path):
        """Load and prepare image for Claude API."""
        if not image_path:
            return None
        
        img_path = Path(image_path)
        if not img_path.exists():
            print(f"Warning: Image not found: {image_path}")
            return None
        
        try:
            return Image.open(img_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def prepare_image_for_api(self, image_path):
        """Prepare image data for OpenRouter API call as a data URI."""
        if not image_path or not Path(image_path).exists():
            return None
        try:
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()
            ext = Path(image_path).suffix.lower()
            media_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            data_uri = f"data:{media_type};base64,{image_b64}"
            print(f"[VERIFY] Sending image: {image_path}")
            print(f"[VERIFY] Data URI sample: {data_uri[:60]}... (length: {len(data_uri)})")
            return {
                "type": "image_url",
                "image_url": {
                    "url": data_uri
                }
            }
        except Exception as e:
            print(f"Error preparing image for API: {e}")
            return None
    
    def extract_python_code(self, text):
        """Extract Python code from Claude's response."""
        code_patterns = [
            r"```python\s*(.*?)\s*```",
            r"```\s*(.*?)\s*```",
            r"class\s+\w+\s*\(Scene\):\s*(.*?)(?=\n\s*(?:class|def|#|$)|\Z)",
        ]
        
        for pattern in code_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                code = match.group(1).strip()
                # Clean up the code
                code = re.sub(r'```(?:python)?', '', code)
                code = re.sub(r'```', '', code)
                return code.strip()
        
        return text.strip()
    
    def clean_generated_code(self, code):
        """Clean up generated code by removing unnecessary imports and JSON operations."""
        # Remove problematic lines
        code = re.sub(r'.*json\.loads\(.*?\).*\n', '', code)
        code = re.sub(r'.*import json.*\n', '', code)
        code = re.sub(r'.*from manim import.*\n', '', code)
        
        return code.strip()
    
    def generate_first_scene(self, first_step_json, problem_image_path, output_dir="/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Generated_Scenes_Both"):
        """
        Generate the first scene animation using Claude API.
        
        Args:
            first_step_json (dict): JSON object containing step_id and sentences
            problem_image_path (str): Path to the reference image
            output_dir (str): Directory to save generated scenes
            0
        Returns:
            tuple: (generated_code, output_path)
        """
        # Use the correct scene name from the step JSON
        scene_id = first_step_json["step_id"]
        # Prepare the enhanced prompt
        user_prompt = f"""{Final_Animation_Scene_1_v4}

**Enhanced Generation Context:**
- Scene ID: {scene_id}
- Duration: Based on sentence timings
- Audio Available: {'Yes' if first_step_json.get('sentences') else 'No'}
- Render Quality: medium_quality

**INPUTS:**
first_step_json = {json.dumps(first_step_json, ensure_ascii=False, indent=2)}

problem_image_path = "{problem_image_path}"

**Important Code Generation Guidelines:**
1. Generate ONLY the Scene class definition (including class declaration and imports)
2. Use proper timing for animations based on sentence timestamps
3. Ensure all animations are synchronized with the provided timings
4. Include proper error handling for mathematical operations
5. Ensure smooth transitions between animation phases
6. Reference Manim documentation for correct syntax and parameters
7. Generate complete, runnable code

Please generate the complete Python script for the first scene animation."""

        # Prepare message parts
        message_content = [
            {"type": "text", "text": user_prompt}
        ]
        
        # Add image if available
        image_part = self.prepare_image_for_api(problem_image_path)
        if image_part:
            message_content.append(image_part)
        
        try:
            print(f"Generating first scene: {scene_id}")
            start_time = time.time()
            
            # Make the API call
            response = self.client.chat.completions.create(
                model="anthropic/claude-sonnet-4",  # Use sonnet-4 for the first scene
                max_tokens=8000,
                temperature=0.1,
                extra_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_title
                },
                messages=[{"role": "user", "content": message_content}],
            )
            
            api_duration = time.time() - start_time
            print(f"Claude API call duration: {api_duration:.2f} seconds")
            
            # Extract and clean the generated code
            response_text = response.choices[0].message.content
            generated_code = self.extract_python_code(response_text)
            
            # Extract token usage
            usage = getattr(response, 'usage', None)
            if usage:
                prompt_tokens = getattr(usage, 'prompt_tokens', 0)
                completion_tokens = getattr(usage, 'completion_tokens', 0)
                total_tokens = getattr(usage, 'total_tokens', 0)
            else:
                prompt_tokens = completion_tokens = total_tokens = 0
            self.token_usage.append({
                'scene_id': scene_id,
                'input': prompt_tokens,
                'output': completion_tokens,
                'total': total_tokens
            })
            print(f"[Tokens] Scene {scene_id}: input={prompt_tokens}, output={completion_tokens}, total={total_tokens}")
            # Save the generated code
            output_path = self._save_scene_code(generated_code, scene_id, output_dir, response_text)
            
            return generated_code, output_path
            
        except Exception as e:
            print(f"Error generating first scene: {e}")
            return None, None
    
    def generate_subsequent_scene(self, previous_scene_code, current_step_json, problem_image_path, output_dir="/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Generated_Scenes_Both"):
        """
        Generate a subsequent scene animation using Claude API.
        
        Args:
            previous_scene_code (str): Complete Python script from the previous scene
            current_step_json (dict): JSON object for the current step
            problem_image_path (str): Path to the reference image
            output_dir (str): Directory to save generated scenes
            
        Returns:
            tuple: (generated_code, output_path)
        """
        # Use the correct scene name from the step JSON
        scene_id = current_step_json["step_id"]
        # Prepare the enhanced prompt
        user_prompt = f"""{Final_Animation_Other_Scenes_v4}

**Enhanced Generation Context:**
- Scene ID: {scene_id}
- Duration: Based on sentence timings
- Audio Available: {'Yes' if current_step_json.get('sentences') else 'No'}
- Render Quality: medium_quality

**INPUTS:**
previous_scene_code = '''
{previous_scene_code}
'''

current_step_json = {json.dumps(current_step_json, ensure_ascii=False, indent=2)}

problem_image_path = "{problem_image_path}"

**Important Code Generation Guidelines:**
1. Generate ONLY the Scene class definition (including class declaration and imports)
2. Analyze the previous scene code to understand the final visual state
3. Recreate all mobjects from the previous scene's final state
4. Use proper timing for animations based on sentence timestamps
5. Ensure perfect visual continuity from the previous scene
6. Include proper error handling for mathematical operations
7. Ensure smooth transitions between animation phases
8. Generate complete, runnable code

Please generate the complete Python script for the current scene animation."""

        # Prepare message parts
        message_content = [
            {"type": "text", "text": user_prompt}
        ]
        
        # Add image if available
        image_part = self.prepare_image_for_api(problem_image_path)
        if image_part:
            message_content.append(image_part)
        
        try:
            print(f"Generating scene: {scene_id}")
            start_time = time.time()
            
            # Make the API call
            response = self.client.chat.completions.create(
                model="anthropic/claude-sonnet-4",  # Use sonnet-4 for subsequent scenes
                max_tokens=8000,
                temperature=0.1,
                extra_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_title
                },
                messages=[{"role": "user", "content": message_content}],
            )
            
            api_duration = time.time() - start_time
            print(f"Claude API call duration: {api_duration:.2f} seconds")
            
            # Extract and clean the generated code
            response_text = response.choices[0].message.content
            generated_code = self.extract_python_code(response_text)
            
            # Extract token usage
            usage = getattr(response, 'usage', None)
            if usage:
                prompt_tokens = getattr(usage, 'prompt_tokens', 0)
                completion_tokens = getattr(usage, 'completion_tokens', 0)
                total_tokens = getattr(usage, 'total_tokens', 0)
            else:
                prompt_tokens = completion_tokens = total_tokens = 0
            self.token_usage.append({
                'scene_id': scene_id,
                'input': prompt_tokens,
                'output': completion_tokens,
                'total': total_tokens
            })
            print(f"[Tokens] Scene {scene_id}: input={prompt_tokens}, output={completion_tokens}, total={total_tokens}")
            # Save the generated code
            output_path = self._save_scene_code(generated_code, scene_id, output_dir, response_text)
            
            return generated_code, output_path
            
        except Exception as e:
            print(f"Error generating subsequent scene: {e}")
            return None, None
    
    def _save_scene_code(self, generated_code, scene_id, output_dir, full_response):
        """Save the generated scene code to a file."""
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Determine file name
        scene_file_name = f"{scene_id}_claude_generated.py"
        output_file = output_path / scene_file_name
        
        # Save the generated code
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(generated_code)
        
        # Debug: Save full response if code is empty or suspiciously short
        if not generated_code.strip() or len(generated_code.strip()) < 20:
            print(f"[WARNING] Extracted code is empty or too short for {scene_id}! Saving full response for debugging.")
            debug_path = output_path / f"{scene_file_name}.raw_response.txt"
            with open(debug_path, "w", encoding="utf-8") as debug_f:
                debug_f.write(full_response)
            print(f"[DEBUG] Full Claude response saved to: {debug_path}")
        
        print(f"✓ Scene code saved to: {output_file}")
        return output_file
    
    def generate_animation_sequence(self, steps_data, problem_image_path, output_dir="/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Generated_Scenes_Both"):
        """
        Generate a complete sequence of animation scenes.
        """
        print(f"Starting animation sequence generation for {len(steps_data)} scenes...")
        generated_scenes = {}
        previous_scene_code = None
        total_api_time = 0.0

        # Generate the first scene
        i = 0
        step_json = steps_data[0]
        step_id = step_json.get('step_id', f'step_{i}')
        start_time = time.time()
        generated_code, output_path = self.generate_first_scene(
            step_json, problem_image_path, output_dir
        )
        api_time = time.time() - start_time
        total_api_time += api_time
        print(f"[Timing] Scene {step_id} API call time: {api_time:.2f} seconds")
        if generated_code and output_path:
            generated_scenes[step_id] = (generated_code, output_path)
            previous_scene_code = generated_code
            print(f"Scene ID: {step_id}")
            print(f"Duration: {self._calculate_duration(step_json)} seconds")
            print(f"Sentences: {len(step_json.get('sentences', []))}")
            print("---")
        else:
            print(f"\u2717 Failed to generate scene for: {step_id}")
            print(f"\nCompleted! Generated {len(generated_scenes)} scenes:")
            for step_id, (_, output_path) in generated_scenes.items():
                print(f"  - {step_id}: {output_path}")
            print(f"\nTotal API call time: {total_api_time:.2f} seconds")
            # Print total token usage
            total_input = sum(u['input'] for u in self.token_usage)
            total_output = sum(u['output'] for u in self.token_usage)
            total_tokens = sum(u['total'] for u in self.token_usage)
            print(f"\n[Token Usage] Total input tokens: {total_input}")
            print(f"[Token Usage] Total output tokens: {total_output}")
            print(f"[Token Usage] Total tokens: {total_tokens}")
            return generated_scenes

        # Generate the second scene if available
        if len(steps_data) > 1:
            i = 1
            step_json = steps_data[1]
            step_id = step_json.get('step_id', f'step_{i}')
            start_time = time.time()
            generated_code, output_path = self.generate_subsequent_scene(
                previous_scene_code, step_json, problem_image_path, output_dir
            )
            api_time = time.time() - start_time
            total_api_time += api_time
            print(f"[Timing] Scene {step_id} API call time: {api_time:.2f} seconds")
            if generated_code and output_path:
                generated_scenes[step_id] = (generated_code, output_path)
                previous_scene_code = generated_code
                print(f"Scene ID: {step_id}")
                print(f"Duration: {self._calculate_duration(step_json)} seconds")
                print(f"Sentences: {len(step_json.get('sentences', []))}")
                print("---")
            else:
                print(f"\u2717 Failed to generate scene for: {step_id}")

        print(f"\nCompleted! Generated {len(generated_scenes)} scenes:")
        for step_id, (_, output_path) in generated_scenes.items():
            print(f"  - {step_id}: {output_path}")
        print(f"\nTotal API call time: {total_api_time:.2f} seconds")
        # Print total token usage
        total_input = sum(u['input'] for u in self.token_usage)
        total_output = sum(u['output'] for u in self.token_usage)
        total_tokens = sum(u['total'] for u in self.token_usage)
        print(f"\n[Token Usage] Total input tokens: {total_input}")
        print(f"[Token Usage] Total output tokens: {total_output}")
        print(f"[Token Usage] Total tokens: {total_tokens}")
        return generated_scenes
    
    def _calculate_duration(self, step_json):
        """Calculate the duration of a step based on sentence timings."""
        sentences = step_json.get('sentences', [])
        if not sentences:
            return 10  # Default duration
        
        max_end_time = max(sentence.get('end', 0) for sentence in sentences)
        return max_end_time + 2  # Add 2 seconds buffer

def main():
    """
    Example usage of the enhanced Claude Animation Generator.
    """

    # Load steps_data from the JSON file
    with open("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/deconstruct_parallel.json", "r", encoding="utf-8") as f:
        steps_json = json.load(f)
    steps_data = steps_json["solution_steps"]

    problem_image_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_question.png"
    output_dir = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Generated_Scenes_Both"

    # Initialize the generator
    try:
        generator = ClaudeAnimationGenerator()
        
        # Generate all scenes in the sequence
        print(f"Starting generation of all {len(steps_data)} scenes...")
        generated_scenes = generator.generate_animation_sequence(
            steps_data, problem_image_path, output_dir
        )
        
        print(f"\n🎉 Successfully generated {len(generated_scenes)} scenes!")
        
        # Render all generated scenes using Manim
        print("\nRendering all generated scenes with Manim...")
        import subprocess
        import shlex
        from pathlib import Path
        all_rendered = True
        for step_id, (_, output_path) in generated_scenes.items():
            try:
                # Find the class name in the generated file (assume first class that inherits from Scene)
                class_name = None
                output_path_obj = Path(output_path).resolve()
                if not output_path_obj.exists():
                    print(f"[ERROR] File does not exist: {output_path_obj}. Skipping render.")
                    all_rendered = False
                    continue
                with open(output_path_obj, 'r', encoding='utf-8') as f:
                    for line in f:
                        match = re.search(r'class\s+(\w+)\s*\(Scene\)', line)
                        if match:
                            class_name = match.group(1)
                            break
                if not class_name:
                    print(f"[ERROR] Could not find a Scene class in {output_path_obj}. Skipping render.")
                    all_rendered = False
                    continue
                print(f"\n[Rendering] {output_path_obj} ({class_name})...")
                # Use shlex.quote to handle spaces and special characters in file names
                manim_cmd = ["manim", "-pql", str(output_path_obj), class_name]
                result = subprocess.run(manim_cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"[SUCCESS] Rendered {class_name} from {output_path_obj}")
                else:
                    print(f"[ERROR] Failed to render {class_name} from {output_path_obj}")
                    all_rendered = False
                    print("--- STDERR ---")
                    print(result.stderr)
                    print("--- STDOUT ---")
                    print(result.stdout)
                    # Rigorous error analysis
                    if 'ValueError' in result.stderr:
                        print("[ANALYSIS] ValueError detected. Check for invalid wait times, negative durations, or other parameter issues in the scene code.")
                    if 'NameError' in result.stderr:
                        print("[ANALYSIS] NameError detected. Check for missing variables or context in the generated code.")
                    if 'SyntaxError' in result.stderr:
                        print("[ANALYSIS] SyntaxError detected. The generated code may be malformed or incomplete.")
                    if 'ModuleNotFoundError' in result.stderr:
                        print("[ANALYSIS] ModuleNotFoundError detected. Ensure all dependencies are installed and import paths are correct.")
                    if 'TypeError' in result.stderr:
                        print("[ANALYSIS] TypeError detected. Check for incorrect function signatures or argument types in the generated code.")
                    if 'AttributeError' in result.stderr:
                        print("[ANALYSIS] AttributeError detected. Check for typos or missing attributes in the generated code.")
                    print("[ANALYSIS] For further debugging, review the full error output above.")
            except Exception as e:
                print(f"[EXCEPTION] Exception occurred while rendering {output_path_obj}: {e}")
                all_rendered = False
                import traceback
                traceback.print_exc()
        
        # Only concatenate if all scenes rendered successfully
        if all_rendered:
            print("\nConcatenating all rendered videos with ffmpeg...")
            video_paths = []
            for step_id, (_, output_path) in generated_scenes.items():
                # Find the output video file (assume 480p15 directory and class name as video name)
                output_path_obj = Path(output_path).resolve()
                class_name = None
                with open(output_path_obj, 'r', encoding='utf-8') as f:
                    for line in f:
                        match = re.search(r'class\s+(\w+)\s*\(Scene\)', line)
                        if match:
                            class_name = match.group(1)
                            break
                if not class_name:
                    continue
                # Construct the expected video path
                video_dir = Path("/Users/kairos/Desktop/Prompt Generation/media/videos")
                # Find the subdirectory that matches the scene name
                subdirs = list(video_dir.glob(f"*{step_id}*"))
                if not subdirs:
                    print(f"[WARNING] Could not find video directory for {step_id}. Skipping in concat.")
                    continue
                video_file = subdirs[0] / "480p15" / f"{class_name}.mp4"
                if not video_file.exists():
                    print(f"[WARNING] Could not find video file: {video_file}. Skipping in concat.")
                    continue
                video_paths.append(video_file)
            if video_paths:
                concat_list_path = Path(output_dir) / "concat_list.txt"
                with open(concat_list_path, 'w', encoding='utf-8') as f:
                    for vp in video_paths:
                        f.write(f"file '{vp}'\n")
                final_video_path = Path(output_dir) / "final_concatenated_scenes.mp4"
                ffmpeg_cmd = [
                    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_path), "-c", "copy", str(final_video_path)
                ]
                print(f"\n[FFMPEG] Concatenating videos into {final_video_path} ...")
                result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"[SUCCESS] Final concatenated video created at: {final_video_path}")
                else:
                    print(f"[ERROR] ffmpeg failed to concatenate videos.")
                    print("--- STDERR ---")
                    print(result.stderr)
                    print("--- STDOUT ---")
                    print(result.stdout)
            else:
                print("[WARNING] No video files found to concatenate.")
        else:
            print("[ERROR] Not all scenes were rendered successfully. Skipping concatenation phase.")
            
        # Commented out: Generate a summary report for now
        # summary_path = Path(output_dir) / "generation_summary.json"
        # summary = {
        #     "total_scenes": len(generated_scenes),
        #     "scenes": {
        #         step_id: {
        #             "output_path": str(output_path),
        #             "code_length": len(code)
        #         }
        #         for step_id, (code, output_path) in generated_scenes.items()
        #     },
        #     "generation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        # }
        # 
        # with open(summary_path, "w", encoding="utf-8") as f:
        #     json.dump(summary, f, indent=2, ensure_ascii=False)
        # 
        # print(f"📊 Generation summary saved to: {summary_path}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your CLAUDE_API_KEY environment variable")
        print("2. Ensure the .env file is in the correct location")
        print("3. Install required packages: pip install anthropic python-dotenv pillow")
        print("4. Verify your step data and image paths are correct")

if __name__ == "__main__":
    main()