## Document de Suivi de projet ARTEFACT ++++++++++

Ce document rend compte de l'avancement du groupe ARTEFACT++++++++++++, avec des points de suivi datés correspondants aux différentes séances effectuées en présentiel. 
> **Pour ne pas multiplier les dates, les travaux réalisés entre deux séances seront placés à la date de la séance suivante.**

## Suivi des séances

### Mercredi 11/02

> Toutes les tâches ont été effectuées en groupe.
- Prise en main du projet : rencontre avec Dominique Blouin et réception des robots.
- Première répartition des rôles.
- Récupération d'une partie du matériel (manque : raspberry, antennes, deux robots non encore en l'état).


### Jeudi 19/02

- Réunion commune pour **mettre en place le planning.**
- Dès la prochaine séance, les travaux individuels pourront commencer.
- Thibaut : **prise en main de cv2**


### Vendredi 20/02

- Colin : **Récupération de la Raspberry** auprès de Tarik Graba et remplacement de l'adaptateur USB-Serie
- Thibaut : 
    - **Première interface caméra** : récupération du flux et affichage sur un serveur web
    - Modifications d'environnement
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
- Thibaut :
    - refonte du [README.md](README.md)
    - Début de la création d'une application pour représenter les cartes utilisées par le robot avec des **graphes**
- Max : **Debug et tests** du serveur Web et serveur de suivi. Reprise des fonctions de mouvement robot 'auto' du projet Artefact.
- Colin : aide aux **debugs**


### Lundi 16/03

- Max (Inter-séance) : Script d'installation du projet pour UNIX. (14/03)

- Thibaut : 
    - **Interface Web** pour les graphes de position, appellé **MAP_CONSTRUCTOR** (abandonnée depuis...)
    - Mise en place d'une **liaison websocket** avec un background python pour cette interface web
- Max : **Contrôle manuel** du robot à partir de l'interface Web. Le robot à 4 roues, le joystick est donc inutilisable (flop). 


### Vendredi 27/03

- Thibaut (interséance) :
    - 18/03 : **git push automatique** sur l'interface web de MAP_CONSTRUCTOR lors de l'export d'un graphe pour qu'elle soit accessible à tous
    - 19/03 : possibilité d'importer des images dans MAP_CONSTRUCTOR (et donc des cartes pour dessiner un graphe dessus)
    - 19/03 : Mise en place de la création de graphe.
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

- Thibaut (04/05):
    - Réception des nouveaux composants
    - Recherche d'un algorithme pour gérer le MPU-9250/6050
    - Réglages de bug avec le bus I2C
- Max (Inter-Séance): 
    - Refonte du contrôle clavier sur l'interface web : avant, certaines actions fonctionnaient sur toutes les touches, maintenant elles sont toujours spéficiques à certaines touches. Ajout de touches pour arrêter le robot. (29/04) 
    - Première version de la documentation et du pseudo-code pour les modes auto (traque et carographie). (29/04) 
    - Travail sur un algorithme de parcours du robot sur un carte prédéfinie pour la cartographie 4G : un DFS modifié (29/04). Amélioration, reconstruction du parcours, nettoyage du code, commentaires, doc et fin. (30/04)
    - Ajout et unification des commentaires coté client, tracking de la rotation de la caméra. (01/05)
- Colin :
    - Branchement de l'antenne
    - Mise en place de la configuration réseau à partir de l'antenne
- Thibaut :
    - Tests de la raspberry avec un **Voltmètre** pour vérifier que les ports SDA et SLC ne sont pas court-circuités
    - Mise en évidence de la nécessité de **souder** les composants
    - Début de la création de **MAP_CONSTRUCTOR_2.0**, interface web permettant de modéliser des cartes non pas à partir de graphes, mais d'une grille de pixels

- Max et Thibaut : 
    - Refléxion et aboutissement d'une méthode pour intégrer la détéction d'obstacles au mode auto du robot.

### Mercredi 13/05

- Thibaut (07/05) : mise en place d'une réception de fichiers images sur l'interface web de MAP_CONSTRUCTOR_2.0
- Thibaut (09/05) : mise en place d'un fichier *start.sh* global permettant d'accéder aux différents applications présentes dans le git sans succomber aux dédales de notre architecture...
- Max (06/05) : Code d'évitement d'obstacle, calcul des nouvelles coordonnées vers l'objectif après évitement et adaptation des fonction pour les modes automatiques. 
- Thibaut (11/05) : Début du rapport "Enjeux"
- Thibaut (12/05) : Accès aux cartes MAP_CONSTRUCTOR2.0
- Colin (12/05) : Ajout d'une fonction de test de vitesse et qualité de connexion Wifi

- Colin : Modification de la fonction de test de vitesse et qualité de connexion Wifi pour l'adapter à la connexion 4G
- Max : Rédaction, reformuation, et fin du rapport "Enjeux".
- Thibaut : Modèle théorique du stockage et de la modélisation d'une carte sur le Git

### Mercredi 27/05

- Thibaut (14/05) : Mise en place de la grille sur MAPCONSTRUCTOR 2.0 pour modéliser la carte, et mise en place d'un cache pour mémoriser les modifications.
- Thibaut (15 et 16/05) : Fin de MAPCONSTRUCTOR 2.0 : export de fichiers directement sur le git, mise en place d'une grille sur l'interface web pour fabriquer les cartes à partir de photos importées.
- Colin : Réalisation que les fonctions établies précédemment pour les tests de la qualité de connexion ne fonctionneront pas avec l'architecture que l'on voudrait utiliser pour le robot -> de retour à la prise en main de minicom
- Max : Fix de bugs avec le mouvement de la caméra au startup, et mise en place de la capture automatique de frame pour l'entrainement de l'IA (traque).

### Jeudi 04/06

- Réunion de groupe (tout le monde présent) avec Jean-Sébastien Gomez pour discuter de l'avancée du projet

### Mercredi 10/06

- Colin (07/06) : Prise en main de minicom (suite)
- Colin (09/06) : Prise en main de minicom (suite suite)
- Colin : Connexion au réseau 4G (enfiiiin !!!) et premiers tests de connexion et de position GPS
- Max : Ajout d'un toggle pour la capture de frames pour l'entrainement de l'IA (traque) sur l'interface, reliée au projet.
- Thibaut : Recherche bibliographique sur la mise en place d'un filtre de Kalman pour notre capteur MPU6050 et apprentissage du principe de foncionnement d'un tel filte - j'ai trouvé un git avec un code adaptable à notre capteur

### Lundi 15/06

Présent : tous 
Durée : 7h00
On a fait une affiche de fou ! Des talents de designer ont été révélé partout !

### Lundi 22/06

- Eden (07/06): recherche sur l'implémentation d'un model de reconnaissance d'objet (du robot) YOLO pour la mise en place d'une traque. Objectif de séance : avoir une idée de comment créer un dataset efficace et adapté à notre utilisation et une idée de comment implémenter et entrainer notre modèle
Ressources : [yolo_from_scratch](https://medium.com/@whyamit404/how-to-implement-a-yolo-object-detector-from-scratch-in-pytorch-e310829d92e6); [single_object_detection](https://stackoverflow.com/questions/51782769/object-detection-for-a-single-object-only)
- Thibaut : Création d'un filtre de kalman pour filtrer les données provenant du capteur MPU6050. Voici le résultat lorsque le capteur est immobile pour la rotation et les accélérations. On voit que le filtrage fonctionne bien après une période transitoire.
<div style="display: flex; width:100%;"><img style="witdh : 60%;" src="./doc/Capture d’écran du 2026-06-23 00-06-51.png"></div>
- Max : Premiers tests des capteurs ultrasons, insertion dans le projet, et complétion du code de détéction d'obstacles.

### Mardi 23/06

- Colin : changement de programme pour récupérer la qualité de connexion 4G -> passage à pyserial + réimplantation dans le nouveau système
- Thibaut : 
    - Mise en forme globale du robot, avec la mise en commun des capteurs, du débeugage, et enfin la refonte du système d'alimentation du raspberry.
    - Configuration de la seconde raspberry pour le robot de la traque 
- Eden : Création d'un dataset d'images du robot, incluant des photos floues, et sous différentes conditions. Séparation de ce dataset en Train, Valid, Test. Implémentation YOLOv8 et training sur 10, 20 puis 100 epochs. --> 100 epochs fonctionne pour les photos telles que robot flou, robot à longue distance, robot coupé par le cadre
- Max : 
  - Développement d'une feature web : le choix interactif du mode auto voulu, et des paramètres associés (la carte, la position de départ), et reliage effectif en WS pour lancer ces modes avec les paramètres. 
  - Correction mineur sur le style de Map Constructor (marges). 
  - Implémentation d'une file de messages pour la gestion des commandes à exécuter côté robot (goto, get_signal), et variables de suivi de leur exécution (afin de savoir quand le serveur peut envoyer la commande suivante). Tests.

### Mercredi 24/06

- Thibaut :
    - Mise en place du robot avec tous les capteurs au Fablab. Impression de support en bois pour les fixations.
    - Implémentations et mesure précise du bruit sur le MPU6050
    - Début d'une interface web pour suivre les robots pour la présentation finale
- Max:
  - Gestion des messages type "position" de l'interface vers les robot en WebSocket.
  - Gestion des cartes générées par MAP_CONSTRUCTOR (elles n'ont pas exactement le même type que les cartes importées à la main).
  - Gestion du cas des positions initiales invalides lors d'une exécution de la cartographie.
  - Ajout de la V1 de la potition par centrale inertielle et filtre de Kalman au robot.
  - Implémentation d'une fonction de récupération (et d'affichage) continue des position par odométrie et kalman, afin de comparer et tester.
  - Réparation des mouvement de la caméra (tout était inversé), et adaptation du pas de rotation, et du temps d'attente entre chaque commande.
  - Correction fondamentale du sens pour tout controle de déplacement du robot : on l'a monté à l'envers de ce qui était prévu...; Optimisations.
- Colin : correction de conflits entre WiFi et 4G


### Jeudi 25/06

- Colin : Assemblage des fonctions de test de la qualité de connexion 4G avec le mode automatique

### Vendredi 26/06
