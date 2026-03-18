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

if __name__ == '__main__':
    app.run(debug=True)