import anthropic
import json
import os
import sys
import time
import base64
import re
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv

# Add the prompt directory to the path to import the prompts
sys.path.append('/Users/kairos/Desktop/Prompt Generation/Geometry_v2')
from final_animation_prompt import Final_Animation_Scene_1_v1, Final_Animation_Other_Scenes_v1

class ClaudeAnimationGenerator:
    def __init__(self, api_key=None, model_name="claude-sonnet-4-20250514"):
        """
        Initialize the Claude API client.
        
        Args:
            api_key (str, optional): Anthropic API key. If not provided, 
                                   will look for CLAUDE_API_KEY environment variable.
            model_name (str): Claude model to use
        """
        # Load environment variables
        load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")
        
        self.api_key = api_key or os.getenv('CLAUDE_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or CLAUDE_API_KEY/ANTHROPIC_API_KEY environment variable")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model_name
        self.system_prompt = "You are an expert Manim programmer specializing in educational animations in the style of 3Blue1Brown."
    
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
        """Prepare image data for Claude API call."""
        if not image_path or not Path(image_path).exists():
            return None
        
        try:
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()
            
            ext = Path(image_path).suffix.lower()
            media_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
            
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_b64
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
    
    def generate_first_scene(self, first_step_json, problem_image_path, output_dir="generated_scenes"):
        """
        Generate the first scene animation using Claude API.
        
        Args:
            first_step_json (dict): JSON object containing step_id and sentences
            problem_image_path (str): Path to the reference image
            output_dir (str): Directory to save generated scenes
            
        Returns:
            tuple: (generated_code, output_path)
        """
        # Use the correct scene name from the step JSON
        scene_id = first_step_json["step_id"]
        # Prepare the enhanced prompt
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

        # Prepare message parts
        message_parts = [{"type": "text", "text": user_prompt}]
        
        # Add image if available
        image_part = self.prepare_image_for_api(problem_image_path)
        if image_part:
            message_parts.append(image_part)
        
        try:
            print(f"Generating first scene: {scene_id}")
            start_time = time.time()
            
            # Make the API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=0.1,
                system=self.system_prompt,
                messages=[{"role": "user", "content": message_parts}]
            )
            
            api_duration = time.time() - start_time
            print(f"Claude API call duration: {api_duration:.2f} seconds")
            
            # Extract and clean the generated code
            response_text = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
            generated_code = self.extract_python_code(response_text)
            
            # Save the generated code
            output_path = self._save_scene_code(generated_code, scene_id, output_dir, response_text)
            
            return generated_code, output_path
            
        except Exception as e:
            print(f"Error generating first scene: {e}")
            return None, None
    
    def generate_subsequent_scene(self, previous_scene_code, current_step_json, problem_image_path, output_dir="generated_scenes"):
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

        # Prepare message parts
        message_parts = [{"type": "text", "text": user_prompt}]
        
        # Add image if available
        image_part = self.prepare_image_for_api(problem_image_path)
        if image_part:
            message_parts.append(image_part)
        
        try:
            print(f"Generating scene: {scene_id}")
            start_time = time.time()
            
            # Make the API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=0.1,
                system=self.system_prompt,
                messages=[{"role": "user", "content": message_parts}]
            )
            
            api_duration = time.time() - start_time
            print(f"Claude API call duration: {api_duration:.2f} seconds")
            
            # Extract and clean the generated code
            response_text = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
            generated_code = self.extract_python_code(response_text)
            
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
        
        # Debug: Save full response if code is empty
        if not generated_code.strip():
            print(f"[WARNING] Extracted code is empty for {scene_id}! Saving full response for debugging.")
            debug_path = output_path / f"{scene_file_name}.raw_response.txt"
            with open(debug_path, "w", encoding="utf-8") as debug_f:
                debug_f.write(full_response)
            print(f"[DEBUG] Full Claude response saved to: {debug_path}")
        
        print(f"✓ Scene code saved to: {output_file}")
        return output_file
    
    def generate_animation_sequence(self, steps_data, problem_image_path, output_dir="generated_scenes"):
        """
        Generate a complete sequence of animation scenes.
        
        Args:
            steps_data (list): List of step JSON objects
            problem_image_path (str): Path to the reference image
            output_dir (str): Directory to save the generated scenes
            
        Returns:
            dict: Dictionary mapping step_id to (generated_code, output_path)
        """
        print(f"Starting animation sequence generation for {len(steps_data)} scenes...")
        
        generated_scenes = {}
        previous_scene_code = None

        for i, step_json in enumerate(steps_data):
            step_id = step_json.get('step_id', f'step_{i}')
            
            if i == 0:
                # Generate first scene
                generated_code, output_path = self.generate_first_scene(
                    step_json, problem_image_path, output_dir
                )
            else:
                # Generate subsequent scene
                generated_code, output_path = self.generate_subsequent_scene(
                    previous_scene_code, step_json, problem_image_path, output_dir
                )
            
            if generated_code and output_path:
                generated_scenes[step_id] = (generated_code, output_path)
                previous_scene_code = generated_code
                
                # Print scene info
                print(f"Scene ID: {step_id}")
                print(f"Duration: {self._calculate_duration(step_json)} seconds")
                print(f"Sentences: {len(step_json.get('sentences', []))}")
                print("---")
            else:
                print(f"✗ Failed to generate scene for: {step_id}")
                break
        
        print(f"\nCompleted! Generated {len(generated_scenes)} scenes:")
        for step_id, (_, output_path) in generated_scenes.items():
            print(f"  - {step_id}: {output_path}")
        
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
    output_dir = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Generated_Scenes"

    # Initialize the generator
    try:
        generator = ClaudeAnimationGenerator()
        
        # Only generate the first two scenes for testing
        generated_scenes = {}
        # Scene 1
        generated_code_1, output_path_1 = generator.generate_first_scene(
            steps_data[0], problem_image_path, output_dir
        )
        if generated_code_1 and output_path_1:
            generated_scenes[steps_data[0]["step_id"]] = (generated_code_1, output_path_1)
        # Scene 2
        generated_code_2, output_path_2 = generator.generate_subsequent_scene(
            generated_code_1, steps_data[1], problem_image_path, output_dir
        )
        if generated_code_2 and output_path_2:
            generated_scenes[steps_data[1]["step_id"]] = (generated_code_2, output_path_2)
        
        print(f"\n🎉 Successfully generated {len(generated_scenes)} scenes!")
        
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