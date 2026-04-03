## Document de Suivi de projet ARTEFACT +++

Ce document rend compte de l'avancement du groupe artishow, avec des points de suivi datés correspondants aux différentes séances effectuées en présentiel. 
Pour ne pas multiplier les dates, les travaux réalisés entre deux séances seront placés à la date de la séance suivante.

### Mercredi 11/02 :

- Toutes les tâches ont été effectuées en groupe
- Prise en main du projet : rencontre avec Dominique Blouin et réception des robots
- Première répartition des rôles
- Récupération d'une partie du matériel (manque : raspberry, antennes, deux robots non encore en l'état)

### Jeudi 19/02 :

- Réunion commune pour mettre en place le planning.
- Dès la prochaine séance, les travaux individuels pourront commencer.

### Vendredi 20/02

- Colin : Récupération de la Raspberry auprès de Tarik Graba et remplacement de l'adaptateur USB-Serie
- Thibaut : prise en main de cv2.

### Lundi 23/02

- Eden : création d'une clé ssh et test de connexion à la raspberry
clonage du git + lecture du code wifibot pour prise en main préliminaire des capteurs IR 
- Colin : config PC pour se connecter à la rasp, documentation hardware robot 
- Thibaut : prise en main du mouvement de la caméra et écriture d'un code python pour la commander. 
- Max : prise en main du déplacement du robot et moteur, test de différentes vitesses, déplacement linéaire + rotation. 

- Thibaut et Max : ajout de logs sur l'interface web et mise en place d'une connexion Web Sockets

### Vendredi 13/03

- Thibaut et Max : Mise en place d'une VM à Rezel pour le serveur central
- Thibaut : refonte du README.md, définition du graphe de cartographie de l'école
- Max : Debug et tests du serveur Web et serveur de suivi
- Colin : aide aux debugs

### Lundi 16/03

- Thibaut : Interface Web pour les graphes de position
- Max : Contrôle manuel du robot à partir de l'interface Web

### Vendredi 27/03

- Colin, Max, Thibaut : Rencontre avec les encadrants
- Colin : Mise en place des cartes SIM et première connexion au réseau 4G de l'école (avec un ordinateur)
- Thibaut : Récupération du matériel pour la centrale inertielle
    - Mise en place de l'accéléromètre
- Max : Changement du joystick de l'interface en boutons

### Jeudi 02/04

- Thibaut, Max : Correction de problèmes de l'accéléromètre

### Vendredi 03/04

- Thibaut : 
    - Mise en place de capteurs à effet Hall
    - Premiers tests et validation du bon fonctionnement des capteurs
    - Recherche d'un capteur plus préci pour notre application
- Colin : Début de mise en place de la connexion 4G au réseau de l'école sur Raspberry Pi