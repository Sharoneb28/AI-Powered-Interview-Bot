let seconds = 0
let timerInterval


async function startCamera(){

    try{

        const stream = await navigator.mediaDevices.getUserMedia({
            video:true,
            audio:true
        })

        const video=document.getElementById("video")
        video.srcObject=stream

    }

    catch(error){

        alert("Camera or microphone permission denied.")
        console.error(error)

    }

}


function startTimer(){

    seconds=0

    clearInterval(timerInterval)

    timerInterval=setInterval(()=>{

        seconds++
        document.getElementById("timer").innerText=seconds+"s"

    },1000)

}


async function getQuestion(performance="average"){

    let domain = localStorage.getItem("domain") || "Software"
    let answer = document.getElementById("answerBox").value

    try{

        let response = await fetch("http://127.0.0.1:5000/get_question",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                domain:domain,
                performance:performance,
                answer:answer
            })
        })

        let data = await response.json()

        console.log("Question received:",data)

        return data.question

    }

    catch(error){

        console.error("Backend error:",error)

        return "Error loading question"

    }

}


function speakQuestion(question){

    const avatar=document.getElementById("aiAvatar")
    const status=document.getElementById("aiStatus")

    document.getElementById("questionText").innerText = question
    document.getElementById("subtitle").innerText = question

    const speech=new SpeechSynthesisUtterance(question)

    speech.onstart=function(){

        avatar.classList.add("talking")
        status.innerText="AI is asking..."

    }

    speech.onend=function(){

        avatar.classList.remove("talking")
        status.innerText="Your turn to answer"

        startTimer()

    }

    window.speechSynthesis.speak(speech)

}


async function loadQuestion(){

    document.getElementById("answerBox").value=""

    let question = await getQuestion("average")

    speakQuestion(question)

}


async function nextQ(){

    let answer=document.getElementById("answerBox").value

    let performance="average"

    if(answer.length > 150){
        performance="strong"
    }
    else if(answer.length < 50){
        performance="weak"
    }

    let question = await getQuestion(performance)

    document.getElementById("answerBox").value=""

    speakQuestion(question)

}


function startVoice(){

    if(!('webkitSpeechRecognition' in window)){
        alert("Use Google Chrome for voice input.")
        return
    }

    const recognition=new webkitSpeechRecognition()

    recognition.lang="en-US"

    recognition.onresult=function(event){

        const transcript=event.results[0][0].transcript
        document.getElementById("answerBox").value=transcript

    }

    recognition.start()

}


function finishInterview(){

    clearInterval(timerInterval)

    let answerText=document.getElementById("answerBox").value.trim()

    let lengthScore=Math.min(answerText.length/5,30)

    let timeScore=seconds<60 ? 30 : 15

    let baseScore=40

    let score=Math.floor(baseScore+lengthScore+timeScore)

    if(score>100) score=100

    let sessions=JSON.parse(localStorage.getItem("sessions")) || []

    sessions.push(score)

    localStorage.setItem("sessions",JSON.stringify(sessions))

    alert("Interview Completed!\nConfidence Score: "+score+"%")

    window.location.href="tasks.html"

}


startCamera()
loadQuestion()