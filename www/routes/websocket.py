from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
import json, asyncio
from www.routes.utils.message_parse_and_build import \
    interface_message_parser, robot_message_parser, \
    message_builder
from www.routes.utils.frame_store import frame_store
router = APIRouter()
shutdown_event = asyncio.Event()


class WSClient:
    Ci = 0 # C(lient)i(ndex)
    def __init__(self, websocket, client_id):
        self.ws = websocket
        self.id = client_id
        self.is_robot = self.id != 0
        self.name = f"ROBOT {client_id}" if self.is_robot else "THE INTERFACE"

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



class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    def get_client(self, client_id):
        if client_id not in self.active_connections:
            print(f"Le client d'ID {client_id} n'existe pas.")
            return None
        else:
            return self.active_connections[client_id]

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        assert client_id not in self.active_connections, f"Client ID {client_id} is already in use, can't connect"
        client = WSClient(websocket, client_id)
        self.active_connections[client_id] = client
        print(f"CLIENT CONNECTED : {client.name}")
        if client_id == 0:
            print("ACTIVATING THE VIDEO FEED")
            frame_store.stop = False
        await client.send(f"Hi from server, you are {client.name}")

    async def disconnect(self, client_id):
        client = self.get_client(client_id)
        if client:
            # await client.send("STOP")
            # await asyncio.sleep(2)
            if client_id == 0:
                print("STOPPING THE VIDEO FEED")
                frame_store.stop = True
            print(f"CLIENT DISCONNECTED : {client.name}")
            del self.active_connections[client_id]
        
    # async def broadcast_shutdown(self):
    #     print("Here, nb of clients : ", len(self.active_connections))
    #     for client in self.active_connections.values():
    #         try:
    #             await client.send("Server is shutting down…")
    #             await client.ws.close()
    #         except Exception:
    #             pass
    #     self.active_connections.clear()

# Let me talk to your MANAGER (manager instance init)
manager = ConnectionManager()


# Main WebSocket loop
@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id) #  Register the client
    client = manager.get_client(client_id) 

    try:
        while True:
            data = await websocket.receive_text() # Wait for a message
            data_type = client.parse(data) # Parse the message

            if data_type != "video": # Pong when it's not a video frame (else the terminal would explode)
                await client.send(
                    f"Received '{data_type.upper()}' message from you, {client.name}."
                )

    except WebSocketDisconnect:
        await manager.disconnect(client_id)

    except KeyboardInterrupt:
        pass

    

