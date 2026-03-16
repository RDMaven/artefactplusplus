import numpy as np



###GESTION DES GRAPH

class graph():
    def __init_(self, vertexs = {}):
        self.vertexs = vertexs
    
    def addVertex(self, vertex: vertex):
        if not vertex.id in self.vertexs.keys():
            self.vertexs[vertex.id] = []

    def addEdge(self, vertex1: vertex, vertex2: vertex):
        if not (vertex1.id in self.vertexs.keys() and vertex2.id in self.vertexs.keys()):
            self.addVertex(vertex1)
            self.addVertex(vertex2)
        if not vertex2.id in self.vertexs[vertex1.id]:
            self.vertexs[vertex1.id].append(vertex2.id)
        if not vertex1.id in self.vertexs[vertex2.id]:
            self.vertexs[vertex2.id].append(vertex1.id)


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
