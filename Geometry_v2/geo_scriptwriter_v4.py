import json
import requests
import os
from pydub import AudioSegment
from pydub.utils import mediainfo # Can be useful for debugging if needed
from dotenv import load_dotenv
from pathlib import Path
import time

# --- Configuration ---
# Load environment variables from .env file.
# Adjust the path based on where your .env file is relative to this script.
# If this script is in 'Geometry_v2/', and .env is also in 'Geometry_v2/', use Path(__file__).resolve().parent
# If .env is one level up from 'Geometry_v2/', use Path(__file__).resolve().parent.parent
dotenv_path = Path(__file__).resolve().parent.parent / '.env' # Now loads .env from the project root
load_dotenv(dotenv_path)

ELEVEN_LABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if ELEVEN_LABS_API_KEY:
    print(f"Loaded ELEVENLABS_API_KEY: {ELEVEN_LABS_API_KEY[:4]}...{'*' * (len(ELEVEN_LABS_API_KEY)-8)}...{ELEVEN_LABS_API_KEY[-4:]}")
else:
    print("ELEVENLABS_API_KEY not found! Please set it in your .env file.")
    exit(1) # Exit if API key is not found

VOICE_ID = "Fahco4VZzobUeiPqni1S" # Example Voice ID. Replace with your preferred voice ID.
MODEL_ID = "eleven_multilingual_v2" 

# Define paths using Pathlib for better cross-OS compatibility
BASE_DIR = Path("/Users/kairos/Desktop/Prompt Generation/Geometry_v2")

INPUT_JSON_FILE = BASE_DIR / "sentence.json" # Assuming 'sentence.json' is the initial raw text input
OUTPUT_JSON_FILE = BASE_DIR / "deconstruct.json" # Output will be saved here, overwriting if exists
INDIVIDUAL_AUDIO_DIR = BASE_DIR / "Audio" # Directory for individual sentence MP3s
SCENE_AUDIO_DIR = BASE_DIR / "Scene"       # Directory for stitched scene MP3s

TIME_GAP_BETWEEN_SENTENCES = 0.01 # The small gap in seconds between sentences

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
    INDIVIDUAL_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    output_filepath = INDIVIDUAL_AUDIO_DIR / f"{step_id}_{sentence_index}.mp3"

    try:
        api_start_time = time.time()
        response = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}", headers=headers, json=data)
        api_end_time = time.time()
        print(f"API call for '{step_id}_{sentence_index}' took {api_end_time - api_start_time:.2f} seconds")
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        # Save the audio file
        with open(output_filepath, 'wb') as f:
            f.write(response.content)

        # Measure audio duration and get AudioSegment object
        audio_segment = AudioSegment.from_file(str(output_filepath), format="mp3") # pydub needs string path
        duration_seconds = len(audio_segment) / 1000.0 # pydub duration is in milliseconds

        print(f"Generated '{output_filepath.name}' (Duration: {duration_seconds:.2f}s) for: '{sentence_text[:50]}...'")
        return str(output_filepath), round(duration_seconds, 2), audio_segment

    except requests.exceptions.RequestException as e:
        print(f"API Request Error for '{sentence_text[:50]}...': {e}")
        print(f"Response status: {e.response.status_code if e.response else 'N/A'}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
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
    calculating durations, and assigning timestamps relative to the scene's start,
    and stitching scene audio.

    Args:
        json_data: The parsed JSON data from the input file.

    Returns:
        A new dictionary with updated step and sentence information.
    """
    processed_data = json_data.copy()

    # Ensure output directories exist
    INDIVIDUAL_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    SCENE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    for step in processed_data.get("solution_steps", []):
        step_id = step["step_id"]
        
        individual_sentence_segments_for_scene = [] # To collect AudioSegments for stitching this scene
        timestamped_sentences_in_step = []
        
        # --- NEW/CONFIRMED: Initialize time tracker for the current scene, resets for each step ---
        current_time_within_scene = 0.0

        if "sentences" in step and isinstance(step["sentences"], list):
            for i, sentence_entry in enumerate(step["sentences"]):
                # Extract the sentence text. This handles both string-only sentences
                # and the dict-based sentences from your deconstruct.json example.
                if isinstance(sentence_entry, dict) and "text" in sentence_entry:
                    sentence_text = sentence_entry["text"]
                elif isinstance(sentence_entry, str):
                    sentence_text = sentence_entry
                else:
                    print(f"Warning: Unexpected sentence format in step '{step_id}', index {i}. Skipping.")
                    continue # Skip to the next sentence

                # Calculate start time relative to the beginning of the current scene
                sentence_start_time_relative = current_time_within_scene
                # Add gap ONLY if it's not the very first sentence of THIS scene (i.e., i > 0)
                if i > 0:
                    sentence_start_time_relative += TIME_GAP_BETWEEN_SENTENCES

                # Generate audio and get actual duration and AudioSegment
                audio_result = generate_and_measure_audio(sentence_text, step_id, i)
                
                audio_filename = None
                duration = 0.0
                sentence_audio_segment = None

                if audio_result:
                    audio_filename, duration, sentence_audio_segment = audio_result
                    individual_sentence_segments_for_scene.append(sentence_audio_segment)
                else:
                    print(f"Warning: Audio generation failed for sentence '{sentence_text[:50]}...', using simulated duration.")
                    duration = max(0.75, len(sentence_text) * 0.15) # Fallback heuristic
                    # Note: If audio generation fails, this sentence will not be included in stitched audio.

                sentence_end_time_relative = sentence_start_time_relative + duration

                timestamped_sentences_in_step.append({
                    "text": sentence_text,
                    "audio_file_individual": audio_filename, # Path to the generated individual audio file
                    "duration_seconds": round(duration, 2),
                    "start_time_seconds": round(sentence_start_time_relative, 2), # Use relative time
                    "end_time_seconds": round(sentence_end_time_relative, 2)     # Use relative time
                })

                # Update current time for the next sentence WITHIN THIS SCENE
                current_time_within_scene = sentence_end_time_relative
            
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
            
            scene_audio_filepath = SCENE_AUDIO_DIR / f"{step_id}_scene.mp3"
            try:
                scene_combined_audio.export(str(scene_audio_filepath), format="mp3") # pydub needs string path
                print(f"Stitched scene audio for '{step_id}' to '{scene_audio_filepath}'")
                step["audio_file_scene"] = str(scene_audio_filepath) # Add scene audio path to the step
                step["duration_scene_seconds"] = round(len(scene_combined_audio) / 1000.0, 2)
                
                # Sanity check: Last sentence's end_time should match scene duration
                if timestamped_sentences_in_step and abs(timestamped_sentences_in_step[-1]["end_time_seconds"] - step["duration_scene_seconds"]) > 0.01:
                    print(f"Warning: For scene '{step_id}', last sentence end time ({timestamped_sentences_in_step[-1]['end_time_seconds']:.2f}s) "
                          f"does not exactly match stitched scene duration ({step['duration_scene_seconds']:.2f}s). This can be due to rounding or silence handling differences.")

            except Exception as e:
                print(f"Error stitching audio for scene '{step_id}': {e}")
                step["audio_file_scene"] = "ERROR: Stitching failed"
                step["duration_scene_seconds"] = 0.0 # Set to 0 if failed
        else:
            print(f"No individual audio segments to stitch for scene '{step_id}'.")
            step["audio_file_scene"] = "N/A (No audio generated for scene)"
            step["duration_scene_seconds"] = 0.0 # No audio, no duration


    return processed_data

# --- Main execution ---
if __name__ == "__main__":
    total_start_time = time.time()
    if not ELEVEN_LABS_API_KEY:
        print("Please set the ELEVENLABS_API_KEY environment variable. Exiting.")
        exit(1)

    if not INPUT_JSON_FILE.exists():
        print(f"Error: The input file '{INPUT_JSON_FILE}' was not found. Please ensure it exists.")
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
    total_end_time = time.time()
    print(f"Total script execution time: {total_end_time - total_start_time:.2f} seconds")