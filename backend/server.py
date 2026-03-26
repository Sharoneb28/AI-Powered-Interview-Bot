from flask import Flask, request, jsonify
from flask_cors import CORS

from context_memory import ConversationContext
from question_generator import generate_question

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from resume_question_generator import generate_resume_questions
from face_analysis import analyze_frame

import numpy as np
import base64
import cv2

app = Flask(__name__)
CORS(app)

# ==============================
# GLOBAL CONTEXT
# ==============================
context = None


# ==============================
# HOME
# ==============================
@app.route("/")
def home():
    return "AI Interview Bot Backend Running 🚀"


# ==============================
# SKIP RESUME
# ==============================
@app.route("/skip_resume", methods=["POST"])
def skip_resume():
    global context

    if context:
        context.resume_questions = []

    return jsonify({"message": "Resume skipped"})


# ==============================
# FACE ANALYSIS
# ==============================
@app.route("/analyze_face", methods=["POST"])
def analyze_face_route():

    try:
        data = request.json.get("image")

        if not data:
            return jsonify({"error": "No image"}), 400

        image_bytes = base64.b64decode(data.split(',')[1])
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        result = analyze_frame(frame)

        return jsonify(result)

    except Exception as e:
        print("Face error:", e)

        return jsonify({
            "score": 60,
            "confidence": "Face not detected"
        })


# ==============================
# RESUME UPLOAD
# ==============================
@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    global context

    try:
        file = request.files.get("resume")
        domain = request.form.get("domain", "Software")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        text = extract_resume_text(file)
        skills = extract_skills(text)

        print("✅ Skills:", skills)

        # 🔥 FIX: Only generate resume questions if skills exist
        if skills:
            resume_questions = generate_resume_questions(skills)
        else:
            resume_questions = []
            print("⚠️ No skills found → skipping resume questions")

        print("✅ Resume Questions:", resume_questions)

        # Create fresh context
        context = ConversationContext(domain, resume_questions)

        return jsonify({
            "message": "Resume processed",
            "skills": skills
        })

    except Exception as e:
        print("Resume error:", e)
        return jsonify({"error": "Resume processing failed"}), 500


# ==============================
# GET QUESTION (MAIN LOGIC)
# ==============================
@app.route("/get_question", methods=["POST"])
def get_question():

    global context

    try:
        data = request.json

        domain = data.get("domain", "Software")
        performance = data.get("performance", "average")
        answer = data.get("answer", "")

        print("\n--- NEW REQUEST ---")
        print("Domain:", domain)
        print("Performance:", performance)
        print("Answer:", answer)

        # 🔥 Create context if not exists
        if context is None:
            context = ConversationContext(domain)

        # 🔥 Update domain without resetting everything
        elif context.domain != domain:
            context.domain = domain

        # 🔥 Safety check
        if not hasattr(context, "resume_questions"):
            context.resume_questions = []

        # 🔥 Generate question
        result = generate_question(context, performance, answer)

        return jsonify(result)

    except Exception as e:
        print("Question error:", e)

        return jsonify({
            "question": "Tell me about yourself.",
            "domain": domain,
            "difficulty": "easy",
            "is_follow_up": False
        })


# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    print("🚀 Starting AI Interview Bot Server...")
    app.run(debug=True)