## Document de Suivi de projet ARTEFACT ++++++++++

Ce document rend compte de l'avancement du groupe ARTEFACT++++++++++++, avec des points de suivi datés correspondants aux différentes séances effectuées en présentiel. 
> **Pour ne pas multiplier les dates, les travaux réalisés entre deux séances seront placés à la date de la séance suivante.**


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

---

## Suivi des séances

### Mercredi 11/02

> Toutes les tâches ont été effectuées en groupe.
- Prise en main du projet : rencontre avec Dominique Blouin et réception des robots.
- Première répartition des rôles.
- Récupération d'une partie du matériel (manque : raspberry, antennes, deux robots non encore en l'état).


### Jeudi 19/02

- Réunion commune pour **mettre en place le planning.**
- Dès la prochaine séance, les travaux individuels pourront commencer.


### Vendredi 20/02

- Colin : **Récupération de la Raspberry** auprès de Tarik Graba et remplacement de l'adaptateur USB-Serie
- Thibaut : **prise en main de cv2.**
- Max : Architecture générale (fichiers d'env, de configuration, squelette du projet), et du serveur web (Flask), pages web de dashbard (général) et de contrôle robot individuel (flux video, animations...). Proposition d'une doc "API" pour la communication Robot-Serveur. Mise en place des canaux WS (interface-serveur).


### Lundi 23/02

- Eden : création d'une clé ssh et test de connexion à la raspberry
clonage du git + lecture du code wifibot pour **prise en main préliminaire des capteurs IR**
- Colin : **config PC** pour se connecter à la rasp, documentation hardware robot 
- Thibaut : **prise en main du mouvement de la caméra** et écriture d'un code python pour la commander. 
- Max : Premières classes haut niveau pour le contrôle manuel. **Prise en main du déplacement du robot** et moteur, test de différentes vitesses, déplacement linéaire + rotation.

- Thibaut et Max : Debug (déjà...) du WS (ne fonctionnait que sous Linux). Adaptation des fonctions caméra à l'environment Linux. Ajout de logs sur l'interface web.


### Vendredi 13/03

- Max (Inter-séance) :
    - Migration du serveur web de Flask vers FastAPI pour une vraie implémentation de WS. (27/02)
    - Nouveau style des pages web 'robot'. Liaison des nouveaux éléments HTML aux fonctions JS + WS. (27/02)
    - Debug de la compatibilité Linux de la caméra. (27/02)
    - Réorganisation du code du serveur web : fichier principale, routes, ws. (28/02)
    - Gestionnaire WS sur le serveur pour toutes les connections. (28/02)
    - Import et lien d'un joystick avec le projet (sur l'interface; envoie/réception ws). (28/02)
    - V1 du client WS pour les robots (connection, parsing, affichage) (05/03)
    - Adaptation du flux video par ws (robot -> serveur -> interface). (05/03)
    - Debug des erreurs causées par interruptions/déconnexions WS : gestion propre, "graceful stops" des canaux WS. (07/03)
    - Architecture : séparation du projet en deux partie : client/ et serveur/. (07/03)
    - Définition (et unification) d'un format clair pour les messages WS; mise en place de nouveaux types de message. (12/03)


- Thibaut et Max : Mise en place d'une **VM à Rezel** pour le serveur central
- Thibaut : refonte du [README.md](README.md), définition du graphe de cartographie de l'école
- Max : **Debug et tests** du serveur Web et serveur de suivi. Reprise des fonctions de mouvement robot 'auto' du projet Artefact.
- Colin : aide aux **debugs**


### Lundi 16/03

- Max (Inter-séance) : Script d'installation du projet pour UNIX. (14/03)

- Thibaut : **Interface Web** pour les graphes de position (abandonnée depuis...)
- Max : **Contrôle manuel** du robot à partir de l'interface Web. Le robot à 4 roues, le joystick est donc inutilisable (flop). 


### Vendredi 27/03

- Colin, Max, Thibaut : Rencontre avec les encadrants 
- Colin : **Mise en place des cartes SIM** et première connexion au réseau 4G de l'école (avec un ordinateur)
- Thibaut : Récupération du matériel pour la centrale inertielle
    - Mise en place de l'**accéléromètre**
- Max : Changement du joystick de l'interface en **boutons**. Documentation et implémentation d'une odométrie simple pour nos mouvements.


### Jeudi 02/04

- Thibaut, Max : Correction de problèmes de l'accéléromètre


### Vendredi 03/04

- Thibaut : 
    - Mise en place de **capteurs à effet Hall**
    - Premiers tests et validation du bon fonctionnement des capteurs
    - Recherche d'un capteur plus précis pour notre application
- Colin : Début de **mise en place de la connexion 4G** au réseau de l'école sur Raspberry Pi


### Vendredi 10/04

- Max: réglage de la **calibration des moteurs** en trouvant le ratio tick/cm. Débug du contrôle manuel : mise en place d'un démarrage systématique des moteurs avant contrôle.
- Thibaut : 
    - Commande des capteurs prévues avec l'encadrant (livraison fin avril)
    - Documentation sur la **reconnaissance d'image** par un modèle d'IA (cours de Stanford)


### Mercredi 15/04

- Max et Thibaut : **Tests caméra** ; les mouvements de la caméra peuvent être maîtrisés par la raspberry, et depuis l'interface, avec l'ajout de boutons et communication ws.


### Mardi 28/04

- Tous : **Réunion de mi-projet** : modification du planning et réévaluation des objectifs (cf nouveau [planning.md](./PLANNING.md))
- Max : ajout d'un **bouton STOP** pour arrêter le robot.


### Évaluation intermédiaire 29/04

- Nouveaux objectifs datés fixés pour la semaine 19 afin d'avoir un robot complètement fonctionnel
- Nouvelle **répartition des tâches** (décidée à la [réunion précédente](#mardi-2804-)) validées par l'encadrant.
- Thibaut : Création du **diagramme d'architecture** du projet, pour connaître précisemment la place de chaque fichier dans le git.


### Mardi 05/05

- Max (Inter-Séance): 
    - Refonte du contrôle clavier sur l'interface web : avant, certaines actions fonctionnaient sur toutes les touches, maintenant elles sont toujours spéficiques à certaines touches. Ajout de touches pour arrêter le robot. (29/04) 
    - Première version de la documentation et du pseudo-code pour les modes auto (traque et carographie). (29/04) 
    - Travail sur un algorithme de parcours du robot sur un carte prédéfinie pour la cartographie 4G : un DFS modifié (29/04). Amélioration, reconstruction du parcours, nettoyage du code, commentaires, doc et fin. (30/04)
    - Ajout et unification des commentaires coté client, tracking de la rotation de la caméra. (01/05)

- Max et Thibaut : Refléxion et aboutissement d'une méthode pour intégrer la détéction d'obstacles au mode auto du robot.

### Mercredi 13/05
### Mercredi 27/05
### Mercredi 10/06
### Lundi 15/06
### Mardi 16/06
### Lundi 22/06
### Mardi 23/06
### Mercredi 24/06
### Jeudi 25/06
### Vendredi 26/06
