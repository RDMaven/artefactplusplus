import threading, cv2, time, datetime, os
import numpy as np
from config import Config


# Configuration pour les images d'entrainement IA ------- #
CAPTURE_FRAME_FREQUENCY = 30

# Stockeur des frames video des robots ------------------ #
class FrameStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._frames = {}  # key: robot_id, value: latest frame
        # self.last_frame = None
        self.stop = False
        self.compt = 0
        self.inited = False

    def set_frame(self, robot_id: int, frame: np.ndarray):
        """Store the latest frame for a specific robot."""
        if not self.inited:
            self.inited = True
        with self._lock:
            self._frames[robot_id] = frame.copy()

    def get_frame(self, robot_id: int):
        """Retrieve the latest frame for a specific robot. Returns None if not set."""
        if not self.inited:
            return None
        with self._lock:
            frame = self._frames.get(robot_id)
            # if self.last_frame != None and self.last_frame == frame:
            #     return frame.copy() if frame is not None else None
            # self.last_frame = frame

            if self.compt == CAPTURE_FRAME_FREQUENCY:
                self.compt=0
                temp_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
                filename = f"{Config.Path.DATA_DIRECTORY}{temp_time}_frame.jpg"
                if os.path.exists(filename): # Eviter d'avoir deux images la meme seconde
                    return frame.copy() if frame is not None else None
                cv2.imwrite(filename, frame)
            else :
                self.compt += 1

            return frame.copy() if frame is not None else None

# Instance initialisée ici pour pouvoir y accéder depuis différent fichiers
frame_store = FrameStore()


# Générateur du feed mjpeg ------------------------------ #
def mjpeg_generator(client_id: int):
    while not frame_store.stop:
        frame = frame_store.get_frame(client_id)
        if frame is None:
            time.sleep(0.01)
            continue

        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        yield b"--frame\r\n" \
              b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"



        time.sleep(0.01)
