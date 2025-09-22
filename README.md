# Geometry Video Generation Pipeline

An automated AI-powered pipeline that transforms geometry question images into professional educational videos with step-by-step solutions, audio narration, and animated visualizations.

## 🚀 Overview

The pipeline processes geometry questions through 5 integrated steps, leveraging multiple AI models for optimal performance:

1. **Solution Analysis** (Gemini 2.5 Pro) - Extracts mathematical concepts and solution strategies
2. **Audio Generation** (ElevenLabs) - Creates natural speech narration for each step
3. **Geometric Analysis** (Gemini + Claude) - Maps solutions to precise coordinates and generates basic visualizations
4. **Video Code Generation** (Claude Sonnet 4) - Creates comprehensive Manim scenes with audio integration
5. **Video Rendering** (Local) - Renders final educational video with synchronized audio

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API keys in .env file
OPENROUTER_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here

# Run complete pipeline
python terminal_pipeline.py --question-image "path/to/question.png"
```

## 🤖 AI Model Performance

### **Step 1: Solution Analysis** 
- **Model**: Google Gemini 2.5 Pro
- **Performance**: 80-90 seconds, ~15K tokens, ~$0.11 per question
- **Capability**: Analyzes geometry questions and generates structured step-by-step solutions with LaTeX formatting

### **Step 2: Audio Generation**
- **Model**: ElevenLabs Multilingual v2
- **Performance**: 10-15 seconds, 250-300 audio segments, ~$0.05-0.10 per question
- **Capability**: Converts solution text to natural speech with mathematical pronunciation support

### **Step 3: Geometric Analysis**
- **Models**: Gemini 2.5 Pro (Blueprint) + Claude Sonnet 4 (Manim Code)
- **Performance**: 150-180 seconds, ~23K tokens, ~$0.26 per question
- **Capability**: Converts solutions to precise geometric coordinates and generates basic Manim visualizations

### **Step 4: Video Code Generation**
- **Model**: Anthropic Claude Sonnet 4
- **Performance**: 100-120 seconds, ~43K tokens, ~$0.15 per question
- **Capability**: Generates comprehensive Manim scenes with audio integration and professional animations

### **Step 5: Video Rendering**
- **Processing**: Local (CPU/GPU)
- **Performance**: 140-160 seconds, $0.00 cost
- **Capability**: Renders Manim animations and creates final synchronized video

**Total Pipeline**: 8-10 minutes, ~123K tokens, ~$0.67 per question

## 📁 Pipeline Architecture

```
Input: Geometry Question Image
    ↓
Step 1: generate_solution_steps.py
    ↓ [Solution JSON with geometric elements]
Step 2: geo_scriptwriter_parallel.py
    ↓ [Audio files + timing data]
Step 3: integrated_geometry_pipeline.py
    ↓ [Geometric coordinates + basic Manim code]
Step 4: video_claude.py
    ↓ [Complete Manim scenes with audio integration]
Step 5: render_and_concatenate_scenes.py
    ↓
Output: Professional Educational Video
```

## 🎬 Output Quality

The pipeline generates professional educational videos featuring:

- **Step-by-step mathematical explanations** with LaTeX-formatted expressions
- **Animated geometric constructions** using Manim's precise rendering engine
- **Natural speech narration** with mathematical pronunciation support
- **Synchronized audio-video timing** for seamless educational experience
- **Multi-scene support** for complex multi-part problems
- **Professional transitions** and visual annotations

## 🛠️ Technical Capabilities

### **Supported Geometry Types**
- ✅ **2D Geometry**: Triangles, polygons, circles, angles, and geometric constructions
- ✅ **3D Geometry**: Pyramids, polyhedra, 3D shapes, and spatial relationships
- ❌ **Coordinate Geometry**: Not currently supported (experimental versions in development)

### **AI Model Selection Rationale**

**Google Gemini 2.5 Pro** (Steps 1 & 3):
- Excellent image analysis for geometry questions
- Strong mathematical reasoning capabilities
- Cost-effective for large input processing
- Fast response times for coordinate calculations

**Anthropic Claude Sonnet 4** (Steps 3 & 4):
- Superior code generation for Manim animations
- Better understanding of complex geometric concepts
- More reliable for structured output generation
- Excellent for multi-step reasoning tasks

**ElevenLabs Multilingual v2** (Step 2):
- Natural-sounding speech synthesis
- Mathematical pronunciation support
- Fast parallel processing for multiple audio files
- Cost-effective for audio generation

## 📊 Performance Metrics

### **Token Usage Breakdown**
- **Gemini**: ~15K tokens (solution analysis)
- **Claude**: ~100K tokens (geometry and video generation)
- **Total**: ~120K tokens per complete run

### **Cost Analysis**
- **Step 1 (Gemini)**: $0.11
- **Step 2 (ElevenLabs)**: $0.05-0.10
- **Step 3 (Gemini + Claude)**: $0.26
- **Step 4 (Claude)**: $0.15
- **Step 5 (Local)**: $0.00
- **Total**: ~$0.67 per question

## 🛠️ Installation

### **System Requirements**
- Python 3.8+
- FFmpeg (for video processing)
- LaTeX (for mathematical expressions)
- 8GB+ RAM recommended

### **Dependencies**
```bash
# Core AI and API libraries
pip install openai python-dotenv requests

# Audio processing
pip install pydub aiohttp

# Video processing and animation
pip install manim moviepy

# Image and PDF processing
pip install pdf2image pillow

# Scientific computing
pip install numpy
```

### **System Dependencies**
```bash
# macOS
brew install ffmpeg poppler

# Ubuntu/Debian
sudo apt install ffmpeg poppler-utils
```

## 🎯 Individual Step Execution

```bash
# Step 1: Generate solution analysis
python generate_solution_steps.py --question-image "question.png"

# Step 2: Generate audio files
python geo_scriptwriter_parallel.py

# Step 3: Generate geometric pipeline
python integrated_geometry_pipeline.py --question-image "question.png"

# Step 4: Generate comprehensive video code
python video_claude.py --question-image "question.png"

# Step 5: Render final video
python render_and_concatenate_scenes.py
```

## 📂 Key Output Files

- **`math_solution_standard.json`**: Structured solution data with step-by-step breakdown
- **`geometric_elements_with_timing.json`**: Audio timing data and geometric element mappings
- **`coordinates.txt`**: Geometric coordinate analysis and spatial relationships
- **`all_scenes.py`**: Complete Manim code with multiple scenes and audio integration
- **`final_geometry_video.mp4`**: Professional educational video output

## 🔧 Troubleshooting

### **Common Issues**
- **API Key Errors**: Ensure `.env` file contains valid `OPENROUTER_API_KEY` and `ELEVENLABS_API_KEY`
- **Manim Installation**: Install with `pip install manim`
- **FFmpeg Not Found**: Install using system package manager
- **LaTeX Errors**: Install LaTeX distribution (TeX Live, MiKTeX, etc.)

### **Performance Tips**
- Use SSD storage for faster video rendering
- Monitor API usage to avoid rate limits
- Use lower quality settings for testing (`-ql` instead of `-qh`)

## 🎓 Educational Value

The pipeline creates videos that enhance learning through:

- **Visual Learning**: Animated geometric constructions help students understand spatial relationships
- **Audio Reinforcement**: Natural speech narration reinforces mathematical concepts
- **Step-by-Step Progression**: Clear solution breakdown prevents cognitive overload
- **Professional Quality**: High-quality output suitable for educational institutions
- **Scalable Production**: Automated pipeline enables rapid creation of educational content

---

**Transform geometry questions into engaging educational videos with AI-powered precision and professional quality.**
