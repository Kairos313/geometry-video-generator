import json
import os
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import time
import anthropic
import base64

# --- CONFIGURATION ---
BLUEPRINT_PATH = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Test_Blueprint_Batch/scene_5_scene_5.json"  # Use Claude batch-generated blueprint for scene 5
STYLE_PATH = "Geometry_v2/geo_v2_style.json"
IMAGE_PATH = "Geometry_v2/math_question.png"  # Set to None if not using image
PROMPT_PATH = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/orchestrator_prompts.py"
MODEL_NAME = "claude-sonnet-4-20250514"

# --- LOAD API KEY ---
load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")
api_key = os.getenv("CLAUDE_API_KEY")
if not api_key:
    raise RuntimeError("CLAUDE_API_KEY not found in environment.")

# --- LOAD PROMPT ---
import sys
sys.path.insert(0, str(Path(PROMPT_PATH).parent.resolve()))
from orchestrator_prompts import Animator_Phase_2_Code_Generation_Claude_v3 as CODE_GEN_PROMPT

# --- LOAD BLUEPRINT ---
with open(BLUEPRINT_PATH, "r", encoding="utf-8") as f:
    blueprint = json.load(f)

# --- LOAD STYLE CONFIG ---
with open(STYLE_PATH, "r", encoding="utf-8") as f:
    style_config = json.load(f)

# --- LOAD IMAGE (OPTIONAL) ---
def load_image(image_path):
    if not image_path:
        return None
    img_path = Path(image_path)
    if not img_path.exists():
        print(f"Image not found: {image_path}")
        return None
    return Image.open(img_path)

image_obj = load_image(IMAGE_PATH)

# --- PREPARE SCENE DATA ---
scene_id = blueprint.get("scene_id", "scene")
duration = blueprint.get("duration_scene_seconds", 10)

# Create scene_data structure expected by the new prompt
scene_data = {
    "scene_id": scene_id,
    "duration_seconds": duration,
    "audio_file_path": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_deduce_isosceles_triangle_scene.mp3",
    "sentence_timestamps": blueprint.get("sentence_timestamps", []),
    "initial_mobjects": blueprint.get("initial_mobjects", []),
    "mobjects": blueprint.get("mobjects", []),
    "animation_flow": blueprint.get("animation_flow", [])
}

# --- PREPARE PROMPT ---
user_prompt = f"""{CODE_GEN_PROMPT}

**Enhanced Generation Context:**
- Scene ID: {scene_id}
- Duration: {duration} seconds
- Audio Available: {'Yes' if scene_data.get('audio_file_path') else 'No'}
- Render Quality: medium_quality

**Scene Data Structure:**
The scene_data variable will contain:
```json
{json.dumps(scene_data, ensure_ascii=False, indent=2)}
```

**Important Code Generation Guidelines:**
1. Generate ONLY the Scene class definition (including class declaration)
2. Use the scene_data variable directly as it is already defined
3. DO NOT include import statements or json.loads() calls
4. Use proper timing for animations based on sentence_timestamps
5. Ensure all animations fit within the specified duration
6. Handle cases where audio might be missing gracefully
7. Include proper error handling for mathematical operations
8. Ensure smooth transitions between animation phases
9. Reference Manim documentation for correct syntax and parameters

Please generate the complete Scene class that will work with the provided scene_data variable."""

# --- CLAUDE API CALL WITH IMAGE ---
client = anthropic.Anthropic(api_key=api_key)
claude_system_prompt = "You are a helpful assistant that writes Manim code for mathematical animations."

# Prepare the message parts
claude_message_parts = [
    {"type": "text", "text": user_prompt}
]

# Attach the image if it exists
if IMAGE_PATH and Path(IMAGE_PATH).exists():
    with open(IMAGE_PATH, "rb") as img_file:
        image_bytes = img_file.read()
    ext = Path(IMAGE_PATH).suffix.lower()
    if ext == ".jpg" or ext == ".jpeg":
        media_type = "image/jpeg"
    else:
        media_type = "image/png"
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    claude_message_parts.append({
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": image_b64
        }
    })

start = time.time()
response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=8000,  # Increased for code generation
    system=claude_system_prompt,
    messages=[
        {
            "role": "user",
            "content": claude_message_parts
        }
    ]
)
api_call_duration = time.time() - start
print(f"Claude API call duration: {api_call_duration:.2f} seconds")
response_text = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])

# --- EXTRACT PYTHON CODE ---
import re
def extract_python_code(text):
    code_patterns = [
        r"```python\s*(.*?)\s*```",
        r"```\s*(.*?)\s*```",
        r"class\s+\w+\s*\(Scene\):\s*(.*?)(?=\n\s*(?:class|def|#|$)|\Z)",
    ]
    for pattern in code_patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
    return text  # fallback

scene_class_code = extract_python_code(response_text)

# Remove Markdown code block markers if present
scene_class_code = re.sub(r'```(?:python)?', '', scene_class_code)
scene_class_code = re.sub(r'```', '', scene_class_code)
scene_class_code = scene_class_code.strip()

# Remove any lines that try to parse or load JSON (the new prompt shouldn't generate these)
scene_class_code = re.sub(r'.*json\.loads\(.*?\).*\n', '', scene_class_code)
scene_class_code = re.sub(r'.*import json.*\n', '', scene_class_code)
scene_class_code = re.sub(r'.*from manim import.*\n', '', scene_class_code)

# Write the output file with only the generated code
output_dir = Path("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Manim Code")
output_dir.mkdir(parents=True, exist_ok=True)
scene_file_name = Path(BLUEPRINT_PATH).stem + "_claude_v3.py"
output_path = output_dir / scene_file_name

# Store only the API response code
with open(output_path, "w", encoding="utf-8") as f:
    f.write(scene_class_code)

# --- DEBUG: Print and save full response if code is empty ---
if not scene_class_code.strip():
    print("[WARNING] Extracted code is empty! Printing full Claude response for debugging:\n")
    print(response_text)
    debug_path = output_dir / (scene_file_name + ".raw_response.txt")
    with open(debug_path, "w", encoding="utf-8") as debug_f:
        debug_f.write(response_text)
    print(f"[DEBUG] Full Claude response saved to: {debug_path}")

print(f"\nScene code written to: {output_path}")
print(f"Scene ID: {scene_id}")
print(f"Duration: {duration} seconds")
print(f"Mobjects count: {len(scene_data.get('mobjects', []))}")
print(f"Animation groups: {len(scene_data.get('animation_flow', []))}")