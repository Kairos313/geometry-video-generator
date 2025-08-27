# 🎯 AI Geometry Video Solution

A comprehensive web application that generates educational geometry videos from uploaded mathematical problem images using AI-powered content generation, audio synthesis, and geometric animations.

## 🚀 Features

- **AI-Powered Solution Generation**: Automatically generates step-by-step mathematical solutions
- **Audio Synthesis**: Creates natural-sounding voiceovers for explanations
- **Geometric Animations**: Synchronized visual animations using Manim
- **Real-time Progress Tracking**: Live progress updates during video generation
- **Modern Web Interface**: Beautiful, responsive frontend with drag-and-drop upload
- **Video Controls**: Full video player with speed controls (0.75x - 2.0x)

## 📁 Project Structure

```
geometry-flow/
├── frontend/              # Lovable frontend (React/Vite)
├── backend/               # Flask server + pipeline
│   ├── server.py         # Main Flask application
│   ├── requirements.txt  # Python dependencies
│   ├── .env             # Environment variables
│   ├── pipeline/        # All pipeline scripts
│   ├── Final_Videos/    # Generated videos
│   └── geometry_questions/ # Uploaded images
└── README.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- FFmpeg (for video processing)
- Manim (for geometric animations)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the backend directory with your API keys:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key
   ELEVEN_LABS_API_KEY=your_elevenlabs_api_key
   ```

4. **Install Manim:**
   ```bash
   pip install manim
   ```

5. **Install FFmpeg:**
   - **macOS:** `brew install ffmpeg`
   - **Ubuntu:** `sudo apt install ffmpeg`
   - **Windows:** Download from https://ffmpeg.org/

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## 🚀 Running the Application

### Development Mode

1. **Start the backend server:**
   ```bash
   cd backend
   python server.py
   ```
   The server will run on `http://localhost:5000`

2. **Start the frontend (optional - backend serves the frontend):**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the application:**
   Open your browser and go to `http://localhost:5000`

### Production Mode

1. **Build the frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Start the backend server:**
   ```bash
   cd backend
   python server.py
   ```

## 📖 Usage

1. **Upload Image**: Drag and drop or click to upload a geometry problem image
2. **Generate Video**: Click the "Generate Video" button to start processing
3. **Monitor Progress**: Watch the progress bar as the AI processes your image
4. **View Result**: The generated video will automatically play when ready
5. **Video Controls**: Use the video player controls to pause, play, seek, and adjust speed

## 🔧 Pipeline Overview

The application uses a comprehensive 4-step pipeline:

1. **Solution Generation**: AI analyzes the image and generates step-by-step solutions
2. **Parallel Processing**: Geometry analysis and audio generation run simultaneously
3. **Video Code Generation**: Creates Manim animation code with timing synchronization
4. **Scene Rendering**: Renders all scenes in parallel and concatenates into final video

## 🎨 Supported File Types

- **Images**: PNG, JPG, JPEG, GIF, BMP, TIFF
- **Output**: MP4 video files

## 🔒 Security Features

- File type validation
- Unique filename generation with timestamps
- Temporary file cleanup after processing
- Error handling and user feedback

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your `.env` file contains valid API keys
2. **FFmpeg Not Found**: Install FFmpeg and ensure it's in your system PATH
3. **Manim Installation**: Some systems may require additional dependencies for Manim
4. **Memory Issues**: Large images or complex problems may require more system memory

### Error Messages

- **"Error encountered. Please try again."**: Generic error message for user-facing issues
- **"Upload failed"**: File upload or validation error
- **"Video not found"**: Generated video file missing or corrupted

## 📝 API Endpoints

- `GET /` - Main application page
- `POST /upload` - File upload endpoint
- `GET /progress/<session_id>` - Progress tracking
- `GET /video/<filename>` - Video streaming
- `GET /health` - Health check

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Manim**: Mathematical animation library
- **ElevenLabs**: AI voice synthesis
- **OpenRouter**: AI model access
- **Lovable**: Frontend framework

## 📞 Support

For support or questions, please open an issue on the GitHub repository. 