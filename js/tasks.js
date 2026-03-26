document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".task-card").forEach(card => {
        card.addEventListener("click", () => {
            let link = card.getAttribute("data-link");
            console.log("Going to:", link);
            window.location.href = link;
        });
    });

    document.getElementById("growthBtn").addEventListener("click", () => {
        window.location.href = "growth.html";
    });

});