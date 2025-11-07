// functions
window.loadFullSite = function(){
    document.getElementById("centerlogo").style.opacity = 0;
    document.body.style.backgroundColor = 'white';
    document.getElementById("menu").style.opacity = 1;
    document.getElementById("nowthisisrealcontent").style.opacity = 1;
    document.getElementById("centerlogo").remove();
}

async function checkAvailabity() {
    const resp = await fetch('/checkcon');
    if(resp.ok){
        document.dispatchEvent(internetAvailable);
        console.log("api available");
    }
    else{
        document.getElementById("nocon").style.opacity = 1;
    }
}

// custome events
const internetAvailable = new CustomEvent('weGotInternet',{
    bubbles: true,
    cancelable: true
})

// event listeners
document.addEventListener("DOMContentLoaded", checkAvailabity)