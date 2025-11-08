async function loadnews(){
    const resp = await fetch("/getrianews").then(response => response.json()).then(data => JSON.stringify(data));
    const data = JSON.parse(resp).data;
    Object.entries(data).forEach(i => {
        console.log(i)
        const ndiv = document.createElement("div");
        ndiv.style = `background-image: linear-gradient(to top, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0) 100%), url(${i[1].image});`
        ndiv.style.cursor = "pointer";
        ndiv.addEventListener('click', function(){window.location.href = i[1].link})
        ndiv.classList.add("newsdiv")
        ndiv.innerHTML = `
        <h1 class="newstitle">${i[1].title}</h1>
        `
        document.getElementById("newslist").appendChild(ndiv)
    });
    loadFullSite();
}

document.addEventListener("weGotInternet", loadnews)