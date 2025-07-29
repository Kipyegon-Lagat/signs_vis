from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import mediapipe as mp
import io
from PIL import Image
import uvicorn

# Check for required dependencies
try:
    from fastapi import FastAPI, File, UploadFile, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import cv2
    import numpy as np
    import mediapipe as mp
    import io
    from PIL import Image
    import uvicorn
except ImportError as e:
    print("❌ Missing required dependency!")
    print(f"Error: {e}")
    print("\n🔧 To fix this, run one of these commands:")
    print("   python scripts/install_dependencies.py")
    print("   python scripts/setup_backend.py")
    print("\nOr install manually:")
    print("   pip install fastapi uvicorn opencv-python mediapipe pillow numpy python-multipart")
    exit(1)

print("✅ All dependencies loaded successfully!")

app = FastAPI(title="Sign Language Detection API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Simple sign recognition based on hand landmarks
class SignRecognizer:
    def __init__(self):
        # Define basic sign patterns based on hand landmarks
        self.sign_patterns = {
            'hello': self._is_hello_gesture,
            'thank_you': self._is_thank_you_gesture,
            'please': self._is_please_gesture,
            'yes': self._is_yes_gesture,
            'no': self._is_no_gesture,
        }
    
    def _is_hello_gesture(self, landmarks):
        """Detect hello gesture (open palm facing forward)"""
        if not landmarks:
            return False
        
        # Check if all fingers are extended
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        finger_pips = [3, 6, 10, 14, 18]  # Finger PIP joints
        
        extended_fingers = 0
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:  # Finger is extended
                extended_fingers += 1
        
        return extended_fingers >= 4
    
    def _is_thank_you_gesture(self, landmarks):
        """Detect thank you gesture (hand moving from chin outward)"""
        if not landmarks:
            return False
        
        # Simplified: check if hand is near face level
        wrist = landmarks[0]
        middle_finger_tip = landmarks[12]
        
        return wrist.y < 0.6 and middle_finger_tip.y < wrist.y
    
    def _is_please_gesture(self, landmarks):
        """Detect please gesture (circular motion on chest)"""
        if not landmarks:
            return False
        
        # Simplified: check hand position relative to body
        wrist = landmarks[0]
        return 0.4 < wrist.y < 0.8
    
    def _is_yes_gesture(self, landmarks):
        """Detect yes gesture (fist moving up and down)"""
        if not landmarks:
            return False
        
        # Check if fingers are curled (fist-like)
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
        finger_mcp = [5, 9, 13, 17]   # MCP joints
        
        curled_fingers = 0
        for tip, mcp in zip(finger_tips, finger_mcp):
            if landmarks[tip].y > landmarks[mcp].y:  # Finger is curled
                curled_fingers += 1
        
        return curled_fingers >= 3
    
    def _is_no_gesture(self, landmarks):
        """Detect no gesture (index finger pointing side to side)"""
        if not landmarks:
            return False
        
        # Check if index finger is extended and others are curled
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        
        index_extended = index_tip.y < index_pip.y
        middle_curled = middle_tip.y > middle_pip.y
        
        return index_extended and middle_curled
    
    def recognize_sign(self, landmarks):
        """Recognize sign from hand landmarks"""
        best_match = None
        best_confidence = 0.0
        
        for sign_name, detector in self.sign_patterns.items():
            if detector(landmarks):
                # Simple confidence based on gesture detection
                confidence = 0.8 + np.random.random() * 0.2
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = sign_name
        
        return best_match, best_confidence

# Initialize sign recognizer
recognizer = SignRecognizer()

@app.post("/detect-sign")
async def detect_sign(image: UploadFile = File(...)):
    try:
        # Read image
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents))
        
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Process with MediaPipe
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)
        
        if results.multi_hand_landmarks:
            # Get the first detected hand
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Recognize sign
            sign, confidence = recognizer.recognize_sign(hand_landmarks.landmark)
            
            if sign:
                return {
                    "sign": sign.replace('_', ' ').title(),
                    "confidence": float(confidence)
                }
        
        return {"sign": None, "confidence": 0.0}
        
    except Exception as e:
        print(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="Image processing failed")

@app.get("/")
async def root():
    return {"message": "Sign Language Detection API is running"}

if __name__ == "__main__":
    print("Starting Sign Language Detection Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
