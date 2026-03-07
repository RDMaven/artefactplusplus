import threading, cv2, time
import numpy as np

# Stockeur des frames video des robots ------------------ #
class FrameStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._frames = {}  # key: robot_id, value: latest frame
        self.stop = False

    def set_frame(self, robot_id: int, frame: np.ndarray):
        """Store the latest frame for a specific robot."""
        with self._lock:
            self._frames[robot_id] = frame.copy()

    def get_frame(self, robot_id: int):
        """Retrieve the latest frame for a specific robot. Returns None if not set."""
        with self._lock:
            frame = self._frames.get(robot_id)
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
