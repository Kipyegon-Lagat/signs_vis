import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

prev_landmarks = None
prev_time = 0
DEBOUNCE_TIME = 0.5  # seconds
MOVEMENT_THRESHOLD = 15  # pixels

def calculate_movement(landmarks1, landmarks2):
    """Sum of Euclidean distances between corresponding landmarks."""
    if landmarks1 is None or landmarks2 is None:
        return float('inf')
    movement = 0
    for lm1, lm2 in zip(landmarks1, landmarks2):
        dx = lm1.x - lm2.x
        dy = lm1.y - lm2.y
        movement += math.sqrt(dx*dx + dy*dy)
    return movement * 1000  # scale for sensitivity

def dummy_predict(landmarks):
    # Just a placeholder: replace with your actual model
    return "A"  # Always returns 'A' as mock

cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        current_time = time.time()
        prediction = ""

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                movement = calculate_movement(prev_landmarks, hand_landmarks.landmark)
                if movement > MOVEMENT_THRESHOLD and current_time - prev_time > DEBOUNCE_TIME:
                    prediction = dummy_predict(hand_landmarks.landmark)
                    prev_time = current_time
                    prev_landmarks = hand_landmarks.landmark

        if prediction:
            cv2.putText(image, f"Sign: {prediction}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        cv2.imshow('Sign Language Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
