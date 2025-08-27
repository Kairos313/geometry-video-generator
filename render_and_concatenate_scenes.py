#!/usr/bin/env python3
"""
Render and Concatenate All Scenes Script

This script automatically:
1. Reads all scene class names from all_scenes.py in the order they appear
2. Renders each scene in parallel using Manim with -ql quality (480p15)
3. Concatenates all rendered videos sequentially using ffmpeg with stream copy
4. Saves the final video as final_geometry_video.mp4 without re-encoding
5. Opens the final video in default media player for preview

Usage: python render_and_concatenate_scenes.py
"""

import subprocess
import sys
import os
import re
import ast
import asyncio
import concurrent.futures
from pathlib import Path
from typing import List, Tuple

class SceneRenderer:
    def __init__(self, scenes_file: str = "all_scenes.py"):
        self.scenes_file = scenes_file
        self.script_dir = Path(__file__).parent
        self.media_dir = self.script_dir / "media"
        self.output_video = self.script_dir / "final_geometry_video.mp4"
        
        # Ensure we're in the correct directory
        os.chdir(self.script_dir)
        
    def extract_scene_classes(self) -> List[str]:
        """
        Extract scene class names from all_scenes.py in the order they appear.
        Returns a list of scene class names.
        """
        print("🔍 Extracting scene classes from all_scenes.py...")
        
        try:
            with open(self.scenes_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all class definitions that inherit from Scene or ThreeDScene
            scene_pattern = r'class\s+(\w+Scene)\s*\((?:Scene|ThreeDScene)\):'
            matches = re.findall(scene_pattern, content)
            
            if not matches:
                raise ValueError("No scene classes found in all_scenes.py")
            
            print(f"✅ Found {len(matches)} scene classes:")
            for i, scene in enumerate(matches, 1):
                print(f"   {i}. {scene}")
            
            return matches
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Scene file not found: {self.scenes_file}")
        except Exception as e:
            raise Exception(f"Error reading scene file: {e}")
    
    def render_scene(self, scene_name: str) -> Tuple[str, bool]:
        """
        Render a single scene using Manim with -ql quality.
        Returns (scene_name, success_status).
        """
        print(f"🎬 Starting render for {scene_name}...")
        
        try:
            # Run manim command with -ql quality and disable caching to prevent conflicts
            cmd = [
                'manim', '-ql', '--disable_caching', self.scenes_file, scene_name
            ]
            
            print(f"   Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.script_dir
            )
            
            if result.returncode == 0:
                print(f"✅ Successfully rendered {scene_name}")
                return scene_name, True
            else:
                print(f"❌ Failed to render {scene_name}")
                print(f"   Error output: {result.stderr}")
                return scene_name, False
                
        except FileNotFoundError:
            print(f"❌ Manim not found. Please install Manim: pip install manim")
            return scene_name, False
        except Exception as e:
            print(f"❌ Error rendering {scene_name}: {e}")
            return scene_name, False
    
    def render_scenes_in_parallel(self, scene_names: List[str]) -> List[Tuple[str, bool]]:
        """
        Render multiple scenes in parallel using ThreadPoolExecutor.
        Returns list of (scene_name, success_status) tuples.
        Stops the entire process if any scene fails.
        """
        print(f"\n🎬 Rendering {len(scene_names)} scenes in parallel...")
        print("-" * 40)
        
        # Use ThreadPoolExecutor for parallel rendering
        # Note: Manim is not fully thread-safe, but we can try parallel rendering
        # If it causes issues, we can fall back to sequential rendering
        max_workers = min(len(scene_names), 4)  # Limit to 4 parallel renders
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all render tasks
            future_to_scene = {
                executor.submit(self.render_scene, scene_name): scene_name 
                for scene_name in scene_names
            }
            
            # Collect results as they complete
            results = []
            for future in concurrent.futures.as_completed(future_to_scene):
                scene_name = future_to_scene[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Check if this scene failed
                    if not result[1]:  # result[1] is the success status
                        print(f"❌ Scene {scene_name} failed. Stopping all renders...")
                        # Cancel all remaining futures
                        for remaining_future in future_to_scene:
                            if not remaining_future.done():
                                remaining_future.cancel()
                        # Wait for cancellations to complete
                        concurrent.futures.wait(future_to_scene, timeout=5)
                        return results  # Return partial results, will be handled in main loop
                        
                except Exception as e:
                    print(f"❌ Exception in {scene_name}: {e}")
                    results.append((scene_name, False))
                    # Cancel all remaining futures
                    for remaining_future in future_to_scene:
                        if not remaining_future.done():
                            remaining_future.cancel()
                    # Wait for cancellations to complete
                    concurrent.futures.wait(future_to_scene, timeout=5)
                    return results  # Return partial results, will be handled in main loop
        
        return results
    
    def find_rendered_video(self, scene_name: str) -> str:
        """
        Find the rendered video file for a scene.
        Returns the path to the video file.
        """
        # Manim creates videos in media/videos/scenes_file_name/quality/
        # The filename is typically scene_name.mp4
        
        # Look for the video file in the media directory (prioritize 480p15 for -ql)
        video_patterns = [
            self.media_dir / "videos" / self.scenes_file.replace('.py', '') / "480p15" / f"{scene_name}.mp4",
            self.media_dir / "videos" / self.scenes_file.replace('.py', '') / "720p30" / f"{scene_name}.mp4",
            self.media_dir / "videos" / self.scenes_file.replace('.py', '') / "1080p60" / f"{scene_name}.mp4",
        ]
        
        for pattern in video_patterns:
            if pattern.exists():
                return str(pattern)
        
        # If not found with standard patterns, search recursively
        for video_file in self.media_dir.rglob(f"{scene_name}.mp4"):
            return str(video_file)
        
        raise FileNotFoundError(f"Rendered video not found for {scene_name}")
    
    def create_concat_list(self, video_files: List[str]) -> str:
        """
        Create a temporary file list for ffmpeg concatenation.
        Returns the path to the temporary file list.
        """
        concat_list_path = self.script_dir / "concat_list.txt"
        
        with open(concat_list_path, 'w') as f:
            for video_file in video_files:
                # Escape single quotes and backslashes for ffmpeg
                escaped_path = video_file.replace("'", "'\"'\"'").replace("\\", "\\\\")
                f.write(f"file '{escaped_path}'\n")
        
        print(f"📝 Created concat list: {concat_list_path}")
        return str(concat_list_path)
    
    def concatenate_videos(self, concat_list_path: str) -> bool:
        """
        Concatenate videos using ffmpeg with -pql quality output.
        Returns True if successful, False otherwise.
        """
        print(f"🎬 Concatenating videos...")
        
        try:
            # Check if ffmpeg is available
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ FFmpeg not found. Please install FFmpeg:")
            print("   macOS: brew install ffmpeg")
            print("   Ubuntu: sudo apt install ffmpeg")
            print("   Windows: Download from https://ffmpeg.org/download.html")
            return False
        
        try:
            # Run ffmpeg command with simple stream copy (no re-encoding)
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_list_path,
                '-c', 'copy',            # Copy both video and audio streams without re-encoding
                str(self.output_video),
                '-y'  # Overwrite output file if it exists
            ]
            
            print(f"   Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.script_dir
            )
            
            if result.returncode == 0:
                print(f"✅ Successfully created final video: {self.output_video}")
                return True
            else:
                print(f"❌ Failed to concatenate videos")
                print(f"   Error output: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error concatenating videos: {e}")
            return False
    
    def cleanup_temp_files(self, concat_list_path: str):
        """Clean up temporary files."""
        try:
            if os.path.exists(concat_list_path):
                os.remove(concat_list_path)
                print(f"🧹 Cleaned up: {concat_list_path}")
        except Exception as e:
            print(f"⚠️  Warning: Could not clean up {concat_list_path}: {e}")
    
    def preview_final_video(self):
        """Preview the final concatenated video."""
        try:
            if not os.path.exists(self.output_video):
                print(f"❌ Final video not found: {self.output_video}")
                return False
            
            print(f"🎬 Previewing final video: {self.output_video}")
            
            # Use system default video player
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", str(self.output_video)])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", str(self.output_video)], shell=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(self.output_video)])
            
            print(f"✅ Video opened in default player")
            return True
            
        except Exception as e:
            print(f"❌ Error previewing video: {e}")
            return False
    
    def run(self):
        """Main execution function."""
        print("🚀 Starting scene rendering and concatenation pipeline...")
        print("📹 Reading scene classes from all_scenes.py, rendering in parallel, concatenating in file order")
        print("=" * 60)
        
        try:
            # Step 1: Extract scene classes from all_scenes.py in order
            scene_classes = self.extract_scene_classes()
            
            # Step 2: Render scenes in parallel
            render_results = self.render_scenes_in_parallel(scene_classes)
            
            # Step 3: Check if all scenes rendered successfully
            print(f"\n📹 Checking render results...")
            failed_scenes = []
            rendered_videos = []
            
            for scene_name in scene_classes:
                # Find the render result for this scene
                render_result = None
                for result_scene, success in render_results:
                    if result_scene == scene_name:
                        render_result = (result_scene, success)
                        break
                
                if render_result and render_result[1]:  # Success
                    try:
                        video_path = self.find_rendered_video(scene_name)
                        rendered_videos.append(video_path)
                        print(f"   ✅ {scene_name} -> {video_path}")
                    except FileNotFoundError as e:
                        print(f"   ❌ {e}. Scene {scene_name} failed.")
                        failed_scenes.append(scene_name)
                else:
                    print(f"   ❌ Failed to render {scene_name}.")
                    failed_scenes.append(scene_name)
            
            # Stop the entire process if any scene failed
            if failed_scenes:
                print(f"\n❌ {len(failed_scenes)} scenes failed to render:")
                for scene in failed_scenes:
                    print(f"   - {scene}")
                print("❌ Stopping entire process. All scenes must render successfully.")
                return False
            
            if not rendered_videos:
                print("❌ No videos were successfully rendered. Stopping execution.")
                return False
            
            # Step 4: Create concat list
            print(f"\n📝 Creating concatenation list...")
            concat_list_path = self.create_concat_list(rendered_videos)
            
            # Step 5: Concatenate videos (simple stream copy)
            print(f"\n🎬 Concatenating {len(rendered_videos)} videos...")
            print("📹 Simple concatenation without re-encoding")
            print("-" * 40)
            
            if not self.concatenate_videos(concat_list_path):
                print("❌ Failed to concatenate videos.")
                return False
            
            # Step 6: Cleanup
            self.cleanup_temp_files(concat_list_path)
            
            # Step 7: Preview final video
            print(f"\n🎬 Previewing final concatenated video...")
            self.preview_final_video()
            
            # Success!
            print("\n" + "=" * 60)
            print("🎉 Pipeline completed successfully!")
            print(f"📹 Final video: {self.output_video}")
            print(f"📊 Total scenes processed: {len(scene_classes)}")
            print(f"📊 Successfully rendered: {len(rendered_videos)}")
            print(f"🎬 Individual scenes: -ql (480p15)")
            print(f"🎬 Final video: Original quality (no re-encoding)")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Pipeline failed with error: {e}")
            return False

def main():
    """Main function."""
    renderer = SceneRenderer()
    success = renderer.run()
    
    if success:
        print("\n✅ All done! Check the final video file.")
        sys.exit(0)
    else:
        print("\n❌ Pipeline failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
