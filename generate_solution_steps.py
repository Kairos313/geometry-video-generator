#!/usr/bin/env python3
"""
Solution Steps Generator
Makes an API call to Gemini-2.5-pro using the Solution_Steps prompt from geometry_prompts.py
Stores the entire JSON output in a single file called math_solution_.json
"""

import os
import json
import logging
import time
import base64
import re
from pathlib import Path
from dotenv import load_dotenv
import requests
from pdf2image import convert_from_path
import tempfile

# Import the Solution_Steps prompt
import sys
sys.path.append('/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline')
from pipeline_prompts import Solution_Steps_v2

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SolutionStepsGenerator:
    """Generate solution steps using Gemini-2.5-pro API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        logger.info("Initialized Solution Steps Generator with Gemini-2.5-pro")
    
    def convert_pdf_to_images(self, pdf_path: str, dpi: int = 300):
        """
        Convert PDF pages to PIL images.
        
        Args:
            pdf_path (str): Path to the PDF file
            dpi (int): Resolution for image conversion
            
        Returns:
            list: List of PIL Image objects
        """
        try:
            logger.info(f"Converting PDF to images: {pdf_path}")
            images = convert_from_path(pdf_path, dpi=dpi)
            logger.info(f"✓ Converted {len(images)} pages to images")
            return images
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            raise
    
    def save_image_to_temp(self, image, page_num: int = 0):
        """
        Save a PIL image to a temporary file.
        
        Args:
            image: PIL Image object
            page_num (int): Page number for naming
            
        Returns:
            str: Path to temporary image file
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=f'_page_{page_num}.png', delete=False) as tmp_file:
                image.save(tmp_file.name, 'PNG')
                logger.info(f"✓ Saved page {page_num} to temporary file: {tmp_file.name}")
                return tmp_file.name
        except Exception as e:
            logger.error(f"Error saving image to temp file: {e}")
            raise
    
    def encode_image_to_base64(self, image_path: str) -> str:
        """Encode image to base64 string for API call."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def make_gemini_api_call(self, image_paths: list):
        """
        Make API call to Gemini-2.5-pro to generate solution steps.
        
        Args:
            image_paths (list): List of paths to image files
            
        Returns:
            dict: API response with content and metadata
        """
        try:
            # Encode all images
            image_contents = []
            for i, image_path in enumerate(image_paths):
                base64_image = self.encode_image_to_base64(image_path)
                image_contents.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                })
                logger.info(f"✓ Encoded image {i+1}/{len(image_paths)}")
            
            # Use the full Solution_Steps_v2 prompt
            prompt_text = Solution_Steps_v2
            
            # Prepare the API request payload
            payload = {
                "model": "google/gemini-2.5-pro",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt_text
                            }
                        ] + image_contents
                    }
                ],
                "max_tokens": 20000,
                "temperature": 0.1
            }
            
            # API endpoint
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            # Headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo",
                "X-Title": "Solution Steps Generator"
            }
            
            # Start timing the API call
            start_time = time.time()
            
            # Make the API call
            logger.info(f"Making Gemini API call with {len(image_paths)} images...")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            # End timing
            end_time = time.time()
            api_call_duration = end_time - start_time
            
            # Parse the response
            response_data = response.json()
            
            # Extract token usage information
            usage = response_data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
            
            # Extract the generated content
            if response_data.get("choices") and len(response_data["choices"]) > 0:
                content = response_data["choices"][0]["message"]["content"]
                
                # Use the specific absolute path for debug files
                output_dir = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/math_solution_pipeline"
                os.makedirs(output_dir, exist_ok=True)
                

                
                logger.info(f"✓ API call completed successfully!")
                logger.info(f"   - Duration: {api_call_duration:.2f} seconds")
                logger.info(f"   - Tokens: {total_tokens} (input: {prompt_tokens}, output: {completion_tokens})")
                logger.info(f"   - Response length: {len(content)} characters")
                
                return {
                    "success": True,
                    "content": content,
                    "api_call_duration": api_call_duration,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens
                }
            else:
                error_msg = "No choices in Gemini API response"
                logger.error(f"Error: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Gemini API request failed: {str(e)}"
            logger.error(f"Error: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error in Gemini call: {str(e)}"
            logger.error(f"Error: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
    
    def extract_question_number(self, question_image_path: str):
        """
        Extract question number from question image filename.
        
        Args:
            question_image_path (str): Path to question image file
            
        Returns:
            str: Question number or "unknown" if not found
        """
        try:
            if not question_image_path:
                return "unknown"
            
            filename = os.path.basename(question_image_path)
            # Extract number from "question_X.png" format
            match = re.search(r'question_(\d+)', filename)
            if match:
                return match.group(1)
            else:
                return "unknown"
                
        except Exception as e:
            logger.error(f"Error extracting question number: {e}")
            return "unknown"
    
    def extract_both_json_from_response(self, content: str):
        """
        Extract both JSON outputs from the API response content.
        
        Args:
            content (str): Raw API response content
            
        Returns:
            tuple: (standard_json, verbose_json) or (None, None) if not found
        """
        try:
            # Look for JSON blocks in the response
            json_pattern = r'```json\s*(\{.*?\})\s*```'
            matches = re.findall(json_pattern, content, re.DOTALL)
            
            if len(matches) >= 2:
                # First JSON is standard, second is verbose
                standard_json = json.loads(matches[0])
                verbose_json = json.loads(matches[1])
                logger.info(f"✓ Extracted 2 JSON blocks from markdown format")
                return standard_json, verbose_json
            
            # If no markdown JSON blocks, try to find raw JSON
            json_objects = []
            brace_count = 0
            start_pos = -1
            
            for i, char in enumerate(content):
                if char == '{':
                    if brace_count == 0:
                        start_pos = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_pos != -1:
                        json_str = content[start_pos:i+1]
                        try:
                            json_obj = json.loads(json_str)
                            json_objects.append(json_obj)
                        except json.JSONDecodeError:
                            pass
                        start_pos = -1
            
            if len(json_objects) >= 2:
                # First JSON is standard, second is verbose
                logger.info(f"✓ Extracted 2 JSON objects from raw format")
                return json_objects[0], json_objects[1]
            
            logger.error(f"Expected 2 JSON objects, found {len(json_objects)}")
            return None, None
                
        except Exception as e:
            logger.error(f"Error extracting JSON from response: {e}")
            return None, None
    
    def generate_intelligent_filename(self, input_path: str, question_image_path: str = None):
        """
        Generate an intelligent filename based on input files.
        
        Args:
            input_path (str): Path to the main input file
            question_image_path (str): Optional path to question image
            
        Returns:
            str: Generated filename
        """
        try:
            # Extract base names from input files
            input_base = os.path.splitext(os.path.basename(input_path))[0]
            
            if question_image_path:
                question_base = os.path.splitext(os.path.basename(question_image_path))[0]
                # Create filename with both inputs
                filename = f"solution_{input_base}_{question_base}"
            else:
                # Create filename with just main input
                filename = f"solution_{input_base}"
            
            # Add timestamp for uniqueness
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}"
            
            return filename
            
        except Exception as e:
            logger.error(f"Error generating filename: {e}")
            # Fallback to timestamp-based filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            return f"solution_generated_{timestamp}"
    
    def save_raw_output(self, content: str):
        """
        Save the entire raw output from the API as .txt file with fixed filename.
        
        Args:
            content (str): The complete raw API response content
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use the specific absolute path for math_solution_pipeline
            output_dir = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/math_solution_pipeline"
            os.makedirs(output_dir, exist_ok=True)
            
            # Use fixed filename
            output_filename = os.path.join(output_dir, "math_solution_raw.txt")
            
            # Save as .txt file (always overwrite)
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✓ Saved complete raw output to: {output_filename}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving raw output: {e}")
            return False
    
    def save_parsed_json_files(self, standard_json: dict, verbose_json: dict):
        """
        Save the parsed JSON outputs as separate files with fixed filenames.
        
        Args:
            standard_json (dict): The standard solution JSON
            verbose_json (dict): The verbose solution JSON
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use the specific absolute path for math_solution_pipeline
            output_dir = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/math_solution_pipeline"
            os.makedirs(output_dir, exist_ok=True)
            
            # Use fixed filenames (always overwrite)
            standard_filename = os.path.join(output_dir, "math_solution_standard.json")
            verbose_filename = os.path.join(output_dir, "math_solution_verbose.json")
            
            # Save standard JSON
            with open(standard_filename, 'w', encoding='utf-8') as f:
                json.dump(standard_json, f, indent=2)
            logger.info(f"✓ Saved standard solution to: {standard_filename}")
            
            # Save verbose JSON
            with open(verbose_filename, 'w', encoding='utf-8') as f:
                json.dump(verbose_json, f, indent=2)
            logger.info(f"✓ Saved verbose solution to: {verbose_filename}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving parsed JSON files: {e}")
            return False
    
    def cleanup_temp_files(self, temp_files: list):
        """
        Clean up temporary image files.
        
        Args:
            temp_files (list): List of temporary file paths to delete
        """
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
                logger.info(f"✓ Cleaned up temporary file: {temp_file}")
            except Exception as e:
                logger.warning(f"Could not delete temporary file {temp_file}: {e}")
    
    def generate_solution_steps(self, input_path: str, question_image_path: str = None):
        """
        Complete pipeline to generate solution steps from an image or PDF, optionally including a question image.
        
        Args:
            input_path (str): Path to the question image or PDF file
            question_image_path (str): Optional path to additional question image
            
        Returns:
            bool: True if successful, False otherwise
        """
        temp_files = []
        
        try:
            # Check if input is a PDF or image
            is_pdf = input_path.lower().endswith('.pdf')
            
            if is_pdf:
                # Verify PDF file exists
                if not os.path.exists(input_path):
                    logger.error(f"PDF file not found: {input_path}")
                    return False
                
                logger.info(f"🎯 Starting solution steps generation from PDF")
                logger.info(f"📁 PDF file: {input_path}")
                
                # Convert PDF to images
                images = self.convert_pdf_to_images(input_path)
                
                # Save images to temporary files
                image_paths = []
                for i, image in enumerate(images):
                    temp_file = self.save_image_to_temp(image, i)
                    temp_files.append(temp_file)
                    image_paths.append(temp_file)
                
            else:
                # Verify image file exists
                if not os.path.exists(input_path):
                    logger.error(f"Image file not found: {input_path}")
                    return False
                
                logger.info(f"🎯 Starting solution steps generation from image")
                logger.info(f"📁 Image file: {input_path}")
                
                image_paths = [input_path]
            
            # Add question image if provided
            if question_image_path:
                if not os.path.exists(question_image_path):
                    logger.error(f"Question image file not found: {question_image_path}")
                    return False
                
                logger.info(f"📁 Adding question image: {question_image_path}")
                image_paths.append(question_image_path)
            
            # Make API call
            api_result = self.make_gemini_api_call(image_paths)
            
            if not api_result["success"]:
                logger.error(f"❌ API call failed: {api_result['error']}")
                return False
            
            # Parse the two JSON outputs from the response
            standard_json, verbose_json = self.extract_both_json_from_response(api_result["content"])
            
            if standard_json is None or verbose_json is None:
                logger.error("❌ Failed to parse JSON outputs from API response")
                return False
            
            # Save the complete raw output as .txt file
            if not self.save_raw_output(api_result["content"]):
                logger.error("❌ Failed to save raw output")
                return False
            
            # Save the parsed JSON files
            if not self.save_parsed_json_files(standard_json, verbose_json):
                logger.error("❌ Failed to save parsed JSON files")
                return False
            
            logger.info("✅ Solution steps generation completed successfully!")
            logger.info(f"📁 Generated files:")
            logger.info(f"   - Raw TXT: /Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/math_solution_pipeline/math_solution_raw.txt")
            logger.info(f"   - Standard JSON: /Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/math_solution_pipeline/math_solution_standard.json")
            logger.info(f"   - Verbose JSON: /Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/math_solution_pipeline/math_solution_verbose.json")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error in solution steps generation: {e}")
            return False
        finally:
            # Clean up temporary files
            self.cleanup_temp_files(temp_files)

def main():
    """Main function to demonstrate the solution steps generation."""
    
    # Configuration - Choose your input type
    # For PDF + Question Image input:
    input_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Math_Solution/symbols.pdf"
    question_image_path = "geometry_questions/question_5.png"
    
    # For PDF only input (uncomment to use):
    # input_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Math_Solution/symbols.pdf"
    # question_image_path = None
    
    # For image only input (uncomment to use):
    # input_path = "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Math Questions/question_5.png"
    # question_image_path = None
    
    # Initialize the generator
    try:
        generator = SolutionStepsGenerator()
        logger.info("✅ Solution Steps Generator initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize generator: {e}")
        return
    
    # Generate solution steps
    logger.info("🎬 Starting solution steps generation...")
    success = generator.generate_solution_steps(input_path, question_image_path)
    
    if success:
        logger.info("✅ Solution steps generation completed successfully!")
        logger.info("📁 Generated file is ready for use")
    else:
        logger.error("❌ Solution steps generation failed!")

if __name__ == "__main__":
    main() 