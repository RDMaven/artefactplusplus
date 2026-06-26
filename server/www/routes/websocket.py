# ------------------------------------------------------- #
# GESTION DE COMMUNICATION WEBSOCKET -------------------- #
# ------------------------------------------------------- #

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body 
import json, asyncio, os

from www.routes.utils.message_parse_and_build import \
    interface_message_parser, robot_message_parser, \
    message_builder
from www.routes.utils.utils_video import frame_store
from control_logic.main_auto_cartographie import cartographie

from pathlib import Path
from config import Config
from fastapi.responses import HTMLResponse



# Init router, et évenement d'arrêt général ------------- #
router = APIRouter()
shutdown_event = asyncio.Event()


# Profil pour un client WebSocket ----------------------- #
class WSClient:
    def __init__(self, websocket, client_id):
        self.ws = websocket
        self.id = client_id
        self.is_robot = (self.id != 0)
        self.name = f"ROBOT {client_id}" if self.is_robot else "INTERFACE"

    # MÉTHODES DE COMMUNICATIONS --------------------
    # -> Recevoir depuis robot/interface ------------
        # Assigner la bonne fonction de parsing pour recevoir des messages
        if self.is_robot:
            self.parse = lambda d: robot_message_parser(d, self.name, self.id)
        else:
            self.parse = lambda d: interface_message_parser(d, self.name)
        
    # -> Envoyer vers robot/interface ---------------
    # TODO
    async def send(self, message: str):
        await self.ws.send_text(message)


# Gestionnaire des communications WS
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    def get_client(self, client_id):
        return self.active_connections.get(client_id) # None si inexistant

    def print_status(self):
        print(f"STATUS - Currently have {len(self.active_connections)} connections : ", end="")
        print(", ".join(client.name for client in self.active_connections.values()))

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        assert client_id not in self.active_connections, f"Client ID {client_id} is already in use, can't connect"
        client = WSClient(websocket, client_id)
        self.active_connections[client_id] = client
        print(f"STATUS - CLIENT CONNECTED : {client.name}")
        if client_id == 0:
            print("STATUS - ACTIVATING THE VIDEO FEED")
            frame_store.stop = False
        await client.send(message_builder("message", client_id, f"Hi from server, you are {client.name}"))
        self.print_status()

    async def disconnect(self, client_id):
        client = self.get_client(client_id)
        if client:
            if client_id == 0:
                print("STATUS - STOPPING THE VIDEO FEED")
                frame_store.stop = True
            print(f"STATUS - CLIENT DISCONNECTED : {client.name}")
            del self.active_connections[client_id]
        self.print_status()

# Let me talk to your MANAGER (manager instance init)
manager = ConnectionManager()

def ask_client():
    return list(manager.active_connections.keys())


# Main WebSocket loop
@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id) #  Register the client
    client = manager.get_client(client_id) 

    # POUR L'INTERFACE, envoyer la liste des cartes disponibles
    if client_id == 0:
        cartes = {i: f.name for i, f in enumerate(Path(Config.Path.MAPS_DIRECTORY).glob("*.txt"))}
        await client.send(message_builder("maps_list", 0, cartes))

    # Boucle principale ws
    try:
        while True:
            data = await websocket.receive_text() # Wait for a message
            data_type, data_for = client.parse(data) # Parse the message
            
            # Forward message (ex. Robot 1 -> Server -> Interface, 
            # alors les messages ne sont pas pour le serveur (-1) d'où la condition)
            if data_for != -1 and data_type not in ["carto_init", "traque_init"]: 
                recipient = manager.get_client(data_for)
                if recipient:
                    await recipient.send(data)

                    await client.send(message_builder("message", data_for, f"ACK - Forwarded '{data_type.upper()}' message ({client.name} -> {recipient.name})."))
                else:
                    await client.send(message_builder("message", data_for, f"ALERT - Client {manager.get_client(data_for)} offline."))
                continue
            

            # Pong when it's not a video frame (else the terminal would explode)
            if data_type != "video" and data_type != "ack":
                await client.send(message_builder("message", data_for, f"ACK - Received '{data_type.upper()}' message ({client.name} -> {data_for})."))


            # La spéciale redondante pour lancer les modes auto
            if data_type in ["carto_init", "traque_init"]:
                data = json.loads(data)
                _, _, rfor, _, rdata = data.values()
                recipient = manager.get_client(rfor)
                if not recipient:
                    await client.send(message_builder("message", data_for, f"ALERT - Client {manager.get_client(data_for)} offline."))
                else:
                    match data_type:
                        case "carto_init":
                            cmap, cx, cy = rdata.values()
                            # TODO Récupérer l'échelle de la carte, ici 1 par défaut
                            await cartographie(recipient, cmap, 90, cx, cy)
                        case "traque_init":
                            pass # TODO


    except WebSocketDisconnect:
        await manager.disconnect(client_id)

    except KeyboardInterrupt:
        pass

