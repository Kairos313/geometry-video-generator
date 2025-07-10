import json
import os
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import time
import logging
import sys
import google.generativeai as genai
from google.generativeai.types import content_types
import concurrent.futures
import re

# --- NEW DEPENDENCY: Tool for searching the web ---
# Make sure to install it first: pip install duckduckgo-search
from duckduckgo_search import DDGS

# --- CONFIGURATION ---
# Adjust these paths to match your project structure
INPUT_PATH = "Geometry_v2/deconstruct_parallel.json"
STYLE_PATH = "Geometry_v2/geo_v2_style.json"
IMAGE_PATH = "Geometry_v2/math_question.png" # Set to None if not using an image
BLUEPRINT_DIR = "Geometry_v2/Blueprint_Batch_Gemini_Tool_Calling"
MODEL_NAME = "gemini-2.5-flash" # Recommended for tool calling

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# --- LOAD API KEY ---
# Ensure your .env file is in the correct location or provide the full path
load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise RuntimeError("GOOGLE_API_KEY not found in environment. Please check your .env file.")
genai.configure(api_key=google_api_key)


# --- 1. TOOL DEFINITION ---
# This is the function the Gemini model will be able to call.
# The docstring is CRITICAL as it's how the model knows what the tool does.
def search_manim_docs(query: str) -> str:
    """
    Searches the official Manim Community documentation (docs.manim.community)
    to find information about functions, classes, properties, or animation techniques.

    Args:
        query: The specific search query (e.g., "fade in animation", "Line properties", "TransformMatchingTex examples").

    Returns:
        A string containing the top search results, including titles, links, and snippets.
        Returns 'No results found.' if the search yields no results.
    """
    logger.info(f"Executing tool 'search_manim_docs' with query: '{query}'")
    site_query = f"site:docs.manim.community {query}"
    try:
        with DDGS() as ddgs:
            # Fetch more results to give the model better context
            results = list(ddgs.text(site_query, max_results=4))
        if not results:
            return "No results found for that query."

        # Format the results cleanly for the model
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n---")
        return "\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Tool 'search_manim_docs' failed: {e}")
        return f"An error occurred during the search: {e}"


# --- 2. UPDATED PROMPT WITH TOOL INSTRUCTIONS ---
# This prompt instructs the model to use the defined tool.
from orchestrator_prompts import Animator_Phase_1_Blueprint_Manim_Docs_v2 as BLUEPRINT_PROMPT_WITH_TOOL

# --- LOAD INPUTS ---
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    input_data = json.load(f)
steps = input_data.get('solution_steps', [])
if not steps:
    raise ValueError(f"No solution_steps found in {INPUT_PATH}.")

with open(STYLE_PATH, "r", encoding="utf-8") as f:
    style_config = json.load(f)

def load_image(image_path):
    if not image_path:
        return None
    img_path = Path(image_path)
    if not img_path.exists():
        logger.warning(f"Image not found: {image_path}, continuing without it.")
        return None
    return Image.open(img_path)

image_obj = load_image(IMAGE_PATH)

# --- UTILITY FOR JSON EXTRACTION ---
def extract_json_object(text):
    text = text.strip()
    if text.startswith('```json'):
        text = text[len('```json'):].strip()
    if text.endswith('```'):
        text = text[:-3].strip()
    
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed: {e}. Text was: {match.group(0)[:500]}")
    
    logger.warning("Could not extract JSON from response. Preview: %s", text[:200])
    return None

# --- 3. MODIFIED SCENE PROCESSING LOGIC WITH TOOL CALLING ---
# Initialize the model once with the tool definition.
model = genai.GenerativeModel(MODEL_NAME, tools=[search_manim_docs])
output_dir = Path(BLUEPRINT_DIR)
output_dir.mkdir(parents=True, exist_ok=True)

def process_scene(i, step):
    scene_id = step.get('scene_id', f'scene_{i}')
    file_stem = f"{i:02d}_{scene_id}"
    out_path = output_dir / f"{file_stem}.json"

    if out_path.exists():
        logger.info(f"Skipping scene {i} ({scene_id}) - blueprint already exists.")
        return True

    single_scene_prompt = f"""{BLUEPRINT_PROMPT_WITH_TOOL}

**Style Config JSON:**
```json
{json.dumps(style_config, ensure_ascii=False, indent=2)}
```

**Single Scene Task:**
Generate a self-contained blueprint JSON for the following solution step. Use your `search_manim_docs` tool to find the best functions and properties.

**Solution Step:**
```json
{json.dumps(step, ensure_ascii=False, indent=2)}
```
"""

    model_input_parts = [single_scene_prompt]
    if image_obj:
        model_input_parts.append(image_obj)
    
    start_time = time.time()
    try:
        # Start the conversation with the model
        response = model.generate_content(model_input_parts)

        # This loop handles the multi-turn conversation required for tool calls
        while response.candidates[0].content.parts[0].function_call.name:
            function_call = response.candidates[0].content.parts[0].function_call
            
            # Execute the specific function the model requested
            if function_call.name == "search_manim_docs":
                tool_output = search_manim_docs(query=function_call.args["query"])
            else:
                logger.warning(f"Model requested an unknown tool: {function_call.name}")
                tool_output = f"Error: Tool '{function_call.name}' is not defined."

            # Send the tool's response back to the model to continue the conversation
            response = model.generate_content(
                [
                    *model_input_parts,
                    response.candidates[0].content, # Include previous model turn
                    content_types.to_part(
                        {"function_response": {"name": function_call.name, "response": {"result": tool_output}}}
                    )
                ]
            )

        # Once the loop finishes, the response should contain the final JSON text
        api_call_duration = time.time() - start_time
        logger.info(f"Total conversation for scene {i} ({scene_id}) took {api_call_duration:.2f} seconds.")

        response_text = response.text
        parsed_json = extract_json_object(response_text)

        if not parsed_json:
            raw_path = output_dir / f'{file_stem}_raw_response.txt'
            with open(raw_path, 'w', encoding='utf-8') as f:
                f.write(response_text)
            logger.error(f"Failed to extract blueprint JSON for scene {i} ({scene_id}). Full response saved to {raw_path}.")
            return False

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved blueprint for scene {i}: {out_path}")
        return True

    except Exception as e:
        logger.error(f"An unexpected error occurred while processing scene {i} ({scene_id}): {e}", exc_info=True)
        return False


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    scenes_to_process = list(enumerate(steps))
    if not scenes_to_process:
        print("No solution steps found in the input file. Exiting.")
        sys.exit(0)

    print(f"Starting blueprint generation for {len(scenes_to_process)} scenes using model '{MODEL_NAME}'...")
    # Using a ThreadPoolExecutor to run API calls in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_scene = {executor.submit(process_scene, i, step): f"Scene {i}" for i, step in scenes_to_process}
        results = []
        for future in concurrent.futures.as_completed(future_to_scene):
            try:
                results.append(future.result())
            except Exception as exc:
                logger.error(f"{future_to_scene[future]} generated an exception: {exc}")

    successful_count = sum(1 for r in results if r)
    print(f"\n--- Generation Complete ---")
    print(f"{successful_count} of {len(scenes_to_process)} blueprints generated successfully.")
    print(f"Blueprints are saved in: {output_dir.resolve()}\n")