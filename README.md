# Geometry_v2 - AI-Powered Mathematical Video Generation

This repository contains an advanced system for generating educational mathematical videos using AI and Manim (Mathematical Animation Engine).

## 🎯 Project Overview

Geometry_v2 is a sophisticated framework that combines:
- **AI-powered content generation** using multiple LLM providers (Claude, GPT, Gemini, DeepSeek)
- **Mathematical animation** using Manim
- **Audio synchronization** for educational content
- **Parallel processing** for efficient video generation

## 📁 Project Structure

```
Geometry_v2/
├── Audio/                    # Audio files for video narration
├── Blueprint/                # Scene blueprints and planning
├── Generated_Scenes/         # Generated Manim scene files
├── Manim Code/              # Core Manim animation code
├── Parallel_Outputs/        # Parallel processing outputs
├── Scene/                   # Scene-specific audio files
├── Video/                   # Final video outputs
├── *.py                     # Main Python scripts
├── *.json                   # Configuration and data files
└── *.png                    # Mathematical diagrams
```

## 🚀 Key Features

### 1. Multi-LLM Integration
- **Claude** (Anthropic)
- **GPT-4** (OpenAI)
- **Gemini** (Google)
- **DeepSeek**
- **OpenRouter** API support

### 2. Advanced Scene Generation
- Automated mathematical diagram creation
- Synchronized audio-visual content
- Pedagogical content structuring
- Parallel scene generation

### 3. Mathematical Animation
- Geometric figure rendering
- Theorem visualization
- Step-by-step proof animations
- Interactive mathematical concepts

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Manim
- OpenAI API key
- Anthropic API key (for Claude)
- Google API key (for Gemini)

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd Geometry_v2

# Install dependencies
pip install -r requirements.txt

# Set up API keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GOOGLE_API_KEY="your-google-key"
```

## 📖 Usage

### Basic Scene Generation
```python
# Generate a single scene
python generate_single_manim_scene_claude.py

# Generate all blueprints
python generate_all_blueprints_batch_v2.py

# Run the orchestrator
python geo_v3_orchestrator.py
```

### Parallel Processing
```python
# Generate scenes in parallel
python parallel_prompts.py
```

## 🎨 Customization

### Style Configuration
Edit `geo_v2_style.json` to customize:
- Color schemes
- Font sizes and styles
- Layout spacing
- Animation timing

### Content Generation
Modify prompt files to adjust:
- Mathematical content
- Pedagogical approach
- Animation complexity
- Audio narration style

## 📊 Output Formats

The system generates:
- **Manim scene files** (.py)
- **Audio files** (.mp3)
- **Video files** (.mp4)
- **JSON blueprints** for scene planning
- **Mathematical diagrams** (.png, .svg)

## 🔧 Configuration Files

- `geo_v2_style.json` - Visual styling configuration
- `deconstruct_parallel.json` - Scene structure and timing
- `all_blueprints_combined.json` - Complete scene blueprints
- `sentence.json` - Audio timing and content

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Manim Community** for the mathematical animation engine
- **OpenAI, Anthropic, Google** for AI capabilities
- **Mathematical community** for educational content inspiration

## 📞 Support

For questions or issues:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error logs and configuration details

---

**Note**: This project requires API keys for AI services. Please ensure you have valid API credentials before running the scripts. 