#c'est un fichier de test crée par Claude

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import cv2

import threading
import time

SERVER_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(SERVER_DIR))

from Detection import detection_by_frame 

def box_attendue(id_test):
    label_path = Path(f"../Dataset/test/labels/{id_test}.txt")
    if not label_path.exists():
        return None

    h, w = cv2.imread(f"../Dataset/test/images/{id_test}.jpg").shape[:2]

    with open(label_path, "r") as f:
        for line in f.readlines():
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            _, x_center, y_center, box_w, box_h = map(float, parts)
            x_center *= w
            y_center *= h
            box_w *= w
            box_h *= h
            x1 = int(x_center - box_w / 2)
            y1 = int(y_center - box_h / 2)
            x2 = int(x_center + box_w / 2)
            y2 = int(y_center + box_h / 2)
            return [(x1, y1), (x2, y2)]

    return None

class FakeFrameStore:
    """Simule un FrameStore en cyclant entre plusieurs images de test à chaque appel."""
    def __init__(self, images_dir, num_images=10):
        self.frames = []
        for i in range(1, num_images + 1):
            frame = cv2.imread(f"{images_dir}/{i}.jpg")
            if frame is None:
                raise FileNotFoundError(f"Impossible de charger l'image : {images_dir}/{i}.jpg")
            self.frames.append(frame)
        self._index = 0

    def get_frame(self, robot_id):
        frame = self.frames[self._index]
        self._index = (self._index + 1) % len(self.frames)
        return frame.copy()

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        id_test = sys.argv[1] if int(sys.argv[1])<11 else 1
    else:
        id_test=1


    frame_store = FakeFrameStore("../Dataset/test/images", num_images=10)
    detector = detection_by_frame(robot_id=1)

    annotated = detector.img_box(frame_store)

    detector.distance_robot(frame_store)
    detector.angle_robot(frame_store)
    print(detector)

    box = box_attendue(id_test)
    print("box attendue : ", box)

    # --- Test du thread de détection en boucle ---
    print("\nDémarrage du thread de détection (boucle toutes les 0.5s)...")
    detector.start_detection_loop(frame_store, interval=0.5)

    time.sleep(2)  # laisse le thread tourner quelques cycles
    print("État après 2s de boucle :", detector)

    # --- Test du générateur de flux MJPEG (sans serveur Flask, juste vérifier qu'il produit des frames) ---
    print("\nTest du générateur de flux MJPEG (3 frames récupérées)...")
    gen = detector.mjpeg_generator_with_box(frame_store)
    for i in range(3):
        chunk = next(gen)
        print(f"Frame {i+1} reçue, taille du chunk : {len(chunk)} octets")

    detector.stop_detection_loop()
    print("\nThread de détection arrêté.")

    img_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 6))
    plt.imshow(img_rgb)
    plt.title("Box prédite")
    plt.axis("off")
    plt.tight_layout()
    plt.show()