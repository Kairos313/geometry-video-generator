import json
import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from typing import Dict, Any, Optional

# Import the enhanced blueprint generator
from generate_all_blueprints_batch_v2 import EnhancedBlueprintGenerator

# --- CONFIGURATION ---
INPUT_PATH = "Geometry_v2/deconstruct_parallel.json"
STYLE_PATH = "Geometry_v2/geo_v2_style.json"
IMAGE_PATH = "Geometry_v2/math_question.png"  # Set to None if not using image
TEST_SCENE_INDEX = 0  # Test the first scene (change this to test different scenes)
OUTPUT_DIR = "Geometry_v2/Test_Blueprint_Output"

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# --- LOAD API KEY ---
load_dotenv(".env")
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise RuntimeError("GOOGLE_API_KEY not found in environment.")
genai.configure(api_key=google_api_key)

def test_single_blueprint_generation():
    """Test blueprint generation for a single scene."""
    
    # Load input data
    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            input_data = json.load(f)
        steps = input_data.get('solution_steps', [])
        if not steps:
            raise ValueError("No solution_steps found in input file.")
        
        with open(STYLE_PATH, "r", encoding="utf-8") as f:
            style_config = json.load(f)
        
        # Load image if provided
        image_obj = None
        if IMAGE_PATH and Path(IMAGE_PATH).exists():
            image_obj = Image.open(IMAGE_PATH)
            logger.info(f"Loaded image: {IMAGE_PATH}")
        
    except Exception as e:
        logger.error(f"Error loading input files: {e}")
        return
    
    # Validate scene index
    if TEST_SCENE_INDEX >= len(steps):
        logger.error(f"Scene index {TEST_SCENE_INDEX} is out of range. Total scenes: {len(steps)}")
        return
    
    # Get the test scene
    test_step = steps[TEST_SCENE_INDEX]
    scene_id = test_step.get('scene_id', f'scene_{TEST_SCENE_INDEX}')
    
    logger.info(f"Testing blueprint generation for scene {TEST_SCENE_INDEX}: {scene_id}")
    logger.info(f"Scene content: {json.dumps(test_step, indent=2)}")
    
    # Initialize generator
    generator = EnhancedBlueprintGenerator()
    
    # Create output directory
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test API connectivity first
    print(f"\n=== TESTING API CONNECTIVITY ===")
    try:
        test_start = time.time()
        test_response = generator.model.generate_content("Hello, this is a test message.")
        test_time = time.time() - test_start
        
        print(f"✅ API connectivity test successful")
        print(f"   Test response time: {test_time:.2f} seconds")
        print(f"   Response type: {type(test_response)}")
        print(f"   Response has text: {hasattr(test_response, 'text')}")
        
    except Exception as e:
        print(f"❌ API connectivity test failed: {str(e)}")
        return
    
    # Generate blueprint with detailed timing
    print(f"\n=== GENERATING BLUEPRINT ===")
    total_start_time = time.time()
    
    try:
        # Time the blueprint generation process
        blueprint_start_time = time.time()
        blueprint = generator.generate_blueprint(test_step, TEST_SCENE_INDEX, style_config)
        blueprint_time = time.time() - blueprint_start_time
        
        total_time = time.time() - total_start_time
        
        print(f"Blueprint generation process took {blueprint_time:.2f} seconds")
        print(f"Total time including setup: {total_time:.2f} seconds")
        
        if blueprint:
            # Save blueprint
            output_path = output_dir / f"test_scene_{TEST_SCENE_INDEX}_{scene_id}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(blueprint, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Successfully generated and saved blueprint: {output_path}")
            
            # Print detailed summary
            print(f"\n=== BLUEPRINT GENERATION SUMMARY ===")
            print(f"Scene ID: {scene_id}")
            print(f"API Call Time: {blueprint_time:.2f} seconds")
            print(f"Total Process Time: {total_time:.2f} seconds")
            print(f"Output File: {output_path}")
            print(f"Number of Mobjects: {len(blueprint.get('mobjects', []))}")
            print(f"Number of Animation Steps: {len(blueprint.get('animation_flow', []))}")
            print(f"Initial Mobjects: {blueprint.get('initial_mobjects', [])}")
            
            # Show a preview of the blueprint
            print(f"\n=== BLUEPRINT PREVIEW ===")
            blueprint_json = json.dumps(blueprint, indent=2)
            if len(blueprint_json) > 2000:
                print(blueprint_json[:2000] + "...")
                print(f"\n[Blueprint truncated. Full blueprint saved to: {output_path}]")
            else:
                print(blueprint_json)
            
        else:
            logger.error("❌ Failed to generate blueprint")
            print(f"\n❌ BLUEPRINT GENERATION FAILED")
            print(f"Scene ID: {scene_id}")
            print(f"API Call Time: {blueprint_time:.2f} seconds")
            print(f"Total Process Time: {total_time:.2f} seconds")
            
    except Exception as e:
        total_time = time.time() - total_start_time
        logger.error(f"Error during blueprint generation: {e}")
        print(f"\n❌ BLUEPRINT GENERATION ERROR")
        print(f"Scene ID: {scene_id}")
        print(f"Total Process Time: {total_time:.2f} seconds")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        
        # Provide more detailed error information
        if "quota" in str(e).lower():
            print(f"💡 This appears to be a quota/rate limit issue")
        elif "authentication" in str(e).lower() or "api_key" in str(e).lower():
            print(f"💡 This appears to be an authentication issue")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            print(f"💡 This appears to be a network connectivity issue")

def test_api_call_directly():
    """Test a direct API call to verify connectivity and timing."""
    print(f"\n=== DIRECT API CALL TEST ===")
    
    try:
        # Initialize generator to get the model
        generator = EnhancedBlueprintGenerator()
        
        # Simple test prompt
        test_prompt = "Generate a simple JSON object with a 'test' field set to 'success'"
        
        print(f"Making direct API call with prompt: {test_prompt}")
        
        # Time the API call
        start_time = time.time()
        response = generator.model.generate_content(test_prompt)
        api_time = time.time() - start_time
        
        print(f"✅ Direct API call successful")
        print(f"   API call time: {api_time:.2f} seconds")
        print(f"   Response type: {type(response)}")
        print(f"   Response has text: {hasattr(response, 'text')}")
        
        if hasattr(response, 'text'):
            print(f"   Response text: {response.text[:200]}...")
        else:
            print(f"   Response content: {str(response)[:200]}...")
            
    except Exception as e:
        print(f"❌ Direct API call failed: {str(e)}")
        print(f"   Error type: {type(e).__name__}")

def test_multiple_scenes():
    """Test blueprint generation for multiple scenes."""
    
    # Load input data
    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            input_data = json.load(f)
        steps = input_data.get('solution_steps', [])
        if not steps:
            raise ValueError("No solution_steps found in input file.")
        
        with open(STYLE_PATH, "r", encoding="utf-8") as f:
            style_config = json.load(f)
        
    except Exception as e:
        logger.error(f"Error loading input files: {e}")
        return
    
    # Initialize generator
    generator = EnhancedBlueprintGenerator()
    
    # Create output directory
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test scenes 0, 1, and 2
    test_scenes = [0, 1, 2]
    
    print(f"\n=== TESTING MULTIPLE SCENES ===")
    print(f"Testing scenes: {test_scenes}")
    
    results = []
    
    for scene_index in test_scenes:
        if scene_index >= len(steps):
            logger.warning(f"Scene index {scene_index} is out of range. Skipping.")
            continue
        
        test_step = steps[scene_index]
        scene_id = test_step.get('scene_id', f'scene_{scene_index}')
        
        print(f"\n--- Testing Scene {scene_index}: {scene_id} ---")
        
        start_time = time.time()
        
        try:
            blueprint = generator.generate_blueprint(test_step, scene_index, style_config)
            generation_time = time.time() - start_time
            
            if blueprint:
                # Save blueprint
                output_path = output_dir / f"test_scene_{scene_index}_{scene_id}.json"
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(blueprint, f, indent=2, ensure_ascii=False)
                
                result = {
                    'scene_index': scene_index,
                    'scene_id': scene_id,
                    'status': 'SUCCESS',
                    'time': generation_time,
                    'mobjects_count': len(blueprint.get('mobjects', [])),
                    'animations_count': len(blueprint.get('animation_flow', [])),
                    'output_path': str(output_path)
                }
                
                print(f"✅ Success: {generation_time:.2f}s, {len(blueprint.get('mobjects', []))} mobjects, {len(blueprint.get('animation_flow', []))} animations")
                
            else:
                result = {
                    'scene_index': scene_index,
                    'scene_id': scene_id,
                    'status': 'FAILED',
                    'time': generation_time,
                    'error': 'No blueprint generated'
                }
                
                print(f"❌ Failed: {generation_time:.2f}s")
                
        except Exception as e:
            generation_time = time.time() - start_time
            result = {
                'scene_index': scene_index,
                'scene_id': scene_id,
                'status': 'ERROR',
                'time': generation_time,
                'error': str(e)
            }
            
            print(f"❌ Error: {generation_time:.2f}s - {str(e)}")
        
        results.append(result)
    
    # Print summary
    print(f"\n=== TEST SUMMARY ===")
    successful = [r for r in results if r['status'] == 'SUCCESS']
    failed = [r for r in results if r['status'] != 'SUCCESS']
    
    print(f"Successful: {len(successful)}/{len(results)}")
    print(f"Failed: {len(failed)}/{len(results)}")
    
    if successful:
        avg_time = sum(r['time'] for r in successful) / len(successful)
        print(f"Average generation time: {avg_time:.2f} seconds")
    
    if failed:
        print(f"\nFailed scenes:")
        for result in failed:
            print(f"  Scene {result['scene_index']} ({result['scene_id']}): {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    print("=== SINGLE SCENE BLUEPRINT GENERATION TEST ===")
    print(f"Testing scene index: {TEST_SCENE_INDEX}")
    print(f"Input file: {INPUT_PATH}")
    print(f"Style file: {STYLE_PATH}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Model: gemini-2.5-flash")
    
    # Test API connectivity first
    test_api_call_directly()
    
    # Test single scene
    test_single_blueprint_generation()
    
    # Uncomment the line below to test multiple scenes
    # test_multiple_scenes() 