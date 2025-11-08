from flask import Flask, render_template, jsonify, request, Response, send_file
import requests
import re
from bs4 import BeautifulSoup
import os
import modidvalidator
import markdown

app = Flask("espressosite", template_folder="templates", static_folder="static")

CLR = re.compile("<.*?>")

@app.route("/")
def mainpage():
    return render_template("mainpage.html")

@app.route("/start")
def startmenu():
    return render_template("startmenu.html")

@app.route("/getrianews")
def getrianews():
    resp = requests.get("https://ria.ru/export/rss2/archive/index.xml")
    soup = BeautifulSoup(resp.text, "xml")
    json = {"data":[]}
    for i in soup.find_all("item"):
        if not i.find_next("enclosure") is None:
            json["data"].append({"title": i.find_next("title").text, "image": i.find_next("enclosure").get("url"), "link": i.find_next("guid").text}) # type: ignore
        else:
            json["data"].append({"title": i.find_next("title").text,"image": "https://static.wikia.nocookie.net/66c2ede7-8ee4-4d71-b0d5-4aa885e66a82/scale-to-width/755", "link": i.find_next("guid").text}) # type: ignore
    return jsonify(json)

@app.route("/geodestore")
def geodeshop():
    q = request.args.get("query")
    if q == None:
        return render_template("geodestore.html")
    else:
        return render_template("geodesearch.html", query=q)

@app.route("/checkcon")
def checkcon():
    resp = requests.get("https://gstatic.com/generate_204")
    return jsonify({"status": resp.status_code})

@app.route("/getmods/<modid>")
def getmod(modid):
    params = request.args.to_dict()
    resp = requests.get(f"https://api.geode-sdk.org/v1/mods/{modid}", params=params)
    return resp.json()

@app.route("/textify", methods=["POST"])
def textify():
    if request.is_json:
        data = request.json
    else:
        return jsonify({"error": "request should be json"})
    
    textified = re.sub(CLR, "", markdown.markdown(data["data"])) # type: ignore
    
    return jsonify({"data": textified})

@app.route("/getmods/<modid>/download")
def downloadmod(modid):
    if modidvalidator.is_valid(modid):
        version = request.args.get("version")
        if not version:
            return jsonify({"error": "parameter 'version' required"}), 422
        iscached = os.path.isfile(f"cache/{modid}.geode")
        if not iscached:
            resp = requests.get(f"https://api.geode-sdk.org/v1/mods/{modid}/versions/{version}/download")
            if resp.status_code == 200:
                with open(f"cache/{modid}.geode", "wb") as f:
                    f.write(resp.content)
                return send_file(open(f"cache/{modid}.geode", "rb"), download_name=f"{modid}.geode")
            else:
                return jsonify({"error": f"geode responded with {resp.status_code}"})
        else:
            return send_file(open(f"cache/{modid}.geode", "rb"), download_name=f"{modid}.geode")
    else:
        return jsonify({"error": f"invalid mod id"})


@app.route("/getmods")
def getmods():
    params = request.args.to_dict()
    resp = requests.get(f"https://api.geode-sdk.org/v1/mods", params=params)
    data = resp.json()
    return jsonify(data)

@app.route("/rianews")
def rianews():
    return render_template("news.html")

@app.route("/geodestore/<modid>")
def geodemod(modid):
    return render_template("geodemod.html")

app.run(debug=True)