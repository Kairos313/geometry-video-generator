# Geometry Video Generation Pipeline

A comprehensive automated pipeline that transforms geometry question images into educational videos with step-by-step solutions, audio narration, and animated geometric visualizations.

## 🚀 Overview

This pipeline takes a geometry question image as input and generates a complete educational video with:
- **Step-by-step solution analysis** using AI
- **Audio narration** for each solution step
- **Animated geometric visualizations** using Manim
- **Synchronized audio-video** with proper timing
- **Professional video output** ready for educational use

## 📹 Video Examples

See the pipeline in action! Check out the example videos in the `video_examples/` directory:

- **Question 1-2 Combined** (6.4 MB): Combined solution for multiple geometry problems
- **Question 2** (3.8 MB): Focused solution for a single geometry problem  
- **With Pauses** (10 MB): Enhanced educational version with strategic pauses

These videos demonstrate the complete pipeline output with:
- ✅ **Professional audio narration** using ElevenLabs
- ✅ **Animated geometric constructions** using Manim
- ✅ **Step-by-step mathematical explanations**
- ✅ **Synchronized audio-video timing**

[📁 View Video Examples](./video_examples/)

## 🤖 AI Models & Performance

The pipeline uses different AI models for optimal performance at each step:

### **Step 1: Solution Analysis** 
- **Model**: Google Gemini 2.5 Pro
- **Purpose**: Analyze geometry questions and generate step-by-step solutions
- **Typical Performance**:
  - ⏱️ **Duration**: 80-90 seconds
  - 🎯 **Tokens**: ~15,000 total (5,000 input + 10,000 output)
  - 💰 **Cost**: ~$0.11 per question
    - Input: 5,000 tokens × $1.25/1M = $0.006
    - Output: 10,000 tokens × $10/1M = $0.10

### **Step 2: Audio Generation**
- **Model**: ElevenLabs Multilingual v2
- **Purpose**: Convert solution text to natural speech audio
- **Typical Performance**:
  - ⏱️ **Duration**: 10-15 seconds
  - 🎯 **Audio Files**: 250-300 individual audio segments
  - 💰 **Cost**: ~$0.05-0.10 per question

### **Step 3: Geometric Analysis**
- **Model**: Google Gemini 2.5 Pro (Blueprint) + Claude Sonnet 4 (Manim Code)
- **Purpose**: Convert solutions to geometric coordinates and generate basic Manim code
- **Typical Performance**:
  - ⏱️ **Duration**: 150-180 seconds
  - 🎯 **Tokens**: ~23,000 total (7,000 input + 16,000 output)
  - 💰 **Cost**: ~$0.26 per question
    - Gemini Input: 3,500 tokens × $1.25/1M = $0.004
    - Gemini Output: 8,000 tokens × $10/1M = $0.08
    - Claude Input: 3,500 tokens × $3/1M = $0.011
    - Claude Output: 8,000 tokens × $15/1M = $0.12

### **Step 4: Video Code Generation**
- **Model**: Anthropic Claude Sonnet 4
- **Purpose**: Generate comprehensive Manim scenes with audio integration
- **Typical Performance**:
  - ⏱️ **Duration**: 100-120 seconds
  - 🎯 **Tokens**: ~43,000 total (33,000 input + 10,000 output)
  - 💰 **Cost**: ~$0.15 per question
    - Input: 33,000 tokens × $3/1M = $0.099
    - Output: 10,000 tokens × $15/1M = $0.15

### **Step 5: Video Rendering**
- **Model**: None (Local Processing)
- **Purpose**: Render Manim animations and concatenate final video
- **Typical Performance**:
  - ⏱️ **Duration**: 140-160 seconds
  - 🎯 **Processing**: CPU/GPU intensive local rendering
  - 💰 **Cost**: $0.00 (local processing)

### **Total Pipeline Performance**
- ⏱️ **Total Duration**: 8-10 minutes per question
- 🎯 **Total Tokens**: ~123,000 tokens
- 💰 **Total Cost**: ~$0.67 per question
  - **Step 1 (Gemini)**: $0.11
  - **Step 2 (ElevenLabs)**: $0.05-0.10
  - **Step 3 (Gemini + Claude)**: $0.26
  - **Step 4 (Claude)**: $0.15
  - **Step 5 (Local)**: $0.00
- 🤖 **AI Models Used**: Gemini 2.5 Pro, Claude Sonnet 4, ElevenLabs

### **Why Different AI Models?**

**Google Gemini 2.5 Pro** (Steps 1 & 3 - Blueprint):
- ✅ **Excellent image analysis** for geometry questions
- ✅ **Strong mathematical reasoning** capabilities
- ✅ **Cost-effective** for large input processing
- ✅ **Fast response times** for coordinate calculations

**Anthropic Claude Sonnet 4** (Steps 3 & 4 - Code Generation):
- ✅ **Superior code generation** for Manim animations
- ✅ **Better understanding** of complex geometric concepts
- ✅ **More reliable** for structured output generation
- ✅ **Excellent** for multi-step reasoning tasks

**ElevenLabs Multilingual v2** (Step 2 - Audio):
- ✅ **Natural-sounding speech** synthesis
- ✅ **Mathematical pronunciation** support
- ✅ **Fast parallel processing** for multiple audio files
- ✅ **Cost-effective** for audio generation

## 🔍 Detailed Step-by-Step Pipeline Explanation

### **Step 1: Solution Analysis (`generate_solution_steps.py`)**

**Purpose**: Analyze geometry question images and generate comprehensive step-by-step solutions.

**Process**:
1. **Image Processing**:
   - Converts PDF to images (if needed) using `pdf2image`
   - Encodes images to base64 for API transmission
   - Supports multiple page questions

2. **AI Analysis**:
   - Uses **Google Gemini 2.5 Pro** via OpenRouter API
   - Applies `Solution_Steps_v3` prompt for structured analysis
   - Analyzes geometric elements, relationships, and solution strategies

3. **Output Generation**:
   - Creates two JSON files:
     - `math_solution_standard.json`: Concise solution steps
     - `math_solution_verbose.json`: Detailed explanations with LaTeX formatting
   - Each step includes:
     - Step ID and description
     - Mathematical reasoning
     - Geometric element identification
     - Solution methodology

**Key Features**:
- ✅ **Multi-page support** for complex questions
- ✅ **LaTeX formatting** for mathematical expressions
- ✅ **Structured output** with clear step progression
- ✅ **Error handling** for API failures

---

### **Step 2: Audio Generation (`geo_scriptwriter_parallel.py`)**

**Purpose**: Convert solution text into natural speech audio with precise timing.

**Process**:
1. **Text Processing**:
   - Parses solution JSON to extract individual sentences
   - Breaks down complex mathematical expressions
   - Handles LaTeX formatting for proper pronunciation

2. **Parallel Audio Generation**:
   - Uses **ElevenLabs Multilingual v2** API
   - Generates audio for each sentence concurrently (up to 5 parallel requests)
   - Voice ID: `Fahco4VZzobUeiPqni1S` (professional math voice)

3. **Audio Management**:
   - Creates individual audio files for each sentence
   - Stitches sentences into scene-level audio files
   - Calculates precise timing for video synchronization
   - Adds small gaps between sentences (0.01 seconds)

**Output Structure**:
- **Individual Audio**: `Audio/step_id_sentence_index.mp3`
- **Scene Audio**: `Scene/step_id_scene.mp3`
- **Timing Data**: `geometric_elements_with_timing.json`

**Key Features**:
- ✅ **Parallel processing** for speed
- ✅ **Mathematical pronunciation** support
- ✅ **Precise timing** calculations
- ✅ **Error recovery** for failed audio generation

---

### **Step 3: Geometric Analysis (`integrated_geometry_pipeline.py`)**

**Purpose**: Convert solution analysis into geometric coordinates and generate basic Manim code.

**Process**:
1. **Blueprint Generation** (Gemini 2.5 Pro):
   - Uses `Geometry_Blueprint_v2` prompt
   - Analyzes solution JSON to extract geometric elements
   - Calculates precise coordinates (3 decimal places)
   - Identifies geometric relationships and properties

2. **Coordinate Analysis**:
   - Maps geometric elements to coordinate system
   - Calculates distances, angles, and areas
   - Determines construction order and dependencies
   - Handles multi-part problems

3. **Basic Manim Code Generation** (Claude Sonnet 4):
   - Uses `Enhanced_Manim_Geometric_Surveyor_v2` prompt
   - Converts coordinate blueprint to Manim code
   - Creates basic geometric constructions
   - Includes animation timing placeholders

**Output Files**:
- `coordinates.txt`: Detailed geometric analysis
- `figure.py`: Basic Manim code with geometric elements

**Key Features**:
- ✅ **Precise coordinate calculations**
- ✅ **Multi-part problem support**
- ✅ **Geometric relationship mapping**
- ✅ **Construction order optimization**

---

### **Step 4: Video Code Generation (`video_claude.py`)**

**Purpose**: Generate comprehensive Manim scenes with audio integration and advanced animations.

**Process**:
1. **Data Integration**:
   - Combines all previous pipeline outputs:
     - Solution JSON (mathematical content)
     - Audio timing data (synchronization)
     - Geometric coordinates (visual elements)
     - Question image (context)

2. **Scene Generation** (Claude Sonnet 4):
   - Uses `ENHANCED_CODE_GENERATION_PROMPT_v4`
   - Creates multiple scenes for different solution parts
   - Integrates audio timing with animations
   - Generates professional-quality Manim code

3. **Code Validation**:
   - Validates Python syntax
   - Fixes common syntax issues automatically
   - Ensures Manim compatibility
   - Generates metadata for tracking

**Output Files**:
- `all_scenes.py`: Complete Manim code with all scenes
- `all_scenes_metadata.json`: Generation metadata and token usage

**Scene Types Generated**:
- **Part A/B/C scenes**: For multi-part problems
- **Solution step scenes**: Individual solution steps
- **Key takeaways scene**: Summary and conclusions
- **Introduction scene**: Problem overview

**Key Features**:
- ✅ **Audio-video synchronization**
- ✅ **Multi-scene support**
- ✅ **Professional animations**
- ✅ **Error handling and validation**

---

### **Step 5: Video Rendering (`render_and_concatenate_scenes.py`)**

**Purpose**: Render Manim animations and create final concatenated video.

**Process**:
1. **Scene Discovery**:
   - Automatically detects all scenes in `all_scenes.py`
   - Validates scene class definitions
   - Determines rendering order

2. **Sequential Rendering**:
   - Renders each scene individually using Manim
   - Quality: 480p15 (480p resolution, 15fps)
   - Handles rendering errors gracefully
   - Stops pipeline if critical scenes fail

3. **Audio Integration**:
   - Matches rendered videos with corresponding audio files
   - Handles naming conventions and file locations
   - Provides warnings for missing audio

4. **Video Concatenation**:
   - Uses FFmpeg to combine all scene videos
   - Maintains audio synchronization
   - Creates final output: `final_geometry_video.mp4`
   - Automatically opens video in default player

**Rendering Process**:
```bash
manim -pql all_scenes.py SceneName
```

**Output Files**:
- Individual scene videos in `media/videos/`
- Final concatenated video: `final_geometry_video.mp4`
- LaTeX files for mathematical expressions

**Key Features**:
- ✅ **Automatic scene detection**
- ✅ **Error recovery** for failed renders
- ✅ **Audio-video synchronization**
- ✅ **Professional output quality**

---

## 📋 Prerequisites

### System Requirements
- **Python 3.8+**
- **macOS/Linux/Windows** (tested on macOS)
- **FFmpeg** (for video processing)
- **LaTeX** (for mathematical expressions in Manim)

### API Keys Required
You'll need API keys for the following services:
- **OpenRouter API** (for Gemini and Claude AI models)
- **ElevenLabs API** (for text-to-speech audio generation)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Prompt Generation"
```

### 2. Install Python Dependencies

**Option A: Install from requirements.txt (recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Install manually**
```bash
# Core AI and API libraries
pip install openai
pip install python-dotenv
pip install requests

# Audio processing
pip install pydub
pip install aiohttp

# Video processing and animation
pip install manim
pip install moviepy

# Image and PDF processing
pip install pdf2image
pip install pillow

# Scientific computing
pip install numpy

# Additional utilities
pip install typing-extensions
```

**Required Python packages for each pipeline step:**

**Step 1 (generate_solution_steps.py):**
- `openai` - OpenRouter API client
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests for API calls
- `pdf2image` - PDF to image conversion
- `pillow` - Image processing (PIL)

**Step 2 (geo_scriptwriter_parallel.py):**
- `aiohttp` - Asynchronous HTTP client
- `pydub` - Audio file manipulation
- `python-dotenv` - Environment variable management

**Step 3 (integrated_geometry_pipeline.py):**
- `openai` - OpenRouter API client
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests for API calls

**Step 4 (video_claude.py):**
- `openai` - OpenRouter API client
- `python-dotenv` - Environment variable management

**Step 5 (render_and_concatenate_scenes.py):**
- `moviepy` - Video editing and concatenation
- `subprocess` - System command execution (built-in)

**Helper files:**
- `functions.py` - Requires `manim` and `numpy`
- `all_scenes.py` - Requires `manim`, `numpy`, and custom `functions`

**Built-in Python modules used:**
- `os` - Operating system interface
- `sys` - System-specific parameters
- `json` - JSON data handling
- `time` - Time-related functions
- `base64` - Base64 encoding/decoding
- `re` - Regular expressions
- `argparse` - Command-line argument parsing
- `logging` - Logging facility
- `subprocess` - Subprocess management
- `pathlib` - Object-oriented filesystem paths
- `typing` - Type hints
- `tempfile` - Temporary file operations
- `asyncio` - Asynchronous I/O

### 3. Install System Dependencies

**macOS:**
```bash
brew install ffmpeg
brew install poppler  # for pdf2image
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
sudo apt install poppler-utils
```

**Windows:**
- Download FFmpeg from https://ffmpeg.org/download.html
- Add to PATH environment variable

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
# Required API Keys
OPENROUTER_API_KEY=your_openrouter_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

## 🎯 Quick Start

### Run Complete Pipeline
```bash
cd "Geometry_v2/Geometry Test Questions/Full_Pipeline"
python terminal_pipeline.py --question-image "../Math Questions/question_4.png"
```

This will run all 5 steps automatically and generate a complete video.

## 📁 Pipeline Steps (Individual Execution)

The pipeline consists of 5 main steps that can be run individually:

### Step 1: Generate Solution Steps
**Script:** `generate_solution_steps.py`
**Purpose:** Analyzes the question image and generates step-by-step solution JSON files

```bash
python generate_solution_steps.py --question-image "../Math Questions/question_4.png"
```

**Outputs:**
- `math_solution_pipeline/math_solution_standard.json`
- `math_solution_pipeline/math_solution_verbose.json`

**What it does:**
- Uses Gemini AI to analyze the geometry question
- Extracts mathematical concepts and solution steps
- Generates structured JSON with solution breakdown

### Step 2: Generate Audio Files
**Script:** `geo_scriptwriter_parallel.py`
**Purpose:** Creates audio narration files for each solution step

```bash
python geo_scriptwriter_parallel.py
```

**Outputs:**
- `Audio/` directory with individual audio files
- `Scene/` directory with scene-specific audio files
- `geometric_elements_with_timing.json`

**What it does:**
- Converts solution steps to natural language scripts
- Generates audio using ElevenLabs text-to-speech
- Creates timing data for video synchronization

### Step 3: Generate Geometric Pipeline
**Script:** `integrated_geometry_pipeline.py`
**Purpose:** Creates geometric blueprint and basic Manim code

```bash
python integrated_geometry_pipeline.py --question-image "../Math Questions/question_4.png"
```

**Outputs:**
- `coordinates.txt` - Geometric coordinate analysis
- `figure.py` - Basic Manim visualization code

**What it does:**
- Uses Gemini AI to analyze geometric elements
- Generates coordinate mappings for the geometry
- Creates basic Manim code for visualization

### Step 4: Generate Comprehensive Video Code
**Script:** `video_claude.py`
**Purpose:** Creates complete Manim scenes with audio integration

```bash
python video_claude.py --question-image "../Math Questions/question_4.png"
```

**Outputs:**
- `all_scenes.py` - Complete Manim code with multiple scenes
- `all_scenes_metadata.json` - Generation metadata

**What it does:**
- Uses Claude AI to generate comprehensive Manim code
- Integrates all previous steps (solution, audio, geometry)
- Creates multiple scenes for different parts of the solution

### Step 5: Render Final Video
**Script:** `render_and_concatenate_scenes.py`
**Purpose:** Renders all scenes and creates final video

```bash
python render_and_concatenate_scenes.py
```

**Outputs:**
- `final_geometry_video.mp4` - Complete educational video

**What it does:**
- Renders each Manim scene individually
- Concatenates all scenes into final video
- Synchronizes audio with video timing
- Adds transitions between scenes

## 📂 File Structure

```
Full_Pipeline/
├── 📄 Core Scripts
│   ├── terminal_pipeline.py              # Main orchestrator
│   ├── generate_solution_steps.py        # Step 1: Solution analysis
│   ├── geo_scriptwriter_parallel.py      # Step 2: Audio generation
│   ├── integrated_geometry_pipeline.py   # Step 3: Geometry analysis
│   ├── video_claude.py                   # Step 4: Video code generation
│   └── render_and_concatenate_scenes.py  # Step 5: Video rendering
│
├── 🎨 Visualization
│   ├── functions.py                      # Geometric helper functions
│   ├── figure.py                         # Basic Manim code
│   └── all_scenes.py                     # Complete Manim scenes
│
├── 🎵 Audio
│   ├── Audio/                            # Individual audio files
│   └── Scene/                            # Scene-specific audio
│
├── 📊 Data
│   ├── math_solution_pipeline/           # Solution JSON files
│   ├── coordinates.txt                   # Geometric coordinates
│   ├── geometric_elements_with_timing.json
│   └── all_scenes_metadata.json
│
├── 🎬 Output
│   ├── media/                            # Manim rendered videos
│   └── final_geometry_video.mp4          # Final video
│
└── 📝 Prompts
    └── pipeline_prompts.py               # AI prompts for all steps
```

## 🔧 Key Files Explained

### Core Pipeline Scripts

**`terminal_pipeline.py`**
- Main orchestrator that runs all 5 steps sequentially
- Handles validation and error checking
- Tracks token usage and performance metrics
- Generates comprehensive logs

**`generate_solution_steps.py`**
- Uses Gemini AI to analyze geometry questions
- Extracts mathematical concepts and solution strategies
- Generates structured JSON with step-by-step breakdown
- Handles PDF symbol reference processing

**`geo_scriptwriter_parallel.py`**
- Converts solution steps to natural language scripts
- Generates audio using ElevenLabs API
- Creates timing data for video synchronization
- Processes geometric elements for animation

**`integrated_geometry_pipeline.py`**
- Uses Gemini AI for geometric analysis
- Generates coordinate mappings and geometric blueprints
- Creates basic Manim visualization code
- Handles both 2D and 3D geometry

**`video_claude.py`**
- Uses Claude AI to generate comprehensive Manim code
- Integrates solution, audio, and geometry data
- Creates multiple scenes for different solution parts
- Handles complex geometric animations

**`render_and_concatenate_scenes.py`**
- Renders individual Manim scenes
- Concatenates scenes with proper timing
- Synchronizes audio with video
- Handles video format and quality settings

### Helper Files

**`functions.py`**
- Geometric helper functions for Manim
- Angle arc creation (2D and 3D)
- Coordinate transformation utilities
- Animation timing helpers

**`pipeline_prompts.py`**
- AI prompts for all pipeline steps
- Structured prompts for consistent output
- Version-controlled prompt management

### Output Files

**`math_solution_standard.json`**
- Structured solution data
- Step-by-step breakdown
- Mathematical concepts and formulas

**`geometric_elements_with_timing.json`**
- Audio timing data
- Geometric element mappings
- Scene synchronization information

**`coordinates.txt`**
- Geometric coordinate analysis
- Point and line mappings
- Spatial relationships

**`all_scenes.py`**
- Complete Manim code
- Multiple scene classes
- Audio integration
- Professional animations

## 🎬 Video Output

The final video includes:
- **Step-by-step solution narration**
- **Animated geometric visualizations**
- **Mathematical expressions and formulas**
- **Professional transitions and timing**
- **Synchronized audio-video**
- **Educational annotations and highlights**

## 🔍 Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: OPENROUTER_API_KEY environment variable not set
```
**Solution:** Ensure your `.env` file is in the correct location and contains valid API keys.

**2. Manim Installation Issues**
```
ModuleNotFoundError: No module named 'manim'
```
**Solution:** Install Manim with `pip install manim`

**3. FFmpeg Not Found**
```
FileNotFoundError: ffmpeg not found
```
**Solution:** Install FFmpeg using your system's package manager.

**4. LaTeX Errors**
```
LaTeX compilation failed
```
**Solution:** Install a LaTeX distribution (TeX Live, MiKTeX, etc.)

### Performance Tips

- **Use SSD storage** for faster video rendering
- **Ensure sufficient RAM** (8GB+ recommended)
- **Monitor API usage** to avoid rate limits
- **Use lower quality settings** for testing (`-ql` instead of `-qh`)

## 📊 Token Usage

The pipeline tracks token usage across all AI models:
- **Gemini**: ~15K tokens (solution analysis)
- **Claude**: ~100K tokens (geometry and video generation)
- **Total**: ~120K tokens per complete run

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the pipeline logs
3. Verify API keys and dependencies
4. Check system requirements

---

**Happy Geometry Video Generation! 🎬📐** 

## 📝 Pipeline Prompts Overview

The `pipeline_prompts.py` file contains all the AI prompts used throughout the geometry pipeline. Each prompt is designed for a specific step and has evolved through multiple versions for improved performance.

### **Available Prompts by Pipeline Step**

#### **Step 1: Solution Analysis Prompts**
**Used by:** `generate_solution_steps.py`

**`Solution_Steps_v1`** - Initial version
- **Purpose:** Analyzes geometry questions and generates step-by-step solutions
- **Output:** Two separate JSON outputs (standard and verbose)
- **Features:** Khan Academy style explanations with LaTeX formatting

**`Solution_Steps_v2`** - Enhanced version
- **Purpose:** Improved solution analysis with better structure
- **Output:** Two separate JSON outputs with enhanced geometric elements
- **Features:** Better geometric element mapping and animation timing

**`Solution_Steps_v3`** - Current version ⭐
- **Purpose:** Streamlined solution analysis with unified output
- **Output:** Single JSON with `visual_output` and `tts_output` sections
- **Features:** 
  - 4-minute voiceover time limit (500 words max)
  - Proper LaTeX mathematical notation
  - Geometric element mapping for animations
  - TTS-friendly script generation

#### **Step 3: Geometry Analysis Prompts**
**Used by:** `integrated_geometry_pipeline.py`

**`Geometry_Blueprint_v1`** - Initial version
- **Purpose:** Converts solution JSON into geometric coordinate blueprint
- **Output:** Detailed coordinate analysis and geometric reconstruction
- **Features:** Multi-part problem support, precise coordinate calculations

**`Geometry_Blueprint_v2`** - Enhanced version
- **Purpose:** Improved geometric analysis with better coordinate system
- **Output:** Enhanced blueprint with better scale definition
- **Features:** Origin placement, axes alignment, scale definition

**`Geometry_Blueprint_v3`** - Advanced version
- **Purpose:** Advanced geometric analysis with 3D support
- **Output:** Comprehensive 3D coordinate system
- **Features:** 3D transformations, complex geometric calculations

**`Geometry_Blueprint_v2`** - Current version ⭐
- **Purpose:** Geometric analysis with coordinate system support
- **Output:** Geometric blueprint for Manim generation
- **Features:**
  - Multi-part problem handling
  - Precise coordinate calculations (3 decimal places)
  - Animation synchronization mapping
  - Status tracking (Given/Constructed/Calculated)

**`Geometry_Blueprint_v3`** - Experimental version (Coordinate Geometry)
- **Purpose:** Attempt to include coordinate plane drawing for coordinate geometry
- **Status:** ⚠️ **In Development** - Not fully functional
- **Note:** Coordinate geometry questions are not currently supported

**`Geometry_Blueprint_v4`** - Experimental version (Coordinate Geometry)
- **Purpose:** Further attempts at coordinate geometry system integration
- **Status:** ⚠️ **In Development** - Not fully functional
- **Note:** Coordinate geometry questions are not currently supported

#### **Step 3: Manim Code Generation Prompts**
**Used by:** `integrated_geometry_pipeline.py`

**`Enhanced_Manim_Geometric_Surveyor_v1`** - Initial version
- **Purpose:** Converts geometric blueprint into basic Manim code
- **Output:** Static Manim functions and classes
- **Features:** Pedagogical clarity, cinematic precision

**`Enhanced_Manim_Geometric_Surveyor_v2`** - Enhanced version
- **Purpose:** Improved Manim code generation with better structure
- **Output:** Enhanced Manim code with better organization
- **Features:** Better scene management, improved visual clarity

**`Enhanced_Manim_Geometric_Surveyor_v2`** - Current version ⭐
- **Purpose:** Manim code generation with geometric element support
- **Output:** Manim code with geometric element support
- **Features:**
  - Geometric element discovery
  - Multi-part problem handling
  - Inventory of geometric elements
  - Cross-reference between blueprint and solution JSON

**`Enhanced_Manim_Geometric_Surveyor_v3`** - Experimental version (Coordinate Geometry)
- **Purpose:** Attempt to include coordinate geometry system in Manim code
- **Status:** ⚠️ **In Development** - Not fully functional
- **Note:** Coordinate geometry questions are not currently supported

#### **Step 4: Comprehensive Video Code Generation Prompts**
**Used by:** `video_claude.py`

**`ENHANCED_CODE_GENERATION_PROMPT_v1`** - Initial version
- **Purpose:** Generates comprehensive Manim code with timing
- **Output:** Self-contained Manim code with hardcoded timing
- **Features:** JSON analysis during generation, pure Manim output

**`ENHANCED_CODE_GENERATION_PROMPT_v3`** - Enhanced version
- **Purpose:** Improved video code generation with better timing
- **Output:** Enhanced Manim code with better timing synchronization
- **Features:** Better audio-video synchronization, improved scene structure

**`ENHANCED_CODE_GENERATION_PROMPT_v4`** - Current version ⭐
- **Purpose:** Latest comprehensive video code generation
- **Output:** Complete Manim code with full pipeline integration
- **Features:**
  - Mandatory helper functions documentation
  - Universal scaling and positioning
  - Angle creation functions (2D and 3D)
  - Hardcoded timing from JSON data
  - One class per solution step
  - Sentence-based code organization

### **Prompt Evolution and Versioning**

Each prompt has evolved through multiple versions:

1. **v1** - Initial implementation with basic functionality
2. **v2** - Enhanced features and better structure
3. **v3** - Advanced capabilities and improved integration
4. **v4** - Current version with full pipeline optimization

### **How Prompts Work Together**

```
Question Image
    ↓
Solution_Steps_v3 (Step 1)
    ↓
[Solution JSON with geometric elements]
    ↓
Geometry_Blueprint_v2 (Step 3)
    ↓
[Geometric coordinate blueprint]
    ↓
Enhanced_Manim_Geometric_Surveyor_v2 (Step 3)
    ↓
[Basic Manim code]
    ↓
ENHANCED_CODE_GENERATION_PROMPT_v4 (Step 4)
    ↓
[Complete Manim scenes with audio integration]
```

### **⚠️ Important Limitations**

**Supported Geometry Types:**
- **✅ 2D Geometry**: Triangles, polygons, circles, angles, and 2D geometric constructions
- **✅ 3D Geometry**: Pyramids, polyhedra, 3D shapes, and spatial geometry
- **❌ Coordinate Geometry**: Not currently supported (experimental versions in development)

**Coordinate Geometry Support:**
- **Not Currently Supported**: The pipeline does not support coordinate geometry questions
- **Experimental Versions**: `Geometry_Blueprint_v3/v4` and `Enhanced_Manim_Geometric_Surveyor_v3` are experimental attempts
- **Status**: These versions are in development and not fully functional
- **Recommendation**: Use only the current stable versions for production

**Question Type Compatibility:**
- **✅ Pure Geometry**: Traditional geometric problems without coordinate systems
- **✅ Spatial Reasoning**: 3D visualization and spatial relationship problems
- **❌ Coordinate Systems**: Problems requiring x-y-z coordinate planes or grid systems
- **❌ Graphing**: Problems involving plotting points, lines, or curves on coordinate grids

### **Key Features Across All Prompts**

- **LaTeX Mathematical Notation**: All mathematical expressions use proper LaTeX syntax
- **Geometric Element Mapping**: Each prompt tracks geometric elements for animations
- **Multi-part Problem Support**: Handles complex problems with multiple subparts
- **Timing Synchronization**: Ensures audio and video are properly synchronized
- **Pedagogical Clarity**: Focuses on educational effectiveness and clear explanations
- **Precision**: Maintains mathematical accuracy and coordinate precision

### **Customization and Extension**

To modify or extend the prompts:

1. **Edit the prompt text** in `pipeline_prompts.py`
2. **Update the import statement** in the corresponding script
3. **Test with a sample question** to ensure compatibility
4. **Version control** your changes by creating new prompt versions

The prompts are designed to be modular and can be easily updated or extended for new use cases. 
# Video Examples

This directory contains example videos generated by the Geometry Video Generation Pipeline.

## 📹 Available Examples

### **1. Question 1 (`final_geometry_video_question_1.mp4`)**
- **Size**: 6.4 MB
- **Duration**: ~2-3 minutes
- **Content**: Combined solution for questions 1 and 2
- **Features**: 
  - Step-by-step geometric analysis
  - Audio narration
  - Animated geometric constructions
  - Mathematical calculations

### **2. Question 2 (`final_geometry_video_question_2.mp4`)**
- **Size**: 3.8 MB
- **Duration**: ~1-2 minutes
- **Content**: Solution for question 2 only
- **Features**:
  - Focused geometric problem solving
  - Clear audio explanations
  - Visual geometric demonstrations

### **3. With Pauses (`final_geometry_video_with_pauses.mp4`)**
- **Size**: 10 MB
- **Duration**: ~3-4 minutes
- **Content**: Enhanced version with strategic pauses
- **Features**:
  - Educational pacing with pauses
  - Extended explanations
  - Better learning flow
  - Comprehensive geometric analysis

## 🎬 Video Quality

All videos are rendered in **480p15** quality:
- **Resolution**: 480p
- **Frame Rate**: 15 FPS
- **Format**: MP4
- **Audio**: Synchronized narration

## 🔧 How These Were Generated

These videos were created using the complete pipeline:

1. **Step 1**: Solution analysis using Gemini 2.5 Pro
2. **Step 2**: Audio generation using ElevenLabs
3. **Step 3**: Geometric analysis and coordinate mapping
4. **Step 4**: Manim code generation using Claude Sonnet 4
5. **Step 5**: Video rendering and concatenation

## 📊 Performance Metrics

- **Total Processing Time**: 8-10 minutes per video
- **AI Token Usage**: ~123,000 tokens per video
- **Cost**: ~$0.67 per video
- **Output Quality**: Professional educational content

## 🚀 Try It Yourself

To generate your own geometry videos:

```bash
# Run the complete pipeline
python terminal_pipeline.py --question-image "path/to/your/question.png"

# Or run individual steps
python generate_solution_steps.py --question-image "path/to/your/question.png"
python geo_scriptwriter_parallel.py
python integrated_geometry_pipeline.py --question-image "path/to/your/question.png"
python video_claude.py --question-image "path/to/your/question.png"
python render_and_concatenate_scenes.py
```

## 📝 Notes

- These videos demonstrate the pipeline's capability to handle various geometry problems
- Each video shows different aspects of the solution process
- The "with pauses" version is optimized for educational viewing
- All videos include synchronized audio narration and visual animations
