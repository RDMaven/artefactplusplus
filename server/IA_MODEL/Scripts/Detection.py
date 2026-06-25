import sys
from pathlib import Path


SERVER_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(SERVER_DIR))

from www.routes.utils.utils_video import *
import math
from model_test import draw_predicted_box
from ultralytics import YOLO

Version = 3
WEIGHTS = "../Results/best_v" + str(Version) + ".pt"
IMAGES_DIR = "../Dataset/test/images"
LABELS_DIR = "../Dataset/test/labels"
CONF = 0.5
IMGSZ = 320


class detection_by_frame:
    def __init__(self, robot_id):
        self.robot_id = robot_id
        self.model = YOLO(WEIGHTS)
        self.current_frame = None
        self.result = None
        self.box = None
        self.distance = None
        self.angle = None
        self.camera_fov = 69.0

    def distance_robot(self, frame_store):
        """Calcule la distance estimée à partir de la hauteur de la box."""
        if self.box is None:
            self.distance = None
            return None

        box_height = self.box[1][1] - self.box[0][1]
        K = 1000

        if box_height > 0:
            self.distance = round(K / box_height, 2)
        else:
            self.distance = None

        return self.distance

    def angle_robot(self, frame_store):
        """Calcule l'angle horizontal du robot détecté par rapport au centre de la frame."""
        if self.box is None:
            self.angle = None
            return None

        frame_width = self.current_frame.shape[1]
        fx = frame_width / (2.0 * math.tan(math.radians(self.camera_fov) / 2.0))

        box_center_x = (self.box[0][0] + self.box[1][0]) / 2
        offset = box_center_x - (frame_width / 2)
        theta = math.degrees(math.atan(offset / fx))
        self.angle = int(theta)

        return self.angle

    def img_box(self, frame_store):
        """Récupère la frame courante, fait la détection YOLO, stocke la box et renvoie l'image annotée."""
        self.current_frame = frame_store.get_frame(self.robot_id)
        self.result = self.model.predict(
            source=self.current_frame, conf=CONF, imgsz=IMGSZ, verbose=False, max_det=1
        )
        result = self.result[0]

        if len(result.boxes) == 0:
            self.box = None
            return self.current_frame

        best_box = result.boxes[0]
        x1, y1, x2, y2 = map(int, best_box.xyxy[0].tolist())
        self.box = [(x1, y1), (x2, y2)]

        image_box = draw_predicted_box(self.current_frame, result)
        return image_box

    def __str__(self):
        box_str = f"{self.box}" if self.box is not None else "Aucune détection"
        distance_str = f"{self.distance:.2f} m" if self.distance is not None else "N/A"
        angle_str = f"{self.angle}°" if self.angle is not None else "N/A"
        return (
            f"Robot {self.robot_id} | "
            f"Box: {box_str} | "
            f"Distance: {distance_str} | "
            f"Angle: {angle_str}"
        )
    
    def start_detection_loop(self, frame_store, interval=0.5):
        """Lance un thread qui exécute la détection en boucle, toutes les `interval` secondes."""
        self._stop_detection = False

        def loop():
            while not self._stop_detection:
                self.img_box(frame_store)
                self.distance_robot(frame_store)
                self.angle_robot(frame_store)
                time.sleep(interval)

        self._detection_thread = threading.Thread(target=loop, daemon=True)
        self._detection_thread.start()

    def stop_detection_loop(self):
        """Arrête le thread de détection."""
        self._stop_detection = True
        if self._detection_thread is not None:
            self._detection_thread.join()

    def mjpeg_generator_with_box(self, frame_store):
        """Génère un flux MJPEG des frames annotées (box dessinée) pour affichage côté serveur."""
        while not self._stop_detection:
            with self._detection_lock:
                frame = self.current_frame
                result = self.result
                box = self.box
                print(self)

            if frame is None:
                time.sleep(0.01)
                continue

            annotated = draw_predicted_box(frame, result[0]) if box is not None else frame

            ret, buffer = cv2.imencode(".jpg", annotated)
            if not ret:
                continue

            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
            time.sleep(0.01)