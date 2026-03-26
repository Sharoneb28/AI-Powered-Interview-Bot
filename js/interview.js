let seconds = 0;
let timerInterval;

/* ============================= */
/* START CAMERA */
/* ============================= */

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });

        document.getElementById("video").srcObject = stream;

    } catch (error) {
        console.error(error);
    }
}

/* ============================= */
/* TIMER */
/* ============================= */

function startTimer() {
    seconds = 0;

    clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        seconds++;
        document.getElementById("timer").innerText = seconds + "s";
    }, 1000);
}

/* ============================= */
/* GET QUESTION */
/* ============================= */

async function getQuestion(performance="average"){

    let domain = localStorage.getItem("domain") || "Software"
    let answer = document.getElementById("answerBox").value

    let response = await fetch("http://127.0.0.1:5000/get_question",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            domain:domain,
            performance:performance,
            answer:answer   // ✅ IMPORTANT
        })
    })

    let data = await response.json()
    return data.question
}

/* ============================= */
/* FACE ANALYSIS */
/* ============================= */

async function sendFrame() {

    let video = document.getElementById("video");

    if (!video.videoWidth) return;

    let canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    let ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    let image = canvas.toDataURL("image/jpeg");

    try {
        let response = await fetch("http://127.0.0.1:5000/analyze_face", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: image })
        });

        let data = await response.json();

        localStorage.setItem("faceScore", data.score || 60);

    } catch (err) {
        console.error("Face API error:", err);
    }
}

/* ============================= */
/* SPEAK QUESTION */
/* ============================= */

function speakQuestion(question) {

    if(!question){
        question = "Tell me about yourself.";
    }

    document.getElementById("questionText").innerText = question;

    const speech = new SpeechSynthesisUtterance(question);

    speech.onend = function () {
        startTimer();
    };

    window.speechSynthesis.speak(speech);
}

/* ============================= */
/* LOAD QUESTION */
/* ============================= */

async function loadQuestion() {
    document.getElementById("answerBox").value = "";

    let question = await getQuestion("average");

    speakQuestion(question);
}

/* ============================= */
/* NEXT QUESTION */
/* ============================= */

async function nextQ(){

    let answer = document.getElementById("answerBox").value.trim().toLowerCase();

    let performance = "average";

if(answer.toLowerCase().includes("skip") || answer.length < 5){
    performance = "weak";
}
else if(answer.length > 120){
    performance = "strong";
}

    let question = await getQuestion(performance);

    document.getElementById("answerBox").value = "";

    speakQuestion(question);
}

/* ============================= */
/* SKIP QUESTION */
/* ============================= */

async function skipQuestion(){

    let question = await getQuestion("weak");

    document.getElementById("answerBox").value = "";

    speakQuestion(question);
}

/* ============================= */
/* VOICE INPUT */
/* ============================= */

function startVoice(){

    if (!('webkitSpeechRecognition' in window)) {
        alert("Use Chrome");
        return;
    }

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult = function(event){
        document.getElementById("answerBox").value =
            event.results[0][0].transcript;
    };

    recognition.start();
}

/* ============================= */
/* FINISH INTERVIEW */
/* ============================= */

function finishInterview() {

    let statsData = {
        labels: ["Eye Contact","Fluency","Confidence","Posture","STAR"],
        previous: [50,50,50,50,50],
        current: [
            parseInt(localStorage.getItem("faceScore")) || 60,
            70,
            80,
            60,
            50
        ]
    };

    localStorage.setItem("statsData", JSON.stringify(statsData));

    window.location.href = "growth.html";
}
/* ============================= */
/* INIT */
/* ============================= */

startCamera();
loadQuestion();
setInterval(sendFrame, 3000);