import json
import threading
import time
from flask import Flask, Response, request, send_from_directory
from flask_sock import Sock

static_dir = "../www_demo"

IP_SERVER = "137.194.255.255" #A modifier
app = Flask(__name__, static_folder=static_dir, static_url_path="/")
sock = Sock(app)

@app.route("/")
def index():
    return send_from_directory(static_dir, "assets/index.html")

@app.get("/video")
def video(id_robot: str):
    return "https://"+IP_SERVER+"/video/"+id_robot

if __name__ == "__main__":
    app.run(debug=True, port=5000)
