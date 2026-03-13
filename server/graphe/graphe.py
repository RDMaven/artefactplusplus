import numpy as np
from flask import Flask, Response, request, send_from_directory
from flask_sock import Sock


###GESTION DES GRAPH

graphe = {} #Dictoinnaire des voisins d'un sommet recconnu grâce à son id
id_list = []

class vertex:

    def __init__(self, id: int, x: int, y: int):
        self.x = x
        self.y = y
        if not id in id_list:
            self.id = id
            id_list.append(id)
        else:
            raise Exception("This id is already defined !")
    
    def calcul_dist(self, other_vertex: vertex):
        return np.sqrt((self.x - other_vertex.x)**2 + (self.y - other_vertex.y)**2)
    

###GESTION WEB

static_dir = "./www_graphe"

app = Flask(__name__, static_folder=static_dir, static_url_path="/")
sock = Sock(app)

@app.get("/")
def index():
    return send_from_directory(static_dir, "index.html")

