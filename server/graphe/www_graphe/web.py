from flask import Flask, Response, request, send_from_directory
from flask_sock import Sock
import threading
from utils import LOG_FILE, log, sendAll, validation
import json
import www_graphe.graphe as G


###GESTION WEB

static_dir = "./assets"
sockets = []    #Liste des clients websockets
GRAPHE = G.graph()

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

@app.get("/map_build")
def map_build():
    GRAPHE.reset()
    return send_from_directory('./templates', 'map_builder.html')

@sock.route("/ws")
def ws(ws):
    with open(LOG_FILE,'w'):
        pass
    lock = threading.Lock()
    sockets.append((ws, lock))
    while True:
        data = ws.receive()
        try:
            data = json.loads(data)
        except Exception as e:
            log("Erreur lors de la reception d'un message ws : {e}", 1)
            continue
        log(data, 0)
        name = data.get("name")
        match name:
            case "setVertex":
                try:
                    id = G.id_list[-1] + 1
                    x: float = data.get('x')
                    y:float =  data.get('y')
                    vertex = G.vertex(id, x, y)
                    GRAPHE.addVertex(vertex)
                    object = validation("setVertex", 1)
                except:
                    object = validation("setVertex", 0)
                sendAll(object, sockets)
            case "setEdge":
                try:
                    v1_json = data.get('v1')
                    v2_json = data.get('v2')
                    v1_json = json.load(v1_json)
                    v2_json = json.load(v2_json)
                    v1 = G.vertex(v1_json.get('id'), v1_json.get('x'), v1_json('y'))
                    v2 = G.vertex(v2_json.get('id'), v2_json.get('x'), v2_json('y'))
                    GRAPHE.addEdge(v1,v2)
                    object = validation("setEdge", 1)
                except:
                    object = validation("setEdge", 0)
                sendAll(object, sockets)
            case "suppressVertex":
                try:
                    vertexId: int = data.get("vertexId")
                    GRAPHE.removeVertex(vertexId)
                    object = validation("suppressVertex", 1)
                except:
                    object = validation("suppressVertex", 0)
                sendAll(object, sockets)
                    


