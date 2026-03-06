import threading
import numpy as np

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

# singleton instance
frame_store = FrameStore()