from flask import Flask, render_template, jsonify, request, Response, send_file
import requests
import re
import os
import markdown

app = Flask("espressosite", template_folder="templates", static_folder="static")

CLR = re.compile("<.*?>")

@app.route("/")
def mainpage():
    return render_template("mainpage.html")

@app.route("/start")
def startmenu():
    return render_template("startmenu.html")

@app.route("/geodestore")
def geodeshop():
    q = request.args.get("query")
    if q == None:
        return render_template("geodestore.html")
    else:
        return render_template("geodesearch.html", query=q)

@app.route("/checkcon")
def checkcon():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    resp = requests.get(f"https://api.geode-sdk.org", headers=headers)
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
    version = request.args.get("version")
    if not version:
        return jsonify({"error": "parameter 'version' required"}), 422
    iscached = os.path.isfile(f"cache/{modid}.geode")
    if not iscached:
        resp = requests.get(f"https://api.geode-sdk.org/v1/mods/{modid}/versions/{version}/download")
        with open(f"cache/{modid}.geode", "wb") as f:
            f.write(resp.content)
            return send_file(open(f"cache/{modid}.geode", "rb"), download_name=f"{modid}.geode")
    else:
        return send_file(open(f"cache/{modid}.geode", "rb"), download_name=f"{modid}.geode")


@app.route("/getmods")
def getmods():
    params = request.args.to_dict()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    resp = requests.get(f"https://api.geode-sdk.org/v1/mods", headers=headers, params=params)
    data = resp.json()
    return jsonify(data)

@app.route("/geodestore/<modid>")
def geodemod(modid):
    return render_template("geodemod.html")