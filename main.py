import cv2
import mediapipe as mp
import math
import time
from datetime import datetime

# ---------------- INITIALIZATION ---------------- #
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

looking_away_frames = 0
eye_contact_score = 100
head_tilt_frames = 0

session_start = time.time()

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

            # -------- HEAD POSTURE ANALYSIS -------- #
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]

            x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
            x2, y2 = int(right_eye.x * w), int(right_eye.y * h)

            # Calculate head tilt angle
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

            if abs(angle) > 10:
                posture_status = "Head Tilted"
                posture_color = (0, 0, 255)
                head_tilt_frames += 1
            else:
                posture_status = "Good Posture"
                posture_color = (0, 255, 0)

            # -------- EYE CONTACT ANALYSIS -------- #
            iris = face_landmarks.landmark[468]
            iris_x = int(iris.x * w)

            eye_left_corner = int(left_eye.x * w)
            eye_right_corner = int(right_eye.x * w)

            eye_width = eye_right_corner - eye_left_corner
            iris_ratio = (iris_x - eye_left_corner) / eye_width if eye_width > 0 else 0.5

            if iris_ratio < 0.35 or iris_ratio > 0.65:
                looking_status = "Looking Away"
                looking_color = (0, 0, 255)
                looking_away_frames += 1
            else:
                looking_status = "Maintaining Eye Contact"
                looking_color = (0, 255, 0)

            # Update scores
            eye_contact_score = max(0, 100 - (looking_away_frames // 3))  # Decay slower
            head_posture_score = max(0, 100 - (head_tilt_frames // 3))
            
            # -------- FACE ANALYSIS SCORE (60% eye contact, 40% head posture) -------- #
            face_analysis_score = int((eye_contact_score * 0.6) + (head_posture_score * 0.4))

            if face_analysis_score > 75:
                confidence_level = "High Confidence"
                level_color = (0, 255, 0)
            elif face_analysis_score > 50:
                confidence_level = "Moderate Confidence"
                level_color = (0, 255, 255)
            else:
                confidence_level = "Low Confidence"
                level_color = (0, 0, 255)

            # -------- DISPLAY RESULTS -------- #
            cv2.putText(frame, posture_status, (30, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, posture_color, 2)

            cv2.putText(frame, looking_status, (30, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, looking_color, 2)

            cv2.putText(frame, f"Eye Contact: {eye_contact_score}", (30, 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            cv2.putText(frame, f"Head Posture: {head_posture_score}", (30, 160),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.putText(frame, f"Face Analysis Score: {face_analysis_score}", (30, 200),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 3)

            cv2.putText(frame, confidence_level, (30, 250),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, level_color, 3)

    cv2.imshow("Face Analysis Only", frame)

    # Press 'q' to end session and save report
    if cv2.waitKey(1) & 0xFF == ord('q'):
        session_duration = int(time.time() - session_start)

        report = f"""
FACE ANALYSIS REPORT
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session Duration: {session_duration} seconds

Eye Contact Score: {eye_contact_score}
Head Posture Score: {head_posture_score}
Final Face Analysis Score: {face_analysis_score}
Confidence Level: {confidence_level}
"""

        with open("face_analysis_report.txt", "w") as file:
            file.write(report)

        print("Face Analysis Report saved as 'face_analysis_report.txt'")
        break

cap.release()
cv2.destroyAllWindows()
