"""
Simplified Sign Language Detection Server
This version has better error handling and fallback options
"""

import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import io

# Try to import required packages with fallbacks
try:
    from fastapi import FastAPI, File, UploadFile, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    FASTAPI_AVAILABLE = True
    print("✅ FastAPI available - using advanced server")
except ImportError:
    FASTAPI_AVAILABLE = False
    print("⚠️  FastAPI not available - using basic HTTP server")

try:
    import cv2
    import numpy as np
    import mediapipe as mp
    from PIL import Image
    VISION_AVAILABLE = True
    print("✅ Computer vision libraries available")
except ImportError as e:
    VISION_AVAILABLE = False
    print(f"⚠️  Vision libraries not available: {e}")
    print("Will use mock detection for demo purposes")

class SimpleSignDetector:
    """Fallback sign detector that works without ML libraries"""
    
    def __init__(self):
        self.signs = ["Hello", "Thank You", "Please", "Yes", "No", "Good", "Bad", "Help"]
        self.current_index = 0
    
    def detect_sign(self, image_data=None):
        """Mock sign detection for demo purposes"""
        import random
        import time
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Return a random sign occasionally
        if random.random() > 0.7:  # 30% chance of detection
            sign = self.signs[self.current_index % len(self.signs)]
            self.current_index += 1
            confidence = 0.75 + random.random() * 0.25
            return {"sign": sign, "confidence": confidence}
        
        return {"sign": None, "confidence": 0.0}

class MLSignDetector:
    """Advanced sign detector using MediaPipe"""
    
    def __init__(self):
        if not VISION_AVAILABLE:
            raise ImportError("Vision libraries not available")
            
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
    
    def detect_sign(self, image_data):
        """Detect sign using MediaPipe"""
        try:
            # Convert image data to PIL Image
            pil_image = Image.open(io.BytesIO(image_data))
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands.process(rgb_image)
            
            if results.multi_hand_landmarks:
                # Simple gesture recognition based on hand landmarks
                landmarks = results.multi_hand_landmarks[0].landmark
                sign = self._recognize_gesture(landmarks)
                if sign:
                    return {"sign": sign, "confidence": 0.85}
            
            return {"sign": None, "confidence": 0.0}
            
        except Exception as e:
            print(f"Error in ML detection: {e}")
            return {"sign": None, "confidence": 0.0}
    
    def _recognize_gesture(self, landmarks):
        """Simple gesture recognition"""
        # Check for open palm (Hello)
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 6, 10, 14, 18]
        
        extended_fingers = 0
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:
                extended_fingers += 1
        
        if extended_fingers >= 4:
            return "Hello"
        elif extended_fingers <= 1:
            return "Yes"  # Fist-like gesture
        
        return None

# Initialize the appropriate detector
if VISION_AVAILABLE:
    try:
        detector = MLSignDetector()
        print("✅ Using ML-based sign detection")
    except Exception as e:
        print(f"⚠️  ML detector failed, using simple detector: {e}")
        detector = SimpleSignDetector()
else:
    detector = SimpleSignDetector()
    print("✅ Using simple mock detector")

if FASTAPI_AVAILABLE:
    # FastAPI version
    app = FastAPI(title="Sign Language Detection API")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.post("/detect-sign")
    async def detect_sign_endpoint(image: UploadFile = File(...)):
        try:
            contents = await image.read()
            result = detector.detect_sign(contents)
            return result
        except Exception as e:
            print(f"Error: {e}")
            return {"sign": None, "confidence": 0.0}
    
    @app.get("/")
    async def root():
        return {"message": "Sign Language Detection API is running"}
    
    def start_server():
        print("🚀 Starting FastAPI server on http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)

else:
    # Basic HTTP server version
    class SignLanguageHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"message": "Sign Language Detection API is running (Basic Mode)"}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.end_headers()
        
        def do_POST(self):
            if self.path == '/detect-sign':
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    # Simple mock detection since we can't easily parse multipart data
                    result = detector.detect_sign()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                    
                except Exception as e:
                    print(f"Error: {e}")
                    self.send_response(500)
                    self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        
        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
    
    def start_server():
        print("🚀 Starting basic HTTP server on http://localhost:8000")
        server = HTTPServer(('localhost', 8000), SignLanguageHandler)
        server.serve_forever()

if __name__ == "__main__":
    print("🎯 Sign Language Detection Server")
    print("=" * 40)
    
    if not FASTAPI_AVAILABLE:
        print("📝 To get full functionality, install:")
        print("   pip install fastapi uvicorn python-multipart")
    
    if not VISION_AVAILABLE:
        print("📝 To get real sign detection, install:")
        print("   pip install opencv-python mediapipe pillow numpy")
    
    print("\n🌐 Server will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("\nTry installing dependencies manually:")
        print("pip install fastapi uvicorn opencv-python mediapipe pillow numpy python-multipart")
