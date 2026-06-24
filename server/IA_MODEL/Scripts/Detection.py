import sys
from pathlib import Path

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
        
    def distance_robot(self, frame_store):
        """Calcule la distance estimée à partir de la hauteur de la box."""
        if self.box is None:
            self.distance = None
            return None

        box_height = self.box[1][1] - self.box[0][1]  # y2 - y1
        K = 1000  # constante de calibrage de la distance

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
    
        frame_width = self.current_frame.shape[1]  # largeur réelle de la frame en cours (en pixels)
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
            source=self.current_frame, conf=CONF, imgsz=IMGSZ, verbose=False
        )

        result = self.result[0] 

        if len(result.boxes) == 0:
            self.box = None
            return self.current_frame

        # s'il y a plusieurs détections, on garde la plus confiante
        box = max(result.boxes, key=lambda b: b.conf.item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        self.box = [(x1, y1), (x2, y2)]

        image_box = draw_predicted_box(self.current_frame, result)
        return image_box  # return en cv2

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