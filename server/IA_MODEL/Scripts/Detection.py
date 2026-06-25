import sys
from pathlib import Path

import threading
import time

SERVER_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(SERVER_DIR))

from www.routes.utils.utils_video import *
import math
from model_test import draw_predicted_box
from ultralytics import YOLO

Version = 3
# 1 train à 10 epochs (pb de détection sur les images "loufoques")
# 2 train à 20 epochs
# 3 train à 100 epochs
WEIGHTS = "../Results/best_v" + str(Version) + ".pt"
IMAGES_DIR = "../Dataset/test/images"
LABELS_DIR = "../Dataset/test/labels"
CONF = 0.5
IMGSZ = 320


class detection_by_frame:
    def __init__(self, robot_id):  # robot_id va dégager plus tard
        self.robot_id = robot_id
        self.model = YOLO(WEIGHTS)  # chargé une seule fois, pas à chaque frame
        self.current_frame = None   # dernière frame stockée (cv2)
        self.result = None          # resultat issu de la detection par YOLO (objet Results unique)
        self.box = None             # [(x1,y1),(x2,y2)]
        self.distance = None        # float positif, distance entre robot suiveur et robot repéré
        self.angle = None           # entier relatif, position angulaire du robot suivi
                                     # par rapport au milieu de la frame du robot suiveur
        self.camera_fov = 69.0
        self._detection_lock = threading.Lock()
        self._detection_thread = None
        self._stop_detection = False
        
    def distance_robot(self, frame_store):
        """Calcule la distance estimée à partir de la hauteur de la box."""
        if self.box is None:
            self.distance = None
            return None

        with self._detection_lock:
            box = self.box

        box_height = box[1][1] - box[0][1]  # y2 - y1
        K = 1000  # constante de calibrage de la distance

        if box_height > 0:
            self.distance = round(K / box_height, 2)
        else:
            self.distance = None

        return self.distance

    def angle_robot(self, frame_store):
        """Calcule l'angle horizontal du robot détecté par rapport au centre de la frame."""
        
        with self._detection_lock:
            box = self.box
            frame_width = self.current_frame.shape[1] if self.current_frame is not None else None

        if box is None:
            self.angle = None   
            return None
    
        fx = frame_width / (2.0 * math.tan(math.radians(self.camera_fov) / 2.0))

        box_center_x = (box[0][0] + box[1][0]) / 2
        offset = box_center_x - (frame_width / 2)
        theta = math.degrees(math.atan(offset / fx))
        self.angle = int(theta)
        
        return self.angle

    def img_box(self, frame_store):
        """Récupère la frame courante, fait la détection YOLO, stocke la box et renvoie l'image annotée."""
        current_frame = frame_store.get_frame(self.robot_id)
        result = self.model.predict(source=current_frame, conf=CONF, imgsz=IMGSZ, verbose=False, max_det =1)

        result = result[0] 

        if len(result.boxes) == 0:
            self.box = None
            return self.current_frame

        else:
            best_box = result.boxes[0]
            x1, y1, x2, y2 = map(int, best_box.xyxy[0].tolist())
            box = [(x1, y1), (x2, y2)]

        if box is not None:
            image_box = draw_predicted_box(current_frame, result)
        else :
            image_box = current_frame

        with self._detection_lock:
            self.current_frame = current_frame
            self.result = result
            self.box = box


        return image_box  # return en cv2

    def __str__(self):
        box_str = f"{self.box}" if self.box is not None else "Aucune détection"
        distance_str = f"{self.distance:.2f} m" if self.distance is not None else "N/A"
        angle_str = f"{self.angle}°" if self.angle is not None else "N/A"
        return (
            f"Robot {self.robot_id} | "
            f"Box: {box_str} | "
            f"Distance: {distance_str} | "
            f"Angle: {angle_str}")
    
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