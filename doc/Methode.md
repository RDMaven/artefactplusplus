# Méthodes :

Ce fichier a pour but de lister les différentes méthodes pour actionner les programmes que nous auront à écrire de manière individuelle.

### Caméra :

Pour accéder au flux vidéo de la webcam :

- Regarder quels sont les flux vidéos de la machine observée :
```bash
>>> v4l2-ctl --list-devices
```
Ou encore (pour avoir le nom de la caméra) :
```bash
>>> lsusb
```
- activer l'environnement virtuel : (depuis le répertoire artefactplusplus)
```bash
>>> source ./environ/bin/activate
```

- lancer le fichier python main :
```bash
>>> python3 ./main.py
```
- Vous rendre dans votre navigateur préféré pour taper :
http://localhost:8080

=> PS ça marche bien sûr avec votre webcam perso si vous modifiez dans le fichier .env **CAMERA_ID = 0**.

### VM REZEL :

Connection VM Rezel :

```bash
>>> ssh root@2a09:6847:fa10:1410::306
```