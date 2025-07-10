import json
import os
import re
import base64
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from mutagen.mp3 import MP3

class MathScriptGenerator:
    def __init__(self, api_key: str, voice_id: str, output_directory: str):
        self.api_key = api_key
        self.voice_id = voice_id
        self.output_directory = output_directory
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)
    
    def load_math_problem(self, json_file_path: str) -> Dict[str, Any]:
        """Load and parse the math problem JSON file."""
        with open(json_file_path, 'r') as f:
            return json.load(f)
    
    def generate_script_for_step(self, step: Dict[str, Any]) -> str:
        """Generate a conversational script for a solution step."""
        step_id = step.get('step_id', '')
        
        # Handle key_takeaways differently
        if step_id == 'key_takeaways':
            title = step.get('title', 'Key Takeaways')
            points = step.get('points', [])
            
            script = f"Let's review the {title.lower()}. "
            for i, point in enumerate(points, 1):
                # Clean up markdown formatting for speech
                clean_point = re.sub(r'\*\*(.*?)\*\*', r'\1', point)  # Remove bold markdown
                script += f"Point {i}: {clean_point}... "
            
            return script.strip()
        
        # For regular solution steps
        action = step.get('action', '')
        calculation = step.get('calculation', '')
        result = step.get('result', '')
        
        # Clean up any existing break tags for natural speech
        action_clean = re.sub(r'<break time="[^"]*"\s*/?\s*>', '', action)
        calculation_clean = re.sub(r'<break time="[^"]*"\s*/?\s*>', '', calculation)
        
        # Create conversational script
        script = f"{action_clean} "
        
        if calculation_clean:
            script += f"Let me walk you through the calculation. {calculation_clean} "
        
        if result:
            script += f"Therefore, {result.lower()}"
        
        return script.strip()
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for timestamp processing."""
        # Handle ellipses and standard sentence endings
        # This regex ensures we split after .!? or ..., followed by a space.
        # It uses a positive lookbehind (?<=[.!?]) or (?<=\.{3}) to keep the punctuation.
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+|(?<=\.{3})\s+', text) if s.strip()]
        return sentences
    
    async def generate_audio_with_timestamps(self, session: aiohttp.ClientSession, text: str, step_id: str) -> Dict[str, Any]:
        """Generate audio and timestamps using ElevenLabs TTS with timing endpoint (async)."""
        url = f"{self.base_url}/text-to-speech/{self.voice_id}/with-timestamps"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "output_format": "mp3_44100_128",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.3,
                "use_speaker_boost": True
            }
        }
        
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                # --- START OF FIX ---
                # Check status code first for non-2xx responses
                if response.status not in range(200, 300):
                    error_text = await response.text() # Read the raw error message
                    return {
                        "success": False,
                        "message": f"API request failed with status {response.status} for step {step_id}: {error_text}",
                        "status_code": response.status
                    }
                
                # If status is successful, try parsing JSON. Catch JSONDecodeError specifically.
                try:
                    result = await response.json()
                except json.JSONDecodeError:
                    raw_response_text = await response.text()
                    return {
                        "success": False,
                        "message": f"API returned non-JSON response for step {step_id} despite status {response.status}. Raw response: {raw_response_text[:500]}...", # Truncate long responses
                        "status_code": response.status
                    }
                # --- END OF FIX ---
            
            # Extract audio data and timestamps
            audio_base64 = result.get('audio_base64', '')
            character_timestamps = result.get('alignment', {}).get('characters', [])
            
            if not audio_base64:
                return {
                    "success": False,
                    "message": f"No audio data received from API for step {step_id} (API response was valid JSON but missing audio data)."
                }
            
            # Save audio file
            audio_file_path = os.path.join(self.output_directory, f"{step_id}.mp3")
            
            with open(audio_file_path, "wb") as f:
                f.write(base64.b64decode(audio_base64))
            
            # Get audio duration
            duration_seconds = MP3(audio_file_path).info.length
            
            # Process character timestamps into sentence timestamps
            sentence_timestamps = self.process_character_to_sentence_timestamps(
                text, character_timestamps
            )
            
            # Save timestamps
            timestamps_file_path = os.path.join(self.output_directory, f"{step_id}_timestamps.json")
            with open(timestamps_file_path, "w") as f:
                json.dump(sentence_timestamps, f, indent=2)
            
            return {
                "success": True,
                "message": "Audio and timestamps generated successfully",
                "audio_file_path": audio_file_path,
                "timestamps_file_path": timestamps_file_path,
                "duration_seconds": round(duration_seconds, 2),
                "sentence_timestamps": sentence_timestamps
            }
            
        except aiohttp.ClientError as e:
            # This catches network-related errors (DNS issues, connection refused, timeouts before getting a response body)
            return {
                "success": False,
                "message": f"Network/Client error during API request for step {step_id}: {str(e)}",
                "status_code": None # Or e.status if it was set before connection issues
            }
        except Exception as e:
            # Generic catch-all for any other unexpected errors
            return {
                "success": False,
                "message": f"An unexpected error occurred during processing for step {step_id}: {str(e)}"
            }
    
    def process_character_to_sentence_timestamps(self, text: str, char_timestamps: List[Dict]) -> List[Dict]:
        """
        Convert character-level timestamps to sentence-level timestamps.
        This attempts to align the characters from ElevenLabs response with the original text.
        """
        sentences = self.split_into_sentences(text)
        sentence_timestamps = []
        
        if not char_timestamps:
            # Fallback: create basic sentence structure without timing
            for sentence in sentences:
                sentence_timestamps.append({
                    "sentence": sentence,
                    "start": 0.0,
                    "end": 0.0
                })
            return sentence_timestamps
        
        char_to_time_map = {} # Maps original_text_index -> {'start': time, 'end': time}
        
        text_idx = 0 # Pointer for the original `text` string
        for api_char_data in char_timestamps:
            api_char = api_char_data['character']
            start_time = api_char_data['start_time_offset_seconds']
            end_time = api_char_data['end_time_offset_seconds']

            # Try to find the `api_char` in `text` starting from `text_idx`
            found_match = False
            original_text_len = len(text)
            
            while text_idx < original_text_len:
                current_text_char = text[text_idx]
                
                # Prioritize exact or case-insensitive match for alphanumeric characters
                if current_text_char.lower() == api_char.lower() and current_text_char.isalnum():
                    char_to_time_map[text_idx] = {'start': start_time, 'end': end_time}
                    text_idx += 1
                    found_match = True
                    break
                # Handle spaces/punctuation:
                # If API char is whitespace/punctuation, and text char is too, or can be skipped
                elif (api_char.isspace() and current_text_char.isspace()) or \
                     (not api_char.isalnum() and not current_text_char.isalnum() and api_char == current_text_char):
                    char_to_time_map[text_idx] = {'start': start_time, 'end': end_time}
                    text_idx += 1
                    found_match = True
                    break
                elif current_text_char.isspace() or not current_text_char.isalnum():
                    # If current text char is a separator/punctuation that might be skipped by TTS,
                    # just advance the text_idx and try to match the *same* api_char with the *next* text_char.
                    text_idx += 1
                    continue # Continue `while` loop, try next text char with current api_char
                else:
                    # Mismatch of alphanumeric chars, or unexpected sequence.
                    # This is a fallback: map API char to current text_idx anyway, then advance text_idx.
                    # This heuristic is imperfect but prevents getting stuck.
                    char_to_time_map[text_idx] = {'start': start_time, 'end': end_time}
                    text_idx += 1
                    found_match = True
                    break
            
            # If no match found for an api_char (e.g., text_idx exhausted or complex mismatch)
            # We still need to process the api_char to advance through char_timestamps.
            # No specific text_idx will be mapped for this api_char in char_to_time_map.
            if not found_match and text_idx >= original_text_len:
                pass # This api_char won't be mapped to the original text.

        # Now, map sentences to timestamps using the char_to_time_map
        sentence_timestamps = []
        current_text_pos = 0 # Current character index in the full original `text` string for `sentences` loop

        for sentence in sentences:
            sentence_start = None
            sentence_end = None
            
            # Find the starting character's timestamp for the current sentence
            for i in range(len(sentence)):
                absolute_char_pos = current_text_pos + i
                if absolute_char_pos in char_to_time_map:
                    sentence_start = char_to_time_map[absolute_char_pos]['start']
                    break
            
            # Find the ending character's timestamp for the current sentence
            for i in range(len(sentence) - 1, -1, -1):
                absolute_char_pos = current_text_pos + i
                if absolute_char_pos in char_to_time_map:
                    sentence_end = char_to_time_map[absolute_char_pos]['end']
                    break
            
            sentence_timestamps.append({
                "sentence": sentence.strip(),
                "start": round(sentence_start, 2) if sentence_start is not None else 0.0,
                "end": round(sentence_end, 2) if sentence_end is not None else 0.0
            })
            
            # Advance `current_text_pos` for the next sentence.
            current_text_pos += len(sentence)
            # Consume any trailing spaces/punctuation after this sentence in the original text
            while current_text_pos < len(text) and (text[current_text_pos].isspace() or not text[current_text_pos].isalnum()):
                current_text_pos += 1
            
        return sentence_timestamps
    
    async def process_single_step(self, session: aiohttp.ClientSession, step: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single step asynchronously."""
        step_id = step['step_id']
        print(f"Processing step: {step_id}")
        
        # Generate script
        script_text = self.generate_script_for_step(step)
        
        # Generate audio and timestamps
        result = await self.generate_audio_with_timestamps(session, script_text, step_id)
        
        # Create step result object
        step_result = {
            "step_id": step_id,
            "script_text": script_text,
            "audio_file_path": result.get("audio_file_path"),
            "duration_seconds": result.get("duration_seconds", 0),
            "timestamps_file_path": result.get("timestamps_file_path"),
            "sentence_timestamps": result.get("sentence_timestamps", []),
            "api_response": {
                "success": result["success"],
                "message": result["message"],
                "elevenlabs_request_id": None  # Not available directly in with-timestamps endpoint response
            }
        }
        
        print(f"Completed step: {step_id} - {'Success' :<7s} {'(Failed)' if not result['success'] else ''}")
        return step_result

    async def process_math_solution(self, json_file_path: str) -> Dict[str, Any]:
        """Main method to process the entire math solution sequentially."""
        # Load the problem
        full_problem = self.load_math_problem(json_file_path)
        
        # Get steps to process
        steps_to_process = full_problem.get('solution_steps', [])
        
        # Add key_takeaways if present
        key_takeaways = full_problem.get('key_takeaways')
        if key_takeaways:
            steps_to_process.append({
                "step_id": "key_takeaways",
                "title": key_takeaways.get("title"),
                "points": key_takeaways.get("points")
            })
        
        print(f"Processing {len(steps_to_process)} steps sequentially...")
        
        processed_steps = []
        # Create a single aiohttp session for all requests
        timeout = aiohttp.ClientTimeout(total=300) # 5 minute timeout per request
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for step in steps_to_process:
                try:
                    result = await self.process_single_step(session, step)
                    processed_steps.append(result)
                except Exception as e:
                    # Handle unexpected exceptions during the sequential processing of a step
                    step_id = step['step_id']
                    script_text = self.generate_script_for_step(step)
                    error_result = {
                        "step_id": step_id,
                        "script_text": script_text,
                        "audio_file_path": None,
                        "duration_seconds": 0,
                        "timestamps_file_path": None,
                        "sentence_timestamps": [],
                        "api_response": {
                            "success": False,
                            "message": f"An unhandled exception occurred during step processing: {str(e)}",
                            "elevenlabs_request_id": None
                        }
                    }
                    processed_steps.append(error_result)
                    print(f"Error processing step {step_id}: {str(e)}")
        
        return {
            "processed_steps": processed_steps
        }

# Usage example
def main():
    # Configuration - replace with your actual values
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    VOICE_ID = "Fahco4VZzobUeiPqni1S"
    OUTPUT_DIRECTORY = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Audio"
    JSON_FILE_PATH = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_solution.json"
    
    if not ELEVENLABS_API_KEY:
        print("Error: ELEVENLABS_API_KEY environment variable not set. Please set it using 'export ELEVENLABS_API_KEY=\"your_key\"'")
        return
    
    # Removed the 'your_voice_id_here' check as it's now hardcoded with a real ID
    # if VOICE_ID == "your_voice_id_here": 
    #     print("Error: Please replace 'your_voice_id_here' with your actual ElevenLabs Voice ID in the script.")
    #     return

    # Create generator instance
    generator = MathScriptGenerator(
        api_key=ELEVENLABS_API_KEY,
        voice_id=VOICE_ID,
        output_directory=OUTPUT_DIRECTORY
    )
    
    # Process the math solution
    try:
        result = asyncio.run(generator.process_math_solution(JSON_FILE_PATH))
        
        # Save final result
        output_file = os.path.join(OUTPUT_DIRECTORY, "processing_result.json")
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\nProcessing complete! Results saved to {output_file}")
        
        # Print summary
        successful_steps = sum(1 for step in result["processed_steps"] 
                             if step["api_response"]["success"])
        total_steps = len(result["processed_steps"])
        
        print(f"Summary: Successfully processed {successful_steps}/{total_steps} steps.")
        
    except Exception as e:
        print(f"\nAn unexpected error occurred during overall processing: {str(e)}")

if __name__ == "__main__":
    main()