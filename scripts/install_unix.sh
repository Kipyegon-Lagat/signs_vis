#!/bin/bash

echo "Installing Python dependencies for Sign Language Detection..."
echo "This may take a few minutes..."

pip3 install fastapi
pip3 install "uvicorn[standard]"
pip3 install python-multipart
pip3 install pillow
pip3 install numpy
pip3 install opencv-python
pip3 install mediapipe

echo ""
echo "🎉 Installation complete!"
echo "Now run: python3 scripts/sign_detection_server.py"
