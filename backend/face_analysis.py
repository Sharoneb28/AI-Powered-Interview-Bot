import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

def analyze_frame(frame):

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if not results.multi_face_landmarks:
        return {"score": 0, "confidence": "No face detected"}

    face_landmarks = results.multi_face_landmarks[0]
    h, w, _ = frame.shape

    left_eye = face_landmarks.landmark[33]
    right_eye = face_landmarks.landmark[263]

    x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
    x2, y2 = int(right_eye.x * w), int(right_eye.y * h)

    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

    head_score = 100 if abs(angle) < 10 else 60

    iris = face_landmarks.landmark[468]
    iris_x = int(iris.x * w)

    eye_width = x2 - x1
    iris_ratio = (iris_x - x1) / eye_width if eye_width > 0 else 0.5

    eye_score = 100 if 0.35 < iris_ratio < 0.65 else 50

    final_score = int((eye_score * 0.6) + (head_score * 0.4))

    if final_score > 75:
        level = "High Confidence"
    elif final_score > 50:
        level = "Moderate Confidence"
    else:
        level = "Low Confidence"

    return {
        "score": final_score,
        "confidence": level
    }