import json
import requests
import os
from pydub import AudioSegment
from pydub.utils import mediainfo # Can be useful for debugging if needed
from dotenv import load_dotenv
from pathlib import Path

# --- Configuration ---
# Load environment variables from .env file in the project root
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path)

ELEVEN_LABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if ELEVEN_LABS_API_KEY:
    print(f"Loaded ELEVENLABS_API_KEY: {ELEVEN_LABS_API_KEY[:4]}...{'*' * (len(ELEVEN_LABS_API_KEY)-8)}...{ELEVEN_LABS_API_KEY[-4:]}")
else:
    print("ELEVENLABS_API_KEY not found!")
VOICE_ID = "Fahco4VZzobUeiPqni1S" # Example Voice ID (e.g., "Bella"). Replace with your preferred voice ID.
MODEL_ID = "eleven_multilingual_v2" # Or "eleven_multilingual_v2" etc.

INPUT_JSON_FILE = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/sentence.json"
OUTPUT_JSON_FILE = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/deconstruct.json"
INDIVIDUAL_AUDIO_DIR = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Audio" # Directory for individual sentence MP3s
SCENE_AUDIO_DIR = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene"       # Directory for stitched scene MP3s
TIME_GAP_BETWEEN_SENTENCES = 0.01 # The small gap in seconds between sentences as per your request

# --- Helper Function for Eleven Labs API and Duration Measurement ---

def generate_and_measure_audio(sentence_text: str, step_id: str, sentence_index: int) -> tuple[str, float, AudioSegment] | None:
    """
    Calls the Eleven Labs API to generate audio for a sentence, saves it,
    measures its duration, and returns the AudioSegment object.

    Args:
        sentence_text: The text content of the sentence.
        step_id: The ID of the current step (for naming the audio file).
        sentence_index: The index of the sentence within its step (for naming the audio file).

    Returns:
        A tuple containing (audio_filepath, duration_seconds, AudioSegment_object) on success,
        or None if an error occurs.
    """
    if not ELEVEN_LABS_API_KEY:
        print("Error: ELEVEN_LABS_API_KEY environment variable not set.")
        return None

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }

    data = {
        "text": sentence_text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    # Ensure individual audio directory exists
    os.makedirs(INDIVIDUAL_AUDIO_DIR, exist_ok=True)
    output_filepath = os.path.join(INDIVIDUAL_AUDIO_DIR, f"{step_id}_{sentence_index}.mp3")

    try:
        response = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}", headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        # Save the audio file
        with open(output_filepath, 'wb') as f:
            f.write(response.content)

        # Measure audio duration and get AudioSegment object
        audio_segment = AudioSegment.from_file(output_filepath, format="mp3")
        duration_seconds = len(audio_segment) / 1000.0 # pydub duration is in milliseconds

        print(f"Generated '{output_filepath}' (Duration: {duration_seconds:.2f}s) for: '{sentence_text[:50]}...'")
        return output_filepath, round(duration_seconds, 2), audio_segment

    except requests.exceptions.RequestException as e:
        print(f"API Request Error for '{sentence_text[:50]}...': {e}")
        return None
    except FileNotFoundError:
        print(f"Error: FFmpeg or audio file not found. Ensure FFmpeg is installed and in your PATH.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred processing '{sentence_text[:50]}...': {e}")
        return None

# --- Main Processing Logic ---

def process_solution_steps_with_audio(json_data: dict) -> dict:
    """
    Processes the solution steps, generating audio for each sentence,
    calculating durations, assigning cumulative timestamps, and
    stitching scene audio.

    Args:
        json_data: The parsed JSON data from the input file.

    Returns:
        A new dictionary with updated step and sentence information.
    """
    processed_data = json_data.copy()
    current_cumulative_time = 0.0

    # Ensure output directories exist
    os.makedirs(INDIVIDUAL_AUDIO_DIR, exist_ok=True)
    os.makedirs(SCENE_AUDIO_DIR, exist_ok=True)

    for step in processed_data.get("solution_steps", []):
        step_id = step["step_id"]
        
        individual_sentence_segments_for_scene = [] # To collect AudioSegments for stitching this scene
        timestamped_sentences_in_step = []

        if "sentences" in step and isinstance(step["sentences"], list):
            for i, sentence_text in enumerate(step["sentences"]):
                sentence_start_time = current_cumulative_time
                if current_cumulative_time > 0:
                    sentence_start_time += TIME_GAP_BETWEEN_SENTENCES

                # Generate audio and get actual duration and AudioSegment
                audio_result = generate_and_measure_audio(sentence_text, step_id, i)
                
                audio_filename = None
                duration = 0.0
                sentence_audio_segment = None

                if audio_result:
                    audio_filename, duration, sentence_audio_segment = audio_result
                    individual_sentence_segments_for_scene.append(sentence_audio_segment)
                else:
                    # Fallback: if audio generation fails, use a simulated duration
                    # This ensures timestamps continue to advance. No audio segment for stitching.
                    print(f"Warning: Audio generation failed for sentence '{sentence_text[:50]}...', using simulated duration.")
                    duration = max(0.75, len(sentence_text) * 0.15) # Fallback heuristic

                sentence_end_time = sentence_start_time + duration

                timestamped_sentences_in_step.append({
                    "text": sentence_text,
                    "audio_file_individual": audio_filename, # Path to the generated individual audio file
                    "duration_seconds": round(duration, 2),
                    "start_time_seconds": round(sentence_start_time, 2),
                    "end_time_seconds": round(sentence_end_time, 2)
                })

                current_cumulative_time = sentence_end_time
            
            step["sentences"] = timestamped_sentences_in_step # Update sentences with new structure

        # --- Stitching Logic for the current Scene (Step) ---
        scene_combined_audio = AudioSegment.empty()
        scene_audio_filepath = None

        if individual_sentence_segments_for_scene:
            for i, segment in enumerate(individual_sentence_segments_for_scene):
                scene_combined_audio += segment
                # Add silence between sentences, but not after the very last one in the scene
                if i < len(individual_sentence_segments_for_scene) - 1:
                    silence = AudioSegment.silent(duration=TIME_GAP_BETWEEN_SENTENCES * 1000)
                    scene_combined_audio += silence
            
            scene_audio_filepath = os.path.join(SCENE_AUDIO_DIR, f"{step_id}_scene.mp3")
            try:
                scene_combined_audio.export(scene_audio_filepath, format="mp3")
                print(f"Stitched scene audio for '{step_id}' to '{scene_audio_filepath}'")
                step["audio_file_scene"] = scene_audio_filepath # Add scene audio path to the step
                step["duration_scene_seconds"] = round(len(scene_combined_audio) / 1000.0, 2)
            except Exception as e:
                print(f"Error stitching audio for scene '{step_id}': {e}")
                step["audio_file_scene"] = "ERROR: Stitching failed"

        else:
            print(f"No individual audio segments to stitch for scene '{step_id}'.")
            step["audio_file_scene"] = "N/A (No audio generated)"


    return processed_data

# --- Main execution ---
if __name__ == "__main__":
    if not ELEVEN_LABS_API_KEY:
        print("Please set the ELEVEN_LABS_API_KEY environment variable.")
        exit(1)

    if not os.path.exists(INPUT_JSON_FILE):
        print(f"Error: The input file '{INPUT_JSON_FILE}' was not found. Please ensure it's in the same directory.")
        exit(1)

    try:
        with open(INPUT_JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_JSON_FILE}'. Please check file format for errors.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        exit(1)

    # Process the data and generate audio
    processed_data_with_audio = process_solution_steps_with_audio(data)

    # Save the output to a new JSON file
    try:
        with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(processed_data_with_audio, f, indent=2)
        print(f"\nProcessing complete. Output JSON saved to '{OUTPUT_JSON_FILE}'.")
        print(f"Individual sentence audio files are in '{INDIVIDUAL_AUDIO_DIR}'.")
        print(f"Stitched scene audio files are in '{SCENE_AUDIO_DIR}'.")
    except Exception as e:
        print(f"Error saving output to file: {e}")