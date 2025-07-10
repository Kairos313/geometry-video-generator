import os
import base64
import json
import time
from openai import OpenAI
from pathlib import Path
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("/Users/kairos/Desktop/Prompt Generation/.env")

# Add the orchestrator's directory to the path to import the prompt
sys.path.append('/Users/kairos/Desktop/Prompt Generation/Geometry_v2')
from orchestrator_prompts import Manim_Geometric_Surveyor_v4

# Paths
image_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_question.png"
styler_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/geo_v2_style.json"

# Prepare image as data URI
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

# Load styler.json
with open(styler_path, "r", encoding="utf-8") as f:
    styler_json = json.load(f)

# Load solution steps JSON
solution_steps_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_solution.json"
with open(solution_steps_path, "r", encoding="utf-8") as f:
    solution_steps_json = json.load(f)

# Compose the message content
message_content = [
    {
        "type": "text",
        "text": f"{Manim_Geometric_Surveyor_v4}\n\nStyler config:\n{json.dumps(styler_json, indent=2)}\n\nSolution steps JSON:\n{json.dumps(solution_steps_json, indent=2)}"
    },
    prepare_image_for_api(image_path)
]

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Make the API call and measure time/tokens
try:
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

    # Save output to .py file
    output_path = "Geometry_v2/geometric_figure_output.py"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)
    print(f"Output saved to {output_path}")

    # Print timing and token usage
    print(f"API call time: {elapsed:.2f} seconds")
    usage = getattr(completion, 'usage', None)
    if usage:
        prompt_tokens = getattr(usage, 'prompt_tokens', 0)
        completion_tokens = getattr(usage, 'completion_tokens', 0)
        total_tokens = getattr(usage, 'total_tokens', 0)
        print(f"Token usage: input={prompt_tokens}, output={completion_tokens}, total={total_tokens}")
    else:
        print("Token usage information not available.")

except Exception as e:
    print(f"Error making API call: {e}")