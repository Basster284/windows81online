function fillInput(){
    const urlParams = new URLSearchParams();
    document.getElementsByName("query")[0].value = urlParams.get("query");
}

document.addEventListener("DOMContentLoaded", fillInput)