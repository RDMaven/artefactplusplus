# Fichier définissant le client WS : récéption, envoie; gestion de threads, gestions d'erreurs.

import asyncio, websockets
from config import Config
from src.utils.message_parse_and_build import message_builder, message_parser
import cv2
from src.camera.camera import Camera
from ws_queue import messages

# ======================================================= #
# DEBUG COUNTER CLASS =================================== #
# ======================================================= #
class Counter: # DEBUG of potentially lost messages (resolved normalement)
    def __init__(self):
        self._counter = 0

    def update(self):
        self._counter +=1
        return self.get()

    def get(self):
        return self._counter


# ======================================================= #
# WEBSOCKET CLIENT ====================================== #
# ======================================================= #
class WebSocketClient:
    """ Client WS pour un robot, qui prend l'url de connection en argument. """
    def __init__(self, uri, debug = False):
        self.uri = uri
        self.websocket = None
        self.stop_event = asyncio.Event()
        self.debug = debug
        if self.debug:
            self.sent_counter = Counter() # DEBUG
            self.receive_counter = Counter() # DEBUG
    
    def counter_status(self): # DEBUG
        print(f"COUNTERS - Received : {self.receive_counter.get()}. Sent : {self.sent_counter.get()}") 

    async def stop(self):
        """ Arrêter le robot n'importe quand avec de l'async."""
        self.stop_event.set()

    async def connect(self):
        """ Initialiser la connection WS. """
        self.websocket = await websockets.connect(self.uri)
        if self.debug : print("Connected to server")

    async def send(self, mtype, mfor, *args):
        """ Formatter et envoyer un message :
        * mtype : le type du message (cf. src.utils.message_parse_and_build)
        * mfor : le code du destinataire (cf. doc) 
        * *args : les arguments nécessaires pour le message (nombre variable d'ou l'*)"""
        message = message_builder(mtype, Config.Robot.ID, mfor, args)
        await self.websocket.send(message)
        if self.debug: self.sent_counter.update() # DEBUG

    async def video_streamer(self):
        """ Fonction pour le thread video, récupère et 
        envoie les frames video à la fréquence paramétrée. """
        camera = Camera()

        try:
            while not self.stop_event.is_set():
                frame = await camera.get_frame()
                await self.send("video", -1, frame)
                await asyncio.sleep(camera.timeout_for_fps)

        finally:
            camera.quit()

    async def sender(self): # DEBUG, TODO faire un sender pour tout les messages du robot !
        # messages.append({"signal": 42})
        while not self.stop_event.is_set():
            while messages:
                msg = messages.pop(0)
                for mtype, mval in msg.items(): # Fausse boucle, il n'y a qu'un élément
                    await self.send(mtype, -1, mval)

            # await self.send("event", -1, "test", {"test": 99})
            await asyncio.sleep(1) # TODO Changer le sleep selon le besoin
        

    async def receiver(self):
        """ Fonction pour le thread de réception des messages WS.
        Parsing et gestion d'erreurs. """
        while not self.stop_event.is_set():
            try:
                data = await self.websocket.recv()
                data_type = message_parser(data)

                if self.debug: self.receive_counter.update() # DEBUG

            except Exception as e:
                await self.send("event", -1, 'ERROR', {"data": f"Robot receiver error: {e}."})
                if self.debug: print("Receive error:", e)
                break


    async def run(self):
        """ Fonction principale du client WS : lance les threads, gère les erreurs."""
        await self.connect()

        receiver_task = asyncio.create_task(self.receiver())
        video_task = asyncio.create_task(self.video_streamer())
        send_task = asyncio.create_task(self.sender())

        try:
            await asyncio.wait(
                [
                    receiver_task, 
                    video_task, 
                    send_task
                    ],
                return_when=asyncio.FIRST_EXCEPTION
            )

        except Exception as e:
            print(e)
        finally:
            self.stop_event.set()
            if self.debug: print("Robot WSClient, arrivé au 'finally' de 'run()' yeah !")

            for task in [
                receiver_task, 
                video_task, 
                send_task
                ]:
                task.cancel()

            await asyncio.gather(
                receiver_task,
                video_task,
                send_task,
                return_exceptions=True
            )

            await self.websocket.close()
            print("Robot WSClient, gracefully stopped the WS connection")


# ======================================================= #
# POUR TESTER LE CLIENT WS ============================== #
# ======================================================= #
if __name__ == "__main__":
    client = WebSocketClient(
        f"ws://{Config.Web.HOST}:{Config.Web.PORT}/ws/{Config.Robot.ID}"
    )
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("Quitting with Ctrl+C...")
