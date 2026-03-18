from flask import Flask, request, jsonify
from flask_cors import CORS

from context_memory import ConversationContext
from question_generator import generate_question

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from resume_question_generator import generate_resume_questions

app = Flask(__name__)
CORS(app)

context = None


@app.route("/")
def home():
    return "AI Interview Bot Backend Running"


@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    global context

    file = request.files["resume"]
    domain = request.form["domain"]

    text = extract_resume_text(file)

    skills = extract_skills(text)

    resume_questions = generate_resume_questions(skills)

    context = ConversationContext(domain, resume_questions)

    return jsonify({
        "message": "Resume processed",
        "skills": skills
    })


@app.route("/get_question", methods=["POST"])
def get_question():

    global context

    data = request.json

    domain = data.get("domain", "Software")
    performance = data.get("performance", "average")
    answer = data.get("answer", "")

    if context is None or context.domain != domain:
        context = ConversationContext(domain)

    result = generate_question(context, performance, answer)

    return jsonify(result)


if __name__ == "__main__":
    print("Starting AI Interview Bot Server...")
    app.run(debug=True)