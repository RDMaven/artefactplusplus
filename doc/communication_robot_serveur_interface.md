# Communication Robot-Serveur-Interface
La communication entre les robots et le serveur et l'interface se fait par **WebSocket**.
Le serveur est central : les informations ne passent **JAMAIS** directement entre interface et robots, mais toujours par le serveur.

Les informations qui doivent circuler sont les suivantes :
* Robot -> Serveur:
    * `status` : L'état du robot, le **mode**, le **niveau de batterie**, et la **position**.
    * `cam` : Le flux de la camera 🚨 **Pourrait spécialement être en requête HTTP commme on le faisait à l'époque**
    * `event`: Détails sur un événement quelconque, une erreur, la réception de l'instruction d'une tache, la fin de tache, la détection d'obstacle...

* Serveur -> Robot:
    * `set_parameter(PARAMETER_NAME, VALUE)` : Changer un parametre de valeur (par exemple, 'speed', 'mode')
    * `goto(X=x, Y=y)` : demande d'aller à une position spécifique
    * `move(X'=x', Y'=y')` : déplacemet manuel, entrée en différentiel 
    * `forward(DISTANCE=d)` : déplacement de test, en ligne droite 
    * `rotate(ANGLE=theta)` : déplcement de test, rotation d'un angle

* Serveur -> Interface:
    * `status` : L'état du robot, le **niveau de batterie**, et la **position**. Pour affichage sur la carte.
  
* Interface -> Serveur:
    * `move` : Pour le mode manuel, déplacer un robot avec un control diff
    * `mode` : Changer le mode manuel/auto
    * `stop` : Arrêter un robot.


## Format des requêtes
En règle générale, les messages doivent **TOUS** avoir cette structure :

```json
{
  "type": "...",
  "timestamp": ...,
  "for": ...,
  "data": {...}
}
```
### Robot -> Serveur
Pour les messages du robot vers le serveur, voici les possibilités :
> Chaque barre vertical (|) sépare une possibilitée.

```json
{
  "type": "status|cam|event",
  "for": "server",
  "timestamp": 1700000000.123,
  "data": {
    // Pour 'status'
    "position": {"x": 42, "y": 42, "theta": 42},
    "battery": 42,
    "mode": "auto",

    // Pour 'cam'
    "camera_data": "...",
    
    // Pour 'event'
    "event_name": "obstacle_detected", // par exemple
    "parameters": {
        "distance": 42,
        //...
    }
  }
}
```

#### Quelques exemples

```json
{
  "type": "status",
  "timestamp": 1700000000.123,
  "for": "server",
  "data": {
    "position": {"x": 42, "y": 42, "theta": 42},
    "battery": 42,
    "mode": 1, // 1 pour auto, 0 pour manuel
  }
}
```

```json
{
  "type": "event",
  "timestamp": 1700000000.456,
  "for": "server",
  "data": {
    "event_name": "obstacle_detected",
    "distance": 42
  }
}
```

---

### Serveur -> Robot
Pour les messages du serveur vers un robot, voici les possibilités :
> Chaque barre vertical (|) sépare une possibilitée.

```json
{
  "type": "set_parameter|goto|move|forward|rotate",
  "timestamp": 1700000000.123,
  "for": 1,
  "data": {
    // Pour 'set_parameter'
    "parameter_name":"mode", // ou 'speed'...
    "value": 1,

    // Pour 'goto'
    "x": 42,
    "y": 42,

    // Pour 'move' (déplacement différentiel, valeurs dans [-1,1])
    "x": 0.7,
    "y": -1,

    // Pour 'forward'
    "distance": 42,

    // Pour 'rotate'
    "angle": 90
  }
}
```

#### Quelques exemples

```json
{
  "type": "goto",
  "timestamp": 1700000001.000,
  "for": 2,
  "data": {
    "x": 5.0,
    "y": 2.0,
    "theta": 0.0
  }
}
```

```json
{
  "type": "set_mode",
  "timestamp": 1700000001.200,
  "for": 1,
  "data": {
    "mode": "manual"
  }
}
```

## Note
La vérification des types et des arguments se fait à l'envoie, et non à la réception des messages ws.

---
---

# Ce qu'il y a sur les robots
<ol>
<li>Fonctions de déplacement <i>low level</i> (contrôle des moteurs)</li>
<li>Fonctions de contrôle manuel, et automatique (+ stratégies pour éviter les objets, ...)</li>
<li>Fonctions pour les différents composants (caméra, wattmètre (?), capteurs, ...)</li>
<li><strong><i>PAS d'interface web</i></strong></li>
<li>L'interface des requêtes ws</li>
</ol>

---
---


# Ce qu'il y a sur le serveur
<ol>
<li>Fonction de répartition des taches pour le mode auto.</li>
<li>L'interface web de contrôle</li>
<li>L'interface des requêtes ws</li>
</ol>
