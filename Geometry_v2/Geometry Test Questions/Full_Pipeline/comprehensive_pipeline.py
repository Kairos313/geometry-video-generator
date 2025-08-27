#!/usr/bin/env python3
"""
Comprehensive Geometry Pipeline Script

This script orchestrates the entire geometry video generation workflow:
1. Generate solution step JSON files using generate_solution_steps.py
2. Run integrated_geometry_pipeline.py and geo_scriptwriter_parallel.py in parallel
3. Generate final video code using video_claude.py
4. Render all scenes in parallel using Manim
5. Render and concatenate all scenes into final video using render_and_concatenate_scenes.py

Usage: python comprehensive_pipeline.py [question_image] [output_name]
Example: python comprehensive_pipeline.py geometry_questions/question_2.png geometry_video_2
"""

import asyncio
import subprocess
import sys
import os
import time
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any
import json

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ComprehensivePipeline:
    def __init__(self, question_image: str = "geometry_questions/question_2.png", output_name: str = "geometry_video"):
        self.question_image = question_image
        self.output_name = output_name
        self.script_dir = Path(__file__).parent
        self.start_time = time.time()
        self.step_times = {}
        
        # Ensure we're in the correct directory
        os.chdir(self.script_dir)
        
        logger.info(f"🚀 Initializing Comprehensive Pipeline")
        logger.info(f"📁 Working directory: {self.script_dir}")
        logger.info(f"🖼️  Question image: {self.question_image}")
        logger.info(f"📹 Output name: {self.output_name}")
    
    def log_step_time(self, step_name: str, start_time: float):
        """Log the time taken for a step."""
        duration = time.time() - start_time
        self.step_times[step_name] = duration
        logger.info(f"⏱️  {step_name} completed in {duration:.2f} seconds")
    
    def check_file_exists(self, file_path: str, step_name: str) -> bool:
        """Check if a required file exists."""
        if not Path(file_path).exists():
            logger.error(f"❌ {step_name}: Required file not found: {file_path}")
            return False
        logger.info(f"✅ {step_name}: Found {file_path}")
        return True
    
    async def run_script_async(self, script_name: str, description: str) -> bool:
        """Run a Python script asynchronously."""
        logger.info(f"🔄 {description}: Starting {script_name}")
        start_time = time.time()
        
        try:
            # Run the script as a subprocess
            process = await asyncio.create_subprocess_exec(
                sys.executable, script_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"✅ {description}: {script_name} completed successfully")
                self.log_step_time(description, start_time)
                return True
            else:
                logger.error(f"❌ {description}: {script_name} failed with return code {process.returncode}")
                logger.error(f"   Error output: {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"❌ {description}: Error running {script_name}: {e}")
            return False
    
    def step_1_generate_solutions(self) -> bool:
        """Step 1: Generate solution step JSON files."""
        logger.info("=" * 60)
        logger.info("STEP 1: Generating Solution Step JSON Files")
        logger.info("=" * 60)
        
        # Check prerequisites
        if not self.check_file_exists(self.question_image, "Step 1"):
            return False
        
        start_time = time.time()
        
        try:
            # Run generate_solution_steps.py with the question image
            result = subprocess.run([
                sys.executable, "generate_solution_steps.py", self.question_image
            ], capture_output=True, text=True, cwd=self.script_dir)
            
            if result.returncode == 0:
                logger.info("✅ Step 1: Solution generation completed successfully")
                self.log_step_time("Step 1: Solution Generation", start_time)
                
                # Check output files
                required_files = [
                    "pipeline_outputs/solution_data/math_solution_standard.json",
                    "pipeline_outputs/solution_data/math_solution_verbose.json"
                ]
                
                for file_path in required_files:
                    if not self.check_file_exists(file_path, "Step 1 Output"):
                        return False
                
                return True
            else:
                logger.error(f"❌ Step 1: Solution generation failed")
                logger.error(f"   Error output: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Step 1: Error during solution generation: {e}")
            return False
    
    async def step_2_parallel_processing(self) -> bool:
        """Step 2: Run geometry pipeline and audio generation in parallel."""
        logger.info("=" * 60)
        logger.info("STEP 2: Parallel Processing (Geometry + Audio)")
        logger.info("=" * 60)
        
        # Check prerequisites
        required_files = [
            "pipeline_outputs/solution_data/math_solution_standard.json",
            "pipeline_outputs/solution_data/math_solution_verbose.json"
        ]
        
        for file_path in required_files:
            if not self.check_file_exists(file_path, "Step 2"):
                return False
        
        start_time = time.time()
        
        # Run both scripts in parallel
        tasks = [
            self.run_script_async("integrated_geometry_pipeline.py", "Geometry Pipeline"),
            self.run_script_async("geo_scriptwriter_parallel.py", "Audio Generation")
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check results
        success = True
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"❌ Step 2: Task {i} failed with exception: {result}")
                success = False
            elif not result:
                logger.error(f"❌ Step 2: Task {i} failed")
                success = False
        
        if success:
            logger.info("✅ Step 2: Parallel processing completed successfully")
            self.log_step_time("Step 2: Parallel Processing", start_time)
            
            # Check output files
            required_outputs = [
                "pipeline_outputs/geometry_data/coordinates.txt",
                "pipeline_outputs/geometry_data/figure.py",
                "pipeline_outputs/audio_data/geometric_elements_with_timing.json"
            ]
            
            for file_path in required_outputs:
                if not self.check_file_exists(file_path, "Step 2 Output"):
                    return False
            
            return True
        else:
            logger.error("❌ Step 2: Parallel processing failed")
            return False
    
    def step_3_generate_video_code(self) -> bool:
        """Step 3: Generate final video code."""
        logger.info("=" * 60)
        logger.info("STEP 3: Generating Final Video Code")
        logger.info("=" * 60)
        
        # Check prerequisites
        required_files = [
            "pipeline_outputs/geometry_data/coordinates.txt",
            "pipeline_outputs/geometry_data/figure.py",
            "pipeline_outputs/audio_data/geometric_elements_with_timing.json",
            "pipeline_outputs/solution_data/math_solution_standard.json"
        ]
        
        for file_path in required_files:
            if not self.check_file_exists(file_path, "Step 3"):
                return False
        
        start_time = time.time()
        
        try:
            # Run video_claude.py with the question image
            result = subprocess.run([
                sys.executable, "video_claude.py", self.question_image
            ], capture_output=True, text=True, cwd=self.script_dir)
            
            if result.returncode == 0:
                logger.info("✅ Step 3: Video code generation completed successfully")
                self.log_step_time("Step 3: Video Code Generation", start_time)
                
                # Check output files
                if not self.check_file_exists("pipeline_outputs/video_code/all_scenes.py", "Step 3 Output"):
                    return False
                
                return True
            else:
                logger.error(f"❌ Step 3: Video code generation failed")
                logger.error(f"   Error output: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Step 3: Error during video code generation: {e}")
            return False
    
    async def step_4_render_scenes_parallel(self) -> bool:
        """Step 4: Render all scenes in parallel and create final video."""
        logger.info("=" * 60)
        logger.info("STEP 4: Parallel Scene Rendering and Video Creation")
        logger.info("=" * 60)
        
        # Check prerequisites
        if not self.check_file_exists("pipeline_outputs/video_code/all_scenes.py", "Step 4"):
            return False
        
        start_time = time.time()
        
        try:
            # First, extract scene classes from the new location
            scene_classes = self.extract_scene_classes("pipeline_outputs/video_code/all_scenes.py")
            if not scene_classes:
                return False
            
            logger.info(f"🎬 Found {len(scene_classes)} scenes to render")
            
            # Render scenes in parallel
            render_tasks = []
            for scene_name in scene_classes:
                task = self.render_scene_async(scene_name, "pipeline_outputs/video_code/all_scenes.py")
                render_tasks.append(task)
            
            render_results = await asyncio.gather(*render_tasks, return_exceptions=True)
            
            # Check render results
            failed_scenes = []
            for i, result in enumerate(render_results):
                if isinstance(result, Exception):
                    logger.error(f"❌ Scene {scene_classes[i]} failed with exception: {result}")
                    failed_scenes.append(scene_classes[i])
                elif not result:
                    logger.error(f"❌ Scene {scene_classes[i]} failed to render")
                    failed_scenes.append(scene_classes[i])
            
            if failed_scenes:
                logger.error(f"❌ Failed to render scenes: {failed_scenes}")
                return False
            
            logger.info("✅ All scenes rendered successfully")
            
            # Create final video
            if not self.create_final_video():
                return False
            
            logger.info("✅ Step 4: Scene rendering and video creation completed successfully")
            self.log_step_time("Step 4: Scene Rendering and Video Creation", start_time)
            return True
            
        except Exception as e:
            logger.error(f"❌ Step 4: Error during scene rendering: {e}")
            return False
    
    def extract_scene_classes(self, file_path: str = "all_scenes.py") -> List[str]:
        """Extract scene class names from all_scenes.py."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all class definitions that inherit from Scene
            import re
            scene_pattern = r'class\s+(\w+Scene)\s*\(Scene\):'
            matches = re.findall(scene_pattern, content)
            
            if not matches:
                logger.error(f"❌ No scene classes found in {file_path}")
                return []
            
            logger.info(f"✅ Found {len(matches)} scene classes: {', '.join(matches)}")
            return matches
            
        except Exception as e:
            logger.error(f"❌ Error extracting scene classes: {e}")
            return []
    
    async def render_scene_async(self, scene_name: str, scene_file: str = "all_scenes.py") -> bool:
        """Render a single scene asynchronously."""
        logger.info(f"🎬 Rendering {scene_name}...")
        
        try:
            process = await asyncio.create_subprocess_exec(
                'manim', '-pql', scene_file, scene_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"✅ {scene_name} rendered successfully")
                return True
            else:
                logger.error(f"❌ {scene_name} failed to render")
                logger.error(f"   Error: {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error rendering {scene_name}: {e}")
            return False
    
    def step_5_render_and_concatenate(self) -> bool:
        """Step 5: Render and concatenate all scenes using the dedicated script."""
        logger.info("=" * 60)
        logger.info("STEP 5: Render and Concatenate All Scenes")
        logger.info("=" * 60)
        
        # Check prerequisites
        if not self.check_file_exists("pipeline_outputs/video_code/all_scenes.py", "Step 5"):
            return False
        
        start_time = time.time()
        
        try:
            # Run the render and concatenate script
            result = subprocess.run([
                sys.executable, "render_and_concatenate_scenes.py"
            ], capture_output=True, text=True, cwd=self.script_dir)
            
            if result.returncode == 0:
                logger.info("✅ Step 5: Render and concatenate completed successfully")
                self.log_step_time("Step 5: Render and Concatenate", start_time)
                
                # Check if final video was created
                if not self.check_file_exists("final_geometry_video.mp4", "Step 5 Output"):
                    return False
                
                return True
            else:
                logger.error(f"❌ Step 5: Render and concatenate failed")
                logger.error(f"   Error output: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Step 5: Error during render and concatenate: {e}")
            return False
    
    def create_final_video(self) -> bool:
        """Create the final concatenated video."""
        logger.info("🎬 Creating final concatenated video...")
        
        try:
            # Run the render pipeline
            result = subprocess.run([
                sys.executable, "run_render_pipeline.py"
            ], capture_output=True, text=True, cwd=self.script_dir)
            
            if result.returncode == 0:
                logger.info("✅ Final video created successfully")
                return True
            else:
                logger.error(f"❌ Failed to create final video")
                logger.error(f"   Error output: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error creating final video: {e}")
            return False
    
    def generate_summary(self):
        """Generate a comprehensive summary of the pipeline execution."""
        total_time = time.time() - self.start_time
        
        logger.info("=" * 60)
        logger.info("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        
        logger.info("📊 EXECUTION SUMMARY:")
        logger.info(f"   Total execution time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
        
        logger.info("\n⏱️  STEP TIMINGS:")
        for step_name, duration in self.step_times.items():
            logger.info(f"   {step_name}: {duration:.2f} seconds")
        
        logger.info("\n📁 GENERATED FILES:")
        generated_files = [
            "pipeline_outputs/solution_data/math_solution_standard.json",
            "pipeline_outputs/solution_data/math_solution_verbose.json",
            "pipeline_outputs/geometry_data/coordinates.txt",
            "pipeline_outputs/geometry_data/figure.py",
            "pipeline_outputs/geometry_data/geometric_elements_with_timing.json",
            "pipeline_outputs/video_code/all_scenes.py",
            "pipeline_outputs/audio_data/deconstruct_parallel_symbols.json",
            "pipeline_outputs/audio_data/geometric_elements_with_timing.json",
            "final_geometry_video.mp4"
        ]
        
        for file_path in generated_files:
            if Path(file_path).exists():
                size = Path(file_path).stat().st_size
                logger.info(f"   ✅ {file_path} ({size:,} bytes)")
            else:
                logger.info(f"   ❌ {file_path} (not found)")
        
        logger.info(f"\n🎬 FINAL OUTPUT:")
        logger.info(f"   📹 Final video: final_geometry_video.mp4")
        logger.info(f"   📊 Pipeline log: pipeline.log")
        
        logger.info("\n" + "=" * 60)
    
    async def run(self) -> bool:
        """Run the complete pipeline."""
        logger.info("🚀 Starting Comprehensive Geometry Pipeline")
        logger.info(f"📅 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Step 1: Generate solutions
            if not self.step_1_generate_solutions():
                logger.error("❌ Pipeline failed at Step 1")
                return False
            
            # Step 2: Parallel processing
            if not await self.step_2_parallel_processing():
                logger.error("❌ Pipeline failed at Step 2")
                return False
            
            # Step 3: Generate video code
            if not self.step_3_generate_video_code():
                logger.error("❌ Pipeline failed at Step 3")
                return False
            
            # Step 4: Render scenes and create final video
            if not await self.step_4_render_scenes_parallel():
                logger.error("❌ Pipeline failed at Step 4")
                return False
            
            # Step 5: Render and concatenate all scenes
            if not self.step_5_render_and_concatenate():
                logger.error("❌ Pipeline failed at Step 5")
                return False
            
            # Generate summary
            self.generate_summary()
            return True
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed with unexpected error: {e}")
            return False

def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(description="Comprehensive Geometry Pipeline")
    parser.add_argument(
        "question_image",
        nargs="?",
        default="geometry_questions/question_2.png",
        help="Path to the question image (default: geometry_questions/question_2.png)"
    )
    parser.add_argument(
        "output_name",
        nargs="?",
        default="geometry_video",
        help="Name for the output video (default: geometry_video)"
    )
    
    args = parser.parse_args()
    
    # Create and run pipeline
    pipeline = ComprehensivePipeline(args.question_image, args.output_name)
    
    # Run the pipeline
    success = asyncio.run(pipeline.run())
    
    if success:
        logger.info("🎉 Pipeline completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Pipeline failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
