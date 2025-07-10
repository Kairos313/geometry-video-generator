import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import base64

# Import the Scene_Code_Generation prompt
from parallel_prompts import Scene_Code_Generation_v1

# Load environment variables
load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file.")

# Paths
base_dir = Path("/Users/kairos/Desktop/Prompt Generation/Geometry_v2")
deconstruct_path = base_dir / "deconstruct_parallel.json"
style_path = base_dir / "geo_v2_style.json"
geometric_figure_output_path = base_dir / "geometric_figure_output.py"
problem_image_path = base_dir / "problem_image.png"
output_dir = base_dir / "Parallel_Outputs"
output_dir.mkdir(exist_ok=True)

# Load all required data
with open(deconstruct_path, "r", encoding="utf-8") as f:
    deconstruct_data = json.load(f)
with open(style_path, "r", encoding="utf-8") as f:
    style_data = json.load(f)
with open(geometric_figure_output_path, "r", encoding="utf-8") as f:
    geometric_figure_code = f.read()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

image_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_question.png"

def generate_scene_code(step):
    step_id = step["step_id"]
    message_content = [
        {
            "type": "text",
            "text": (
                f"{Scene_Code_Generation_v1}\n\n"
                f"---\n"
                f"**INPUT FILES:**\n"
                f"1. deconstruct_parallel.json (full file):\n```json\n{json.dumps(deconstruct_data, indent=2)}\n```\n"
                f"2. geo_v2_style.json:\n```json\n{json.dumps(style_data, indent=2)}\n```\n"
                f"3. geometric_figure_output.py:\n```python\n{geometric_figure_code}\n```\n"
                f"4. math_question.png: (image file present at {image_path}, sent as input)\n"
                f"\n---\n"
                f"**TARGET_STEP_ID:** {step_id}\n"
                f"Generate the complete Manim Python code for this scene as described above. Output ONLY the code, in a single Python code block."
            )
        },
        prepare_image_for_api(image_path)
    ]
    start_time = time.time()
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://yoursite.com",
            "X-Title": "Your App Name",
        },
        model="anthropic/claude-sonnet-4",
        messages=[
            {
                "role": "user",
                "content": message_content
            }
        ],
        max_tokens=8000,
        temperature=0.2
    )
    elapsed = time.time() - start_time
    # Extract code block from response
    code_match = re.search(r"```python(.*?)```", completion.choices[0].message.content, re.DOTALL)
    code = code_match.group(1).strip() if code_match else completion.choices[0].message.content

    # Ensure import of geometric_figure_output.py
    import_statement = "from Geometry_v2.geometric_figure_output import *"
    if import_statement not in code:
        # Find last import statement
        import_lines = [m.end() for m in re.finditer(r"^import .*$|^from .+ import .*$", code, re.MULTILINE)]
        if import_lines:
            insert_pos = import_lines[-1]
            code = code[:insert_pos] + "\n" + import_statement + code[insert_pos:]
        else:
            code = import_statement + "\n" + code
    # Save to file
    out_path = output_dir / f"scene_{step_id}.py"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(code)
    # Token usage
    usage = getattr(completion, 'usage', None)
    input_tokens = getattr(usage, 'prompt_tokens', 0) if usage else 0
    output_tokens = getattr(usage, 'completion_tokens', 0) if usage else 0
    total_tokens = getattr(usage, 'total_tokens', 0) if usage else 0
    print(f"Saved code for {step_id} to {out_path} | Time: {elapsed:.2f}s | Input tokens: {input_tokens} | Output tokens: {output_tokens} | Total tokens: {total_tokens}")
    return {
        "step_id": step_id,
        "file": str(out_path),
        "time": elapsed,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens
    }

def prepare_image_for_api(image_path):
    ext = Path(image_path).suffix.lower()
    media_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_uri = f"data:{media_type};base64,{image_b64}"
    return {
        "type": "image_url",
        "image_url": {
            "url": data_uri
        }
    }

def main():
    steps = deconstruct_data["solution_steps"]
    # Only process the first scene for testing
    steps_to_run = steps[:1]
    # steps_to_run = steps[:2]  # Commented out: Only generate the first scene for now
    # steps_to_run = steps      # Commented out: Only generate the first scene for now
    results = []
    start_all = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_step = {executor.submit(generate_scene_code, step): step for step in steps_to_run}
        for future in as_completed(future_to_step):
            result = future.result()
            results.append(result)
    total_time = time.time() - start_all
    total_tokens = sum(r["total_tokens"] for r in results)
    print("\n--- Parallel Scene Generation Summary ---")
    print(f"Total time for all API calls: {total_time:.2f} seconds")
    print(f"Total tokens used: {total_tokens}")
    print("\nPer-scene details:")
    print(f"{'Scene':<35} {'Time (s)':>10} {'Prompt':>10} {'Completion':>12} {'Total':>8}")
    for r in results:
        print(f"{r['step_id']:<35} {r['time']:>10.2f} {r['input_tokens']:>10} {r['output_tokens']:>12} {r['total_tokens']:>8}")

if __name__ == "__main__":
    main() 