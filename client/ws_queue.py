# File de message à envoyer en websocket. Placée ici pour :
# - pouvoir les ajouter lorsqu'on recoit une requête 'get_signal' sur serveur
# - pouvoir les ajouter lors d'un événement du robot
# - pouvoir les envoyer avec client.py

from queue import Queue

messages = Queue()