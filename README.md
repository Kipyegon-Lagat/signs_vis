# Sign Language Translator

An interactive web application that uses computer vision to detect sign language gestures in real-time and translate them to text and speech.

## Features

- 🎥 Real-time webcam integration
- 🤟 Sign language gesture detection
- 📝 Text translation display
- 🔊 Text-to-speech functionality
- 📊 Confidence scoring
- 📜 Translation history
- 📱 Responsive design

## How It Works

### Frontend (React/Next.js)
- Captures live video from user's webcam
- Sends video frames to the backend for analysis
- Displays detected signs and translations
- Provides text-to-speech functionality

### Backend (Python/FastAPI)
- Receives images from the frontend
- Uses MediaPipe for hand landmark detection
- Analyzes hand gestures to recognize signs
- Returns translation results with confidence scores

## Setup Instructions

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Webcam access

### Quick Start

#### Option 1: Automatic Setup (Recommended)
\`\`\`bash
# Install Python dependencies
python scripts/install_dependencies.py

# Start the backend server
python scripts/sign_detection_server.py

# In another terminal, start the frontend
npm run dev
\`\`\`

#### Option 2: Manual Installation
\`\`\`bash
# Install Python packages
pip install fastapi uvicorn opencv-python mediapipe pillow numpy python-multipart

# Start backend
python scripts/sign_detection_server.py

# Start frontend
npm run dev
\`\`\`

#### Option 3: Platform-specific Scripts

**Windows:**
\`\`\`cmd
scripts\install_windows.bat
python scripts\sign_detection_server.py
\`\`\`

**Mac/Linux:**
\`\`\`bash
chmod +x scripts/install_unix.sh
./scripts/install_unix.sh
python3 scripts/sign_detection_server.py
\`\`\`

### Troubleshooting Installation

If you get "ModuleNotFoundError", try:
1. Make sure you're using the correct Python version: `python --version`
2. Try using `pip3` instead of `pip`
3. Install packages one by one:
   \`\`\`bash
   pip install fastapi
   pip install uvicorn
   pip install opencv-python
   pip install mediapipe
   pip install pillow
   pip install numpy
   pip install python-multipart
   \`\`\`

## Supported Signs

Currently supports basic signs:
- Hello (open palm)
- Thank You (hand near chin)
- Please (circular motion)
- Yes (fist nodding)
- No (index finger side to side)

## Technical Details

### Hand Detection
- Uses Google's MediaPipe for robust hand landmark detection
- Tracks 21 key points on each hand
- Works in various lighting conditions

### Sign Recognition
- Pattern matching based on hand landmark positions
- Confidence scoring for accuracy
- Extensible architecture for adding new signs

### Performance
- Processes frames at ~1 FPS for real-time detection
- Optimized for accuracy over speed
- Minimal latency between gesture and translation

## Extending the System

### Adding New Signs
1. Define gesture patterns in `SignRecognizer` class
2. Add detection logic based on hand landmarks
3. Test with various hand positions and orientations

### Improving Accuracy
- Collect more training data
- Implement machine learning models
- Add temporal analysis for dynamic gestures

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

Requires webcam permissions and modern browser features.

## Troubleshooting

### Camera Issues
- Ensure webcam permissions are granted
- Check if other applications are using the camera
- Try refreshing the page

### Backend Connection
- Verify Python server is running on port 8000
- Check firewall settings
- Ensure all dependencies are installed

### Detection Accuracy
- Ensure good lighting conditions
- Position hand clearly in camera view
- Make distinct, deliberate gestures
- Keep hand steady for better detection

## Future Enhancements

- [ ] Support for more sign languages
- [ ] Dynamic gesture recognition
- [ ] Machine learning model training
- [ ] Mobile app version
- [ ] Multi-hand detection
- [ ] Sentence construction
- [ ] User customization options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
