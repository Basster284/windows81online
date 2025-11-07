async function getMods() {
    // i stealed that
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const q = urlParams.get("query");
    // written by myself
    const resp =  await fetch(`/getmods?query=${q}&per_page=999`).then(response => response.json()).then(data => JSON.stringify(data))
    const data = JSON.parse(resp).payload.data;
    document.getElementById("results").innerHTML = `${JSON.parse(resp).payload.count} результатов`;
    data.forEach(mod => {
        const ndiv = document.createElement("div");
        ndiv.classList.add("searchmodelement")
        ndiv.addEventListener("click", function(){
            window.location.replace(`/geodestore/${mod.versions[0].mod_id}`)
        })
        ndiv.innerHTML = `<img class="verysmallmodlogo" src='https://api.geode-sdk.org/v1/mods/${mod.id}/logo'>
        <h1 class="searchmodtitle">${mod.versions[0].name}</h1>
        <p class="searchmoddesc">${mod.versions[0].description}</p>
        <p class="price">Бесплатно</p>`;
        document.getElementById("modlist").appendChild(ndiv);
    })
}

document.addEventListener("DOMContentLoaded", getMods)