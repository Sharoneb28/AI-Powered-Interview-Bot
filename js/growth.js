let sessions=JSON.parse(localStorage.getItem("sessions"))||[];

let current=sessions[sessions.length-1]||0;
let previous=sessions[sessions.length-2]||0;

document.getElementById("currentScore").innerText=current+"%";
document.getElementById("previousScore").innerText=previous+"%";
document.getElementById("improvement").innerText=(current-previous)+"%";

new Chart(document.getElementById("chart"),{
type:'line',
data:{
labels:sessions.map((_,i)=>"Session "+(i+1)),
datasets:[{
label:'Confidence Score',
data:sessions,
borderColor:'#3b82f6',
backgroundColor:'rgba(59,130,246,0.2)',
fill:true
}]
},
options:{scales:{y:{beginAtZero:true,max:100}}}
});