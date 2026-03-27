import asyncio, websockets
from config import Config
from src.utils.message_parse_and_build import message_builder, message_parser
import cv2
from src.camera.camera import Camera


class Counter: # for debug of potentially lost messages (resolved normalement)
    def __init__(self):
        self._counter = 0

    def update(self):
        self._counter +=1
        return self.get()

    def get(self):
        return self._counter


# Client class for the websocket ------------------------ #
class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.stop_event = asyncio.Event()
        self.sent_counter = Counter() # for debug
        self.receive_counter = Counter() # for debug
    
    def counter_status(self): # for debug
        print(f"COUNTERS - Received : {self.receive_counter.get()}. Sent : {self.sent_counter.get()}") 

    async def stop(self):
        self.stop_event.set()

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        print("Connected to server")

    async def send(self, mtype, mfor, *args):
        message = message_builder(mtype, Config.Robot.ID, mfor, args)
        await self.websocket.send(message)
        self.sent_counter.update() # for debug

    async def video_streamer(self):
        camera = Camera()

        try:
            while not self.stop_event.is_set():
                frame = await camera.get_frame()
                await self.send("video", -1, frame)
                await asyncio.sleep(camera.timeout_for_fps)

        finally:
            camera.quit()

    async def event_sender(self): # for testing, TODO faire un sender pour tout les messages du robot !
        while not self.stop_event.is_set():
            await self.send("event", -1, "test", {"test": 99})
            await asyncio.sleep(10)


    async def receiver(self):
        while not self.stop_event.is_set():
            try:
                data = await self.websocket.recv()
                if data == "STOP":
                    self.stop_event.set()
                    print("STOP detected")
                    break

                data_type = message_parser(data)

                self.receive_counter.update() # for debug

            except Exception as e:
                print("Receive error:", e)
                break


    async def run(self):
        await self.connect()

        receiver_task = asyncio.create_task(self.receiver())
        video_task = asyncio.create_task(self.video_streamer())
        event_task = asyncio.create_task(self.event_sender())

        try:
            await asyncio.wait(
                [receiver_task, video_task, event_task],
                return_when=asyncio.FIRST_EXCEPTION
            )

        finally:
            self.stop_event.set()
            print("Je suis arrivé au finally de STOP yeah !")

            for task in [receiver_task, video_task, event_task]:
                task.cancel()

            await asyncio.gather(
                receiver_task,
                video_task,
                event_task,
                return_exceptions=True
            )

            await self.websocket.close()


# Run Client -------------------------------------------- #
if __name__ == "__main__":
    client = WebSocketClient(
        f"ws://{Config.Web.HOST}:{Config.Web.PORT}/ws/{Config.Robot.ID}"
    )
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("Quitting with Ctrl+C...")
