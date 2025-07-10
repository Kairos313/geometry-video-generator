import json
import os
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import time
import logging
import sys
import google.generativeai as genai
import concurrent.futures

# --- CONFIGURATION ---
INPUT_PATH = "Geometry_v2/deconstruct_parallel.json"  # Input JSON with all solution steps
STYLE_PATH = "Geometry_v2/geo_v2_style.json"
IMAGE_PATH = "Geometry_v2/math_question.png"  # Set to None if not using image
PROMPT_PATH = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/orchestrator_prompts.py"
BLUEPRINT_DIR = "Geometry_v2/Blueprint_Batch_Gemini"
MODEL_NAME = "gemini-2.5-flash"

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# --- LOAD API KEY ---
load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise RuntimeError("GOOGLE_API_KEY not found in environment.")
genai.configure(api_key=google_api_key)

# --- LOAD PROMPT ---
sys.path.insert(0, str(Path(PROMPT_PATH).parent.resolve()))
from orchestrator_prompts import Animator_Phase_1_Blueprint_Claude_v1 as BLUEPRINT_PROMPT

# --- LOAD INPUTS ---
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    input_data = json.load(f)
steps = input_data.get('solution_steps', [])
if not steps:
    raise ValueError("No solution_steps found in input file.")

with open(STYLE_PATH, "r", encoding="utf-8") as f:
    style_config = json.load(f)

def load_image(image_path):
    if not image_path:
        return None
    img_path = Path(image_path)
    if not img_path.exists():
        logger.warning(f"Image not found: {image_path}")
        return None
    return Image.open(img_path)

image_obj = load_image(IMAGE_PATH)

# --- EXTRACT JSON ---
import re
def extract_json_object(text):
    # Debug: log preview of the response
    logger.debug(f"Raw response preview (first 200): {text[:200]}")
    logger.debug(f"Raw response preview (last 200): {text[-200:]}")
    # Remove Markdown code block markers if present
    text = text.strip()
    if text.startswith('```json'):
        text = text[len('```json'):].strip()
    if text.startswith('```'):
        text = text[len('```'):].strip()
    if text.endswith('```'):
        text = text[:-3].strip()
    logger.debug(f"Stripped response preview (first 200): {text[:200]}")
    logger.debug(f"Stripped response preview (last 200): {text[-200:]}")
    # Try greedy extraction between first '{' and last '}'
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except Exception as e:
            logger.error(f"Primary extraction failed: {e}")
    # Fallback to regex patterns
    patterns = [
        r"```json\\s*(\{.*?\})\\s*```",
        r"```\\s*(\{.*?\})\\s*```",
        r"(\{[^{}]*\{.*?\}[^{}]*\})",
        r"(\{.*?\})"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception as e:
                logger.error(f"Regex extraction failed: {e}")
                continue
    logger.warning("Could not extract JSON from response. Preview: %s", text[:200])
    return None

# --- GEMINI API CALL PER SCENE ---
model = genai.GenerativeModel(MODEL_NAME)
output_dir = Path(BLUEPRINT_DIR)
output_dir.mkdir(parents=True, exist_ok=True)

def try_load_json_from_file(raw_path):
    try:
        with open(raw_path, 'r', encoding='utf-8') as f:
            raw = f.read().strip()
        # Strip code block markers
        if raw.startswith('```json'):
            raw = raw[len('```json'):].strip()
        if raw.startswith('```'):
            raw = raw[len('```'):].strip()
        if raw.endswith('```'):
            raw = raw[:-3].strip()
        return json.loads(raw)
    except Exception as e:
        logger.error(f"Fallback file JSON load failed: {e}")
        return None

existing_files = set(p.stem for p in output_dir.glob("*.json"))
scenes_to_process = []
for i, step in enumerate(steps):
    scene_id = step.get('scene_id', f'scene_{i}')
    file_stem = f"{i:02d}_{scene_id}"
    if file_stem not in existing_files:
        scenes_to_process.append((i, step))
    else:
        logger.info(f"Skipping scene {i} ({scene_id}) - already exists.")

if not scenes_to_process:
    print("All blueprints already exist. Nothing to retry.")
    exit(0)

def process_scene(i, step):
    scene_id = step.get('scene_id', f'scene_{i}')
    single_scene_prompt = f"""{BLUEPRINT_PROMPT}

**Single Scene Blueprint Generation**
- Generate a self-contained blueprint JSON for the following solution step.
- Use the style config provided below.

**Style Config JSON:**
```json
{json.dumps(style_config, ensure_ascii=False, indent=2)}
```

**Solution Step:**
```json
{json.dumps(step, ensure_ascii=False, indent=2)}
```

**Instructions:**
- Output a single blueprint JSON object for this scene.
- The blueprint should be self-contained and renderable independently.
"""
    if image_obj is not None:
        gemini_messages = [
            {"role": "user", "parts": [single_scene_prompt, image_obj]}
        ]
    else:
        gemini_messages = [
            {"role": "user", "parts": [single_scene_prompt]}
        ]
    start = time.time()
    try:
        response = model.generate_content(gemini_messages)
        api_call_duration = time.time() - start
        response_text = response.text if hasattr(response, 'text') else str(response)
        logger.info(f"Gemini API call for scene {i} ({scene_id}) duration: {api_call_duration:.2f} seconds")
        parsed = extract_json_object(response_text)
        if not parsed:
            # Save the full response for debugging
            raw_path = f'gemini_scene_{i}_raw_response.txt'
            with open(raw_path, 'w', encoding='utf-8') as f:
                f.write(response_text)
            logger.error(f"Could not extract blueprint JSON for scene {i} ({scene_id}). Full response saved to {raw_path}.")
            # Fallback: try to load JSON directly from file
            parsed = try_load_json_from_file(raw_path)
            if parsed:
                out_path = output_dir / f"{i:02d}_{scene_id}.json"
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(parsed, f, indent=2, ensure_ascii=False)
                logger.info(f"[Fallback] Saved blueprint {i}: {out_path}")
                return True
            return False
        out_path = output_dir / f"{i:02d}_{scene_id}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved blueprint {i}: {out_path}")
        return True
    except Exception as e:
        logger.error(f"Error processing scene {i} ({scene_id}): {e}")
        return False

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_scene, i, step) for i, step in scenes_to_process]
    for future in concurrent.futures.as_completed(futures):
        _ = future.result()

print(f"\nAll scene blueprints generated and saved to: {output_dir}\n") 