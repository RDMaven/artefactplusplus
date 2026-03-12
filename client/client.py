import asyncio, websockets
from config import Config
from src.utils.message_parse_and_build import message_builder, message_parser
import cv2


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
        if Config.OS_IS_LINUX: # selon si on est sous linux, il faut cv.CAP_V4L2
            cap = cv2.VideoCapture(Config.Camera.ID, cv.CAP_V4L2)              #Valeur propre à mon pc : id = 2
        else:
            cap = cv2.VideoCapture(Config.Camera.ID)

        # Determine timeout for the requested FPS rate.
        timeout_for_fps = round(1/Config.Camera.FPS,3)
        print(f"CAMERA - To achieve {Config.Camera.FPS} FPS, setting timeout to {timeout_for_fps}s")

        # Resize
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 320)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 240)

        try:
            while not self.stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    await asyncio.sleep(0.01)
                    continue

                frame = cv2.resize(frame, (640, 480)) #(320, 240)) # reduce size maybe TODO
                frame = cv2.flip(frame, 1) # flip image TODO enlever pour les robots (peut-être)
                _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70]) # reduce quality

                await self.send("video", -1, buffer.tobytes())
                await asyncio.sleep(timeout_for_fps)

        finally:
            cap.release()
            cv2.destroyAllWindows()

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
