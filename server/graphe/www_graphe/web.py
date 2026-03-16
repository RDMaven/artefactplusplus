from flask import Flask, Response, request, send_from_directory
from flask_sock import Sock


###GESTION WEB

static_dir = "./assets"

app = Flask(__name__, static_folder=static_dir, static_url_path="/")
sock = Sock(app)

@app.get("/")
def index():
    return send_from_directory("./templates","index.html")

@app.get("/en")
def index_anglais():
    return send_from_directory("./templates","index_anglais.html")

@app.get("/wait")
def wait():
    return send_from_directory('./templates',"waiting.html")

@app.get("/team")
def team():
    return send_from_directory('./templates', 'equipe.html')