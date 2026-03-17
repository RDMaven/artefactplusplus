import numpy as np



###GESTION DES GRAPH

class graph():
    '''
    Les sommets sont identifiés à partir de leurs id'''
    def __init__(self, vertexs = {}):
        self.vertexs = vertexs
    
    def addVertex(self, vertex: vertex):
        if not vertex.id in self.vertexs.keys():
            self.vertexs[vertex.id] = []

    def addEdge(self, vertex1: vertex, vertex2: vertex):
        if not (vertex1.id in self.vertexs.keys() and vertex2.id in self.vertexs.keys()):
            self.addVertex(vertex1)
            self.addVertex(vertex2)
        if not vertex2.id in self.vertexs[vertex1.id]:
            self.vertexs[vertex1.id].append(vertex2)
        if not vertex1.id in self.vertexs[vertex2.id]:
            self.vertexs[vertex2.id].append(vertex1)
    
    def reset(self):
        self.vertexs = {}

    def toString(self):
        res: str = "{"
        for key in self.vertexs.keys():
            res += str(key)
            res += ": ["
            for elt in self.vertexs[key]:
                res+= "vertex"
                res += str(elt.id)
            res += "] "
        res += "}"
        print(res)

    def removeVertex(self, vertixId: int):
        '''Supprime le sommet d'id : vertexId'''
        if vertixId in self.vertexs.keys():
            del self.vertexs[vertixId]

id_list = []

class vertex():

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


### Exemple ###
'''Graphe_ex = graph()
v1, v2, v3 = vertex(0, 1, 1), vertex(1,2,2), vertex(2,3,3)
Graphe_ex.addVertex(v1)
Graphe_ex.addVertex(v2)
Graphe_ex.addVertex(v3)
Graphe_ex.addEdge(v1,v3)

Graphe_ex.toString()'''