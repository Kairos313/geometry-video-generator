#!/usr/bin/env python3
"""
Simple wrapper script to run the render and concatenate pipeline.
This script checks prerequisites and runs the main pipeline.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_prerequisites():
    """Check if required tools are installed."""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in the right directory
    if not Path("all_scenes.py").exists():
        print("❌ Error: all_scenes.py not found in current directory")
        print("   Please run this script from the Full_Pipeline directory")
        return False
    
    # Check if Manim is installed
    try:
        subprocess.run(['manim', '--version'], capture_output=True, check=True)
        print("✅ Manim is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Manim not found. Please install it:")
        print("   pip install manim")
        return False
    
    # Check if FFmpeg is installed
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found. Please install it:")
        print("   macOS: brew install ffmpeg")
        print("   Ubuntu: sudo apt install ffmpeg")
        print("   Windows: Download from https://ffmpeg.org/download.html")
        return False
    
    print("✅ All prerequisites met!")
    return True

def main():
    """Main function."""
    print("🚀 Geometry Scene Render Pipeline")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install missing tools.")
        sys.exit(1)
    
    # Run the main pipeline
    print("\n🎬 Starting render pipeline...")
    try:
        from render_and_concatenate_scenes import SceneRenderer
        renderer = SceneRenderer()
        success = renderer.run()
        
        if success:
            print("\n🎉 Pipeline completed successfully!")
            print("📹 Check final_geometry_video.mp4 for the result")
        else:
            print("\n❌ Pipeline failed. Check the error messages above.")
            sys.exit(1)
            
    except ImportError:
        print("❌ Could not import render_and_concatenate_scenes.py")
        print("   Make sure the file exists in the current directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
