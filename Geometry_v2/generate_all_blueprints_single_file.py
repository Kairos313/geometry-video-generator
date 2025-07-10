import json
import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from typing import Dict, Any, Optional

# Anthropic Claude Sonnet
import anthropic

# --- CONFIGURATION ---
INPUT_PATH = "Geometry_v2/deconstruct_parallel.json"
STYLE_PATH = "Geometry_v2/geo_v2_style.json"
IMAGE_PATH = "Geometry_v2/math_question.png"  # Set to None if not using image
OUTPUT_DIR = "Geometry_v2/Test_Blueprint_Batch"
MODEL_NAME = "claude-sonnet-4-20250514"
DELAY_BETWEEN_CALLS = 0.5  # seconds

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# --- LOAD API KEY ---
load_dotenv(".env")
claude_api_key = os.getenv("CLAUDE_API_KEY")
if not claude_api_key:
    raise RuntimeError("CLAUDE_API_KEY not found in environment.")

# --- LOAD PROMPT ---
from orchestrator_prompts import Animator_Phase_1_Blueprint_Manim_Docs_v2 as BLUEPRINT_PROMPT

# --- LOAD INPUTS ---
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_image(image_path):
    if not image_path:
        return None
    img_path = Path(image_path)
    if not img_path.exists():
        logger.warning(f"Image not found: {image_path}")
        return None
    return Image.open(img_path)

input_data = load_json(INPUT_PATH)
steps = input_data.get('solution_steps', [])
if not steps:
    raise ValueError("No solution_steps found in input file.")

style_config = load_json(STYLE_PATH)
image_obj = load_image(IMAGE_PATH)

# --- EXTRACT JSON ---
def extract_json_object(text):
    import re
    text = text.strip()
    if text.startswith('```json'):
        text = text[len('```json'):].strip()
    if text.startswith('```'):
        text = text[len('```'):].strip()
    if text.endswith('```'):
        text = text[:-3].strip()
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except Exception as e:
            logger.error(f"Primary extraction failed: {e}")
    patterns = [
        r"```json\s*(\{.*?\})\s*```",
        r"```\s*(\{.*?\})\s*```",
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

# --- MAIN FUNCTION ---
def generate_all_blueprints_claude():
    output_file = "Geometry_v2/all_blueprints_combined.json"
    client = anthropic.Anthropic(api_key=claude_api_key)
    total = len(steps)

    # Prepare a single prompt for all scenes (without style config)
    all_scenes_prompt = f"""{BLUEPRINT_PROMPT}

**Batch Blueprint Generation**
- For each solution step in the list below, generate a self-contained blueprint JSON object.
- Return a JSON array (list) of blueprints, one per scene, in the same order as the input.

**Solution Steps List:**
```json
{json.dumps(steps, ensure_ascii=False, indent=2)}
```

**Instructions:**
- Output a single JSON array (list) of blueprint objects, one for each scene.
- Each blueprint should be self-contained and renderable independently.
"""
    print(f"\n=== CLAUDE SONNET API: Batch Blueprint Generation for {total} scenes ===")
    print(f"Prompt length: {len(all_scenes_prompt)} characters")
    # Prepare message parts
    claude_message_parts = [{"type": "text", "text": all_scenes_prompt}]
    if IMAGE_PATH and Path(IMAGE_PATH).exists():
        with open(IMAGE_PATH, "rb") as img_file:
            image_bytes = img_file.read()
        ext = Path(IMAGE_PATH).suffix.lower()
        media_type = "image/png" if ext == ".png" else "image/jpeg"
        import base64
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
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=8000,
            temperature=0.4,
            messages=[{"role": "user", "content": claude_message_parts}]
        )
        api_time = time.time() - start
        response_text = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
        print(f"API call time: {api_time:.2f} seconds")
        # Expecting a JSON array/list of blueprints
        try:
            all_blueprints = json.loads(response_text)
        except Exception:
            # Try to extract JSON array from markdown/code block
            import re
            match = re.search(r'\[\s*\{.*?\}\s*\](?=\s*$)', response_text, re.DOTALL)
            if match:
                all_blueprints = json.loads(match.group(0))
            else:
                print("❌ Failed to extract blueprint JSON array. See logs for details.")
                raw_path = "claude_batch_raw_response.txt"
                with open(raw_path, "w", encoding="utf-8") as f:
                    f.write(response_text)
                print(f"Raw response saved to: {raw_path}")
                return
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_blueprints, f, indent=2, ensure_ascii=False)
        print(f"\nAll scene blueprints saved to: {output_file}\n")
    except Exception as e:
        print(f"❌ Claude Sonnet API call failed: {e}")
        logger.error(f"Claude Sonnet API call failed: {e}")

if __name__ == "__main__":
    generate_all_blueprints_claude() 