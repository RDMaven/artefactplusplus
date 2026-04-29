## Document de Suivi de projet ARTEFACT ++++++++++

Ce document rend compte de l'avancement du groupe artishow, avec des points de suivi datés correspondants aux différentes séances effectuées en présentiel. 
Pour ne pas multiplier les dates, les travaux réalisés entre deux séances seront placés à la date de la séance suivante.


<details open>
<summary style="font-size: 1.5rem; font-weight: bold;">Architecture du projet (repliable)</summary>

```
artefactplusplus
├── install.sh (préparer le projet)
├── PLANNING.md
├── README.md
├── SUIVI.md (VOUS ÊTES ICI)
├── client/
│   ├── client.py
│   ├── config.py
│   ├── requirements.txt
│   ├── start.sh
│   └── src/
│       ├── camera/
│       │   ├── camera.py
│       │   └── Camera_move.py
│       ├── robot/
│       │   ├── controller.py
│       │   └── driver.py
│       └── utils/
│           ├── math_utils.py
│           └── message_parse_and_build.py
│
├── doc/
│   ├── communication_robot_serveur_interface.md
│   ├── Methode.md
│   ├── odometry.md
│   ├── raspberry.md
│   └── setup.md
│
├── sensors/
│   ├── Hall_sensor.py
│   ├── MPU6050.py
│   ├── PCF8591.py
│   ├── requirements.txt
│   ├── start_sensor.sh
│   └── sens/ (environnement python)
│
└── server/
    ├── config.py
    ├── requirements.txt
    ├── run.py
    ├── start.sh
    ├── graphe/ (interface Map Constructor)
    │   ├── API.md
    │   ├── deploy.sh (git push automatique du dossier Cartes/)
    │   ├── package.json
    │   ├── package-lock.json
    │   ├── run.py
    │   ├── start_graphe.sh (lancement de l'appli web)
    │   ├── utils.py
    │   ├── Cartes/ (vide mais contient les cartes crées par Map Constructor)
    │   └── www_graphe/
    │       ├── graphe.py
    │       ├── web.py
    │       ├── assets/
    │       │   ├── fonts/ (polices d'écritures de la page Web)
    │       │   │   ├── Geo/
    │       │   │   ├── Quicksand/
    │       │   │   └── Tiro_Telugu/
    │       │   ├── script/
    │       │   │   ├── panzoom.js
    │       │   │   ├── script_index.js
    │       │   │   ├── script_index.ts
    │       │   │   ├── script_map.js
    │       │   │   └── script_map.ts
    │       │   ├── src/ (tout un tas d'images pour le site)
    │       │   ├── equipe.css
    │       │   ├── header.css
    │       │   ├── map_build.css
    │       │   ├── style.css
    │       │   └── style_anglais.css
    │       └── templates/
    │           ├── equipe.html
    │           ├── index.html
    │           ├── index_anglais.html
    │           ├── map_builder.html
    │           └── waiting.html
    └── www/ (interface des robots)
        ├── main.py
        ├── assets/
        │   ├── images/ (images de la page web)
        │   ├── scripts/
        │   │   ├── app.js
        │   │   ├── log.js
        │   │   ├── manual-control.js
        │   │   ├── ws.js
        │   │   └── imports/
        │   │       ├── jquery-3.7.1.min.js
        │   │       └──  virtual-joystick.js
        │   └── styles/
        │       ├── app.css
        │       ├── dashboard.css
        │       ├── modules/
        │       │   ├── controls-buttons.css
        │       │   ├── log-console.css
        │       │   ├── return-btn.css
        │       │   └── toggle-button.css
        │       └── robot/
        │           ├── color.css
        │           ├── layout.css
        │           └── main.css
        ├── pages/
        │   ├── index.html
        │   └── robot.html
        └── routes/
            ├── routes.py
            ├── websocket.py
            └── utils
                ├── message_parse_and_build.py
                └── utils_video.py


```

</details>

## Suivi des séances :

### Mercredi 11/02 :

- Toutes les tâches ont été effectuées en groupe
- Prise en main du projet : rencontre avec Dominique Blouin et réception des robots
- Première répartition des rôles
- Récupération d'une partie du matériel (manque : raspberry, antennes, deux robots non encore en l'état)

### Jeudi 19/02 :

- Réunion commune pour **mettre en place le planning.**
- Dès la prochaine séance, les travaux individuels pourront commencer.

### Vendredi 20/02

- Colin : **Récupération de la Raspberry** auprès de Tarik Graba et remplacement de l'adaptateur USB-Serie
- Thibaut : **prise en main de cv2.**

### Lundi 23/02

- Eden : création d'une clé ssh et test de connexion à la raspberry
clonage du git + lecture du code wifibot pour **prise en main préliminaire des capteurs IR**
- Colin : **config PC** pour se connecter à la rasp, documentation hardware robot 
- Thibaut : **prise en main du mouvement de la caméra** et écriture d'un code python pour la commander. 
- Max : **prise en main du déplacement du robot** et moteur, test de différentes vitesses, déplacement linéaire + rotation. 

- Thibaut et Max : ajout de logs sur l'interface web et mise en place d'une connexion **Web Sockets**

### Vendredi 13/03

- Thibaut et Max : Mise en place d'une **VM à Rezel** pour le serveur central
- Thibaut : refonte du [README.md](README.md), définition du graphe de cartographie de l'école
- Max : **Debug et tests** du serveur Web et serveur de suivi
- Colin : aide aux **debugs**

### Lundi 16/03

- Thibaut : **Interface Web** pour les graphes de position (abandonnée depuis...)
- Max : **Contrôle manuel** du robot à partir de l'interface Web

### Vendredi 27/03

- Colin, Max, Thibaut : Rencontre avec les encadrants
- Colin : **Mise en place des cartes SIM** et première connexion au réseau 4G de l'école (avec un ordinateur)
- Thibaut : Récupération du matériel pour la centrale inertielle
    - Mise en place de l'**accéléromètre**
- Max : Changement du joystick de l'interface en **boutons**

### Jeudi 02/04

- Thibaut, Max : Correction de problèmes de l'accéléromètre

### Vendredi 03/04

- Thibaut : 
    - Mise en place de **capteurs à effet Hall**
    - Premiers tests et validation du bon fonctionnement des capteurs
    - Recherche d'un capteur plus précis pour notre application
- Colin : Début de **mise en place de la connexion 4G** au réseau de l'école sur Raspberry Pi


### Vendredi 10/04

- Max: réglage de la **calibration des moteurs** en trouvant le ratio tick/cm
- Thibaut : 
    - Commande des capteurs prévues avec l'encadrant (livraison fin avril)
    - Documentation sur la **reconnaissance d'image** par un modèle d'IA (cours de Stanford)


### Mercredi 15/04 :

- Max et Thibaut : **Tests caméra** ; les mouvements de la caméra peuvent être maîtrisés par le raspberry et par l'utilisateur


### Mardi 28/04 :

- Tous : **Réunion de mi-projet** : modification du planning et réévaluation des objectifs (cf nouveau [planning.md](./PLANNING.md))
- Max : ajout d'un **bouton STOP** pour arrêter le robot


### Évaluation intermédiaire 29/04 :

- Nouveaux objectifs datés fixés pour la semaine 19 afin d'avoir un robot complètement fonctionnel
- Nouvelle **répartition des tâches** (décidée à la [réunion précédente](#mardi-2804-)) validées par l'encadrant.
- Thibaut : Création du **diagramme d'architecture** du projet, pour connaître précisemment la place de chaque fichier dans le git.