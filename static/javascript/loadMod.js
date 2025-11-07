async function loadMod(){
    modid = window.location.pathname.split("/")[2]
    const resp = await fetch(`/getmods/${modid}`).then(response => response.json()).then(data => JSON.stringify(data))
    const data = JSON.parse(resp).payload
    //the worst part
    //getting mod name
    document.getElementById("modtitle").textContent = data.versions[0].name
    //download button
    const downloadButton = document.getElementById("downloadbutton")
    downloadButton.style.visibility = "visible"
    downloadButton.addEventListener("click", function(){
        window.open(`/getmods/${modid}/download?version=${data.versions[0].version}`)
    })
    //this all to get description
    const whatwesend = {
        data: JSON.parse(resp).payload.about
    }
    const textified = await fetch(`/textify`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(whatwesend)
    }).then(response => response.json()).then(response => JSON.stringify(response));
    const textdata = JSON.parse(textified);
    document.getElementById("moddesc").innerHTML = JSON.stringify(textdata.data.replace(/\n/g, "<br><br>"))
}

document.addEventListener("DOMContentLoaded", loadMod)