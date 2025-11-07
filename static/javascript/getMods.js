async function getmods() {
    const fresp = await fetch("/getmods?per_page=999").then(response => response.json()).then(data => JSON.stringify(data))
    const fdata = JSON.parse(fresp).payload.data
    console.log("got mods");
    console.log("building page");
    fdata.forEach(i => {
        tags = i.tags;
        const ndiv = document.createElement("div");
        ndiv.classList.add("thumbmodelement");
        ndiv.addEventListener("click", function(){
            window.location.replace(`/geodestore/${i.versions[0].mod_id}`)
        })
        ndiv.innerHTML = `<img class="thumbmodimage" src="https://api.geode-sdk.org/v1/mods/${i.versions[0].mod_id}/logo">
        <h3 class="thumbmodtitle">${JSON.stringify(i.versions[0].name).replace(/\"/g, '')}</h3>
        <h3 class="thumbmodprice">Бесплатно</h3>
        <p class="thumbmoddownloads">${JSON.stringify(i.versions[0].download_count).replace(/\"/g, '')}</p>
        <p class="thumbmoddownloads">${tags[0]}</p>`;
        document.getElementById("modlist").appendChild(ndiv);
    })
    loadFullSite();
    console.log("we re done");
}

document.addEventListener("weGotInternet", getmods)