@echo off
echo Installing Python dependencies for Sign Language Detection...
echo This may take a few minutes...

pip install fastapi
pip install uvicorn[standard]
pip install python-multipart
pip install pillow
pip install numpy
pip install opencv-python
pip install mediapipe

echo.
echo Installation complete!
echo Now run: python scripts/sign_detection_server.py
pause
