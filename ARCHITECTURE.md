### Architecture du projet :

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