# DeepSeek version of the ClaudeAnimationGenerator script
# Requirements: requests, python-dotenv, pillow
# Set your DeepSeek API key in the DEEPSEEK_API_KEY environment variable

import json
import os
import sys
import time
import base64
import re
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
import requests

# Add the prompt directory to the path to import the prompts
sys.path.append('/Users/kairos/Desktop/Prompt Generation/Geometry_v2')
from final_animation_prompt import Final_Animation_Scene_1_v1, Final_Animation_Other_Scenes_v1

class DeepSeekAnimationGenerator:
    def __init__(self, api_key=None, model_name="deepseek-reasoner"):
        """
        Initialize the DeepSeek API client.
        Args:
            api_key (str, optional): DeepSeek API key. If not provided, will look for DEEPSEEK_API_KEY environment variable.
            model_name (str): DeepSeek model to use
        """
        load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or DEEPSEEK_API_KEY environment variable")
        self.model = model_name
        self.system_prompt = "You are an expert Manim programmer specializing in educational animations in the style of 3Blue1Brown."
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

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
        # DeepSeek API may not support image input; skip for now
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

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 8000,
            "temperature": 0.1
        }
        try:
            print(f"Generating first scene: {scene_id}")
            start_time = time.time()
            response = requests.post(self.api_url, headers=headers, json=payload)
            api_duration = time.time() - start_time
            print(f"DeepSeek API call duration: {api_duration:.2f} seconds")
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                return None, None
            response_json = response.json()
            response_text = response_json['choices'][0]['message']['content']
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

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 8000,
            "temperature": 0.1
        }
        try:
            print(f"Generating scene: {scene_id}")
            start_time = time.time()
            response = requests.post(self.api_url, headers=headers, json=payload)
            api_duration = time.time() - start_time
            print(f"DeepSeek API call duration: {api_duration:.2f} seconds")
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                return None, None
            response_json = response.json()
            response_text = response_json['choices'][0]['message']['content']
            generated_code = self.extract_python_code(response_text)
            output_path = self._save_scene_code(generated_code, scene_id, output_dir, response_text)
            return generated_code, output_path
        except Exception as e:
            print(f"Error generating subsequent scene: {e}")
            return None, None

    def _save_scene_code(self, generated_code, scene_id, output_dir, full_response):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        scene_file_name = f"{scene_id}_deepseek_generated.py"
        output_file = output_path / scene_file_name
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(generated_code)
        if not generated_code.strip():
            print(f"[WARNING] Extracted code is empty for {scene_id}! Saving full response for debugging.")
            debug_path = output_path / f"{scene_file_name}.raw_response.txt"
            with open(debug_path, "w", encoding="utf-8") as debug_f:
                debug_f.write(full_response)
            print(f"[DEBUG] Full DeepSeek response saved to: {debug_path}")
        print(f"✓ Scene code saved to: {output_file}")
        return output_file

def main():
    """
    Example usage of the DeepSeek Animation Generator.
    """
    with open("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/deconstruct_parallel.json", "r", encoding="utf-8") as f:
        steps_json = json.load(f)
    steps_data = steps_json["solution_steps"]
    problem_image_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_question.png"
    output_dir = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Generated_Scenes_Deepseek"
    try:
        generator = DeepSeekAnimationGenerator()
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
        print("1. Check your DEEPSEEK_API_KEY environment variable")
        print("2. Ensure the .env file is in the correct location")
        print("3. Install required packages: pip install requests python-dotenv pillow")
        print("4. Verify your step data and image paths are correct")

if __name__ == "__main__":
    main() 