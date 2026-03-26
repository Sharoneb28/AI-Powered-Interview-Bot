document.addEventListener("DOMContentLoaded", () => {

    let statsData = JSON.parse(localStorage.getItem("statsData")) || {
        labels: ["Eye Contact", "Fluency", "Confidence", "Posture", "STAR"],
        previous: [50,50,50,50,50],
        current: [70,60,80,60,50]
    };

    // UI Update
    document.getElementById("fluency").innerText =
        "Fluency: " + statsData.current[1] + "%";

    document.getElementById("posture").innerText =
        "Posture: " + statsData.current[3] + "%";

    document.getElementById("confidence").innerText =
        "Confidence: " + statsData.current[2] + "%";

    // Chart
    new Chart(document.getElementById("chart"), {
        type: "radar",
        data: {
            labels: statsData.labels,
            datasets: [
                {
                    label: "Previous",
                    data: statsData.previous,
                    borderWidth:2
                },
                {
                    label: "Current",
                    data: statsData.current,
                    borderWidth:2
                }
            ]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

});

// Navigation
function goTask(page){
    window.location.href = "./" + page;
}

function goDashboard(){
    window.location.href = "./dashboard.html";
}