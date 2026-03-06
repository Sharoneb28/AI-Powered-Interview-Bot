import cv2
import mediapipe as mp
import math
import speech_recognition as sr
import threading
import time
from datetime import datetime

# ---------------- INITIALIZATION ---------------- #

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

looking_away_frames = 0
eye_contact_score = 100

fluency_score = 100
filler_words = ["um", "uh", "like", "actually", "basically", "you know"]

recognizer = sr.Recognizer()
mic = sr.Microphone()

session_start = time.time()

# ---------------- SPEECH ANALYSIS ---------------- #

def speech_analysis():
    global fluency_score

    with mic as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)

        words = text.split()
        total_words = len(words)
        filler_count = sum(words.count(word) for word in filler_words)

        if total_words > 0:
            fluency_score = max(0, 100 - (filler_count * 10))

        print("Fluency Score:", fluency_score)

    except:
        print("Could not understand audio")

speech_thread = threading.Thread(target=speech_analysis)
speech_thread.start()

# ---------------- MAIN LOOP ---------------- #

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            h, w, _ = frame.shape

            # -------- HEAD POSTURE -------- #
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]

            x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
            x2, y2 = int(right_eye.x * w), int(right_eye.y * h)

            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

            if abs(angle) > 10:
                posture = "Head Tilted"
                posture_color = (0, 0, 255)
            else:
                posture = "Good Posture"
                posture_color = (0, 255, 0)

            # -------- EYE CONTACT -------- #
            iris = face_landmarks.landmark[468]
            iris_x = int(iris.x * w)

            eye_left_corner = int(left_eye.x * w)
            eye_right_corner = int(right_eye.x * w)

            eye_width = eye_right_corner - eye_left_corner
            iris_ratio = (iris_x - eye_left_corner) / eye_width

            if iris_ratio < 0.35 or iris_ratio > 0.65:
                looking_status = "Looking Away"
                looking_color = (0, 0, 255)
                looking_away_frames += 1
            else:
                looking_status = "Maintaining Eye Contact"
                looking_color = (0, 255, 0)

            eye_contact_score = max(0, 100 - looking_away_frames)

            # -------- FINAL CONFIDENCE SCORE -------- #
            final_confidence = int((eye_contact_score * 0.6) + (fluency_score * 0.4))

            if final_confidence > 75:
                level = "High Confidence"
            elif final_confidence > 50:
                level = "Moderate Confidence"
            else:
                level = "Low Confidence"

            # -------- DISPLAY -------- #
            cv2.putText(frame, posture, (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, posture_color, 2)

            cv2.putText(frame, looking_status, (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, looking_color, 2)

            cv2.putText(frame, f"Eye Contact Score: {eye_contact_score}", (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            cv2.putText(frame, f"Fluency Score: {fluency_score}", (30, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.putText(frame, f"Final Confidence: {final_confidence}", (30, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

            cv2.putText(frame, level, (30, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    cv2.imshow("AI Interview Behavioral Analysis", frame)

    # Press 'q' to end session and save report
    if cv2.waitKey(1) & 0xFF == ord('q'):
        session_duration = int(time.time() - session_start)

        report = f"""
AI Interview Behavioral Report
Date: {datetime.now()}
Session Duration: {session_duration} seconds

Eye Contact Score: {eye_contact_score}
Fluency Score: {fluency_score}
Final Confidence Score: {final_confidence}
Confidence Level: {level}
"""

        with open("session_report.txt", "w") as file:
            file.write(report)

        print("Session Report Saved as session_report.txt")
        break

cap.release()
cv2.destroyAllWindows()