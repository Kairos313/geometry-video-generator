# Gemini 2.5 Pro version of the ClaudeAnimationGenerator script
# Requirements: google-generativeai (pip install google-generativeai)
# Set your Gemini API key in the GOOGLE_API_KEY environment variable

import json
import os
import sys
import time
import base64
import re
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Add the prompt directory to the path to import the prompts
sys.path.append('/Users/kairos/Desktop/Prompt Generation/Geometry_v2')
from final_animation_prompt import Final_Animation_Scene_1_v1, Final_Animation_Other_Scenes_v1

class GeminiAnimationGenerator:
    def __init__(self, api_key=None, model_name="gemini-2.5-pro"):
        """
        Initialize the Gemini API client.
        Args:
            api_key (str, optional): Gemini API key. If not provided, will look for GEMINI_API_KEY environment variable.
            model_name (str): Gemini model to use
        """
        load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or GOOGLE_API_KEY environment variable")
        genai.configure(api_key=self.api_key)
        self.model = model_name
        self.system_prompt = "You are an expert Manim programmer specializing in educational animations in the style of 3Blue1Brown."

    def load_image(self, image_path):
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
        if not image_path or not Path(image_path).exists():
            return None
        try:
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()
            return {
                "mime_type": "image/png" if image_path.lower().endswith(".png") else "image/jpeg",
                "data": image_bytes
            }
        except Exception as e:
            print(f"Error preparing image for API: {e}")
            return None

    def extract_python_code(self, text):
        code_patterns = [
            r"```python\s*(.*?)\s*```",
            r"```\s*(.*?)\s*```",
            r"class\s+\w+\s*\(Scene\):\s*(.*?)(?=\n\s*(?:class|def|#|$)|\Z)",
        ]
        for pattern in code_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                code = match.group(1).strip()
                code = re.sub(r'```(?:python)?', '', code)
                code = re.sub(r'```', '', code)
                return code.strip()
        return text.strip()

    def generate_first_scene(self, first_step_json, problem_image_path, output_dir="generated_scenes"):
        scene_id = first_step_json["step_id"]
        user_prompt = f"""{Final_Animation_Scene_1_v1}

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

        contents = [user_prompt]
        image_part = self.prepare_image_for_api(problem_image_path)
        if image_part:
            contents.append(image_part)
        try:
            print(f"Generating first scene: {scene_id}")
            start_time = time.time()
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(contents)
            api_duration = time.time() - start_time
            print(f"Gemini API call duration: {api_duration:.2f} seconds")
            response_text = response.text if hasattr(response, 'text') else str(response)
            generated_code = self.extract_python_code(response_text)
            output_path = self._save_scene_code(generated_code, scene_id, output_dir, response_text)
            return generated_code, output_path
        except Exception as e:
            print(f"Error generating first scene: {e}")
            return None, None

    def generate_subsequent_scene(self, previous_scene_code, current_step_json, problem_image_path, output_dir="generated_scenes"):
        scene_id = current_step_json["step_id"]
        user_prompt = f"""{Final_Animation_Other_Scenes_v1}

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

        contents = [user_prompt]
        image_part = self.prepare_image_for_api(problem_image_path)
        if image_part:
            contents.append(image_part)
        try:
            print(f"Generating scene: {scene_id}")
            start_time = time.time()
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(contents)
            api_duration = time.time() - start_time
            print(f"Gemini API call duration: {api_duration:.2f} seconds")
            response_text = response.text if hasattr(response, 'text') else str(response)
            generated_code = self.extract_python_code(response_text)
            output_path = self._save_scene_code(generated_code, scene_id, output_dir, response_text)
            return generated_code, output_path
        except Exception as e:
            print(f"Error generating subsequent scene: {e}")
            return None, None

    def _save_scene_code(self, generated_code, scene_id, output_dir, full_response):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        scene_file_name = f"{scene_id}_gemini_generated.py"
        output_file = output_path / scene_file_name
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(generated_code)
        if not generated_code.strip():
            print(f"[WARNING] Extracted code is empty for {scene_id}! Saving full response for debugging.")
            debug_path = output_path / f"{scene_file_name}.raw_response.txt"
            with open(debug_path, "w", encoding="utf-8") as debug_f:
                debug_f.write(full_response)
            print(f"[DEBUG] Full Gemini response saved to: {debug_path}")
        print(f"✓ Scene code saved to: {output_file}")
        return output_file

def main():
    """
    Example usage of the Gemini Animation Generator.
    """
    with open("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/deconstruct_parallel.json", "r", encoding="utf-8") as f:
        steps_json = json.load(f)
    steps_data = steps_json["solution_steps"]
    problem_image_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_question.png"
    output_dir = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Generated_Scenes_Gemini"
    try:
        generator = GeminiAnimationGenerator()
        generated_scenes = {}
        generated_code_1, output_path_1 = generator.generate_first_scene(
            steps_data[0], problem_image_path, output_dir
        )
        if generated_code_1 and output_path_1:
            generated_scenes[steps_data[0]["step_id"]] = (generated_code_1, output_path_1)
        generated_code_2, output_path_2 = generator.generate_subsequent_scene(
            generated_code_1, steps_data[1], problem_image_path, output_dir
        )
        if generated_code_2 and output_path_2:
            generated_scenes[steps_data[1]["step_id"]] = (generated_code_2, output_path_2)
        print(f"\n🎉 Successfully generated {len(generated_scenes)} scenes!")
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your GOOGLE_API_KEY environment variable")
        print("2. Ensure the .env file is in the correct location")
        print("3. Install required packages: pip install google-generativeai python-dotenv pillow")
        print("4. Verify your step data and image paths are correct")

if __name__ == "__main__":
    main()
