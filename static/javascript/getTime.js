function getTime(){
    now = new Date();
    hours = now.getHours();
    minutes = now.getMinutes();

    document.getElementById("clock").textContent = `${hours}:${minutes}`
}

document.addEventListener("DOMContentLoaded", getTime)