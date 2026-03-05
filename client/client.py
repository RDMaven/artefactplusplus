import asyncio, websockets
from config import Config
from communication_utils import message_builder, message_parser


# Client class for the websocket ------------------------ #
class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.stop_event = asyncio.Event()
    
    async def stop(self):
        self.stop_event.set()

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        print("Connected to server")

    async def send(self, mtype, mfor, *args):
        message = message_builder(mtype, mfor, args)
        await self.websocket.send(message)

    async def run(self):
        await self.connect()

        while not self.stop_event.is_set():
            data = await self.websocket.recv()
            data_type = message_parser(data)

            await asyncio.sleep(5)

            # test TODO enlever 
            await self.send("event", "server", "test", {"prout": 99})
                
        await self.websocket.close()

async def stop_listener(client):
    await asyncio.to_thread(input, "Press ENTER to stop\n")
    await client.stop()

# ---- Run Client ----
async def main():
    client = WebSocketClient(f"ws://{Config.Web.HOST}:{Config.Web.PORT}/ws/{Config.Robot.ID}") # TODO : automatically assign a number, no hardcoded 1.
    await asyncio.gather(
       client.run(),
        stop_listener(client)
    )


if __name__ == "__main__":
    asyncio.run(main())