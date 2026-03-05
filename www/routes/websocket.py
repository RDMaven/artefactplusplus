from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
import json
from www.routes.utils.message_parse_and_build import \
    interface_message_parser, robot_message_parser, \
    message_builder

router = APIRouter()

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
            self.receive = lambda d: robot_message_parser(d, self.name)
        else:
            self.receive = lambda d: interface_message_parser(d, self.name)

        # -> Envoyer vers robot/interface ---------------
        # TODO


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WSClient] = []

    def get_client(self, client_id):
        selected_client = [c for c in self.active_connections if c.id == client_id]
        assert len(selected_client) == 1, "Plusieurs clients ont le même id !"
        return selected_client[0]

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        assert all([c.id != client_id for c in self.active_connections]), "The client ID for this new connection is already in use."
        client = WSClient(websocket, client_id)
        self.active_connections.append(client)
        await self.send_personal_message(f"Hi, you are {client.name}", websocket)

    def disconnect(self, client_id):
        self.active_connections.remove(self.get_client(client_id))

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.ws.send_text(message)
    
manager = ConnectionManager()
    

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)

    try:
        # once = False
        while True:
            data = await websocket.receive_text()
            client = manager.get_client(client_id)
            data_type = client.receive(data)
            # print(f"Recieved from {client_id} : {data}")

            await manager.send_personal_message(
                f"{data_type.upper()} message recieved from {client.name}.", websocket
            )
            
            # TODO enlever ce test
            # if not once and not client.is_robot:
            #     await manager.send_personal_message(
            #         str(message_builder("status", "interface", 42, {"x": 0, "y": 1, "theta": 90})),
            #         websocket
            #     )
            #     once = True
                

            # await manager.broadcast(
            #     f"Client #{client_id} says: {data}"
            # )

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(
            f"Client #{client_id} left the chat"
        )
