from flask import Flask, render_template, request
import json
import os
import requests

app = Flask(__name__)

HOME = None


def loadJson():
    global HOME
    with open(f"{os.getcwd()}/database/main_website.json", "r", encoding="utf-8") as temp:
        x = json.load(temp)
        HOME = x["HOME"]


@app.route("/", methods=['GET'])
def index():
    global HOME
    if HOME is None:
        loadJson()

    try:
        breed = request.args.get("breed")
    except:
        breed = None

    if (breed is None) or (bool(breed) is False) or (len(breed) == 0):
        data = requests.get(
            "https://dog.ceo/api/breeds/image/random/50").json()
        data_list = data["message"]
        return render_template("index.html",
                               sorted_list=data_list,
                               HOME=HOME,
                               HOME_logo=HOME["logo"],
                               HOME_title=HOME["title"],
                               HOME_links=HOME["links"],
                               )

    else:
        data = requests.get(
            f"https://dog.ceo/api/breed/{breed}/images/random/50").json()
        data_list = data["message"]
        return render_template("index.html",
                               sorted_list=data_list,
                               HOME=HOME,
                               HOME_logo=HOME["logo"],
                               HOME_title=HOME["title"],
                               HOME_links=HOME["links"],
                               )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    with open(os.path.join(os.getcwd(), "database", "settings.json"), "r", encoding="utf-8") as f1:
        host_data = json.load(f1)

    app.run(str(host_data["website"]["host"]),
            port=int(host_data["website"]["port"]))
