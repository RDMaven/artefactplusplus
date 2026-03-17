# API de communication entre l'interface graphique (IG) et le programme python (PY)

### IG -> PY

Set vertex :

```json
{
    "name": "setVertex"
    "x": float
    "y": float
}
```

Set Edge :

```json
{
    "name": "setEdge",
    "vertex1": vertex,
    "vertex2": vertex
}

Vertex de la forme :
json{
    id: int,
    x: float,
    y: float
}
```

Suppression de vertex :
```json
{
    "name": "suppressVertex",
    "vertexId": id: int
}
```



### PY -> IG

Opération effectuée :

```json
{
    "name": "validation",
    "operation": string,
    "result": int   #0: ratée 1: réussie
}
```