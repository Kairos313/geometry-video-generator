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
TEST_SCENE_INDEX = 0  # Test the first scene (change this to test different scenes)
OUTPUT_DIR = "Geometry_v2/Test_Blueprint_Output_Claude"
MODEL_NAME = "claude-sonnet-4-20250514"

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# --- LOAD API KEY ---
load_dotenv(".env")
claude_api_key = os.getenv("CLAUDE_API_KEY")
if not claude_api_key:
    raise RuntimeError("CLAUDE_API_KEY not found in environment.")

# --- LOAD PROMPT ---
from orchestrator_prompts import Animator_Phase_1_Blueprint_Manim_Docs_v1 as BLUEPRINT_PROMPT

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

# --- MAIN TEST FUNCTION ---
def test_single_blueprint_generation_claude():
    if TEST_SCENE_INDEX >= len(steps):
        logger.error(f"Scene index {TEST_SCENE_INDEX} is out of range. Total scenes: {len(steps)}")
        return
    test_step = steps[TEST_SCENE_INDEX]
    scene_id = test_step.get('scene_id', f'scene_{TEST_SCENE_INDEX}')
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"test_scene_{TEST_SCENE_INDEX}_{scene_id}.json"

    # Prepare prompt
    single_scene_prompt = f"""{BLUEPRINT_PROMPT}\n\n**Single Scene Blueprint Generation**\n- Generate a self-contained blueprint JSON for the following solution step.\n- Use the style config provided below.\n\n**Style Config JSON:**\n```json\n{json.dumps(style_config, ensure_ascii=False, indent=2)}\n```\n\n**Solution Step:**\n```json\n{json.dumps(test_step, ensure_ascii=False, indent=2)}\n```\n\n**Instructions:**\n- Output a single blueprint JSON object for this scene.\n- The blueprint should be self-contained and renderable independently.\n"""

    print(f"\n=== CLAUDE SONNET API TEST: Scene {TEST_SCENE_INDEX} ({scene_id}) ===")
    print(f"Prompt length: {len(single_scene_prompt)} characters")

    # API call
    client = anthropic.Anthropic(api_key=claude_api_key)
    start = time.time()
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            temperature=0.4,
            messages=[{"role": "user", "content": single_scene_prompt}]
        )
        api_time = time.time() - start
        response_text = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
        print(f"API call time: {api_time:.2f} seconds")
        # Extract JSON
        blueprint = extract_json_object(response_text)
        if blueprint:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(blueprint, f, indent=2, ensure_ascii=False)
            print(f"✅ Blueprint saved: {out_path}")
            print(f"Number of Mobjects: {len(blueprint.get('mobjects', []))}")
            print(f"Number of Animation Steps: {len(blueprint.get('animation_flow', []))}")
        else:
            print(f"❌ Failed to extract blueprint JSON. See logs for details.")
            raw_path = output_dir / f"test_scene_{TEST_SCENE_INDEX}_{scene_id}_raw.txt"
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(response_text)
            print(f"Raw response saved to: {raw_path}")
    except Exception as e:
        print(f"❌ Claude Sonnet API call failed: {e}")
        logger.error(f"Claude Sonnet API call failed: {e}")

if __name__ == "__main__":
    test_single_blueprint_generation_claude() 