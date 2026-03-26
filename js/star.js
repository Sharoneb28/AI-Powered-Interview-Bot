document.addEventListener("DOMContentLoaded", () => {

    const submitBtn = document.getElementById("submitStar");

    if (!submitBtn) return;

    submitBtn.addEventListener("click", calculateSTAR);

});

function calculateSTAR(){

    let s = document.getElementById("s").value.trim().length;
    let t = document.getElementById("t").value.trim().length;
    let a = document.getElementById("a").value.trim().length;
    let r = document.getElementById("r").value.trim().length;

    if(s === 0 || t === 0 || a === 0 || r === 0){
        alert("Please fill all fields!");
        return;
    }

    // ⭐ STAR scoring logic
    let score = Math.min((s + t + a + r) / 10, 100);
    score = Math.floor(score);

    // ✅ Save STAR score separately
    localStorage.setItem("starScore", score);

    // ✅ Update statsData immediately
    function calculateSTAR(){

    let s = document.getElementById("s").value.length;
    let t = document.getElementById("t").value.length;
    let a = document.getElementById("a").value.length;
    let r = document.getElementById("r").value.length;

    let score = Math.min((s+t+a+r)/5, 100);

    let statsData = JSON.parse(localStorage.getItem("statsData")) || {
        labels: ["Eye Contact", "Fluency", "Confidence", "Posture", "STAR"],
        previous: [50,50,50,50,50],
        current: [50,50,50,50,50]
    };

    statsData.previous = [...statsData.current];

    // update STAR (index 4)
    statsData.current[4] = score;

    localStorage.setItem("statsData", JSON.stringify(statsData));

    alert("STAR Score: " + score);

    window.location.href = "growth.html";
}
}