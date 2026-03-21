from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # This data must match the names used in your dashboard.html script
    user_stats = {
        "labels": ['Fluency', 'Eye Contact', 'STAR Method', 'Confidence', 'Posture'],
        "previous": [70, 35, 55, 60, 65],
        "current": [85, 40, 60, 80, 70]
    }
    # This sends the user_stats to your HTML file
    return render_template('dashboard.html', stats=user_stats)

@app.route('/star-train')
def star_train():
    return render_template('star_training.html')

@app.route('/fluency-drill')
def fluency_drill():
    return render_template('fluency_drill.html')

@app.route('/eye-contact')
def eye_contact():
    return render_template('eye_contact.html')

@app.route('/power-pose')
def power_pose():
    return render_template('power_pose.html')

from flask import request, jsonify
import json
from datetime import datetime

def calculate_confidence(fluency, posture):
    return int((0.6 * fluency) + (0.4 * posture))


@app.route("/save_session", methods=["POST"])
def save_session_api():
    data = request.json

    data["confidence"] = calculate_confidence(
        data["fluency"], data["posture"]
    )
    data["timestamp"] = str(datetime.now())

    try:
        with open("data.json", "r") as f:
            sessions = json.load(f)
    except:
        sessions = []

    sessions.append(data)

    with open("data.json", "w") as f:
        json.dump(sessions, f, indent=4)

    return jsonify({"status": "saved"})


@app.route("/get_progress", methods=["GET"])
def get_progress():
    try:
        with open("data.json", "r") as f:
            sessions = json.load(f)
    except:
        return jsonify({"error": "No data"})

    if len(sessions) < 2:
        return jsonify({"message": "Not enough data"})

    current = sessions[-1]
    previous = sessions[-2]

    improvement = {
        "fluency": current["fluency"] - previous["fluency"],
        "posture": current["posture"] - previous["posture"],
        "confidence": current["confidence"] - previous["confidence"]
    }

    return jsonify({
        "current": current,
        "previous": previous,
        "improvement": improvement
    })

if __name__ == '__main__':
    app.run(debug=True)