#c'est un fichier de test crée par Claude

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import cv2

SERVER_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(SERVER_DIR))

from Detection import DetectionByFrame

def box_attendue(id_test):
    label_path = Path(f"../Dataset/test/labels/{id_test}.txt")
    image_path = Path(f"../Dataset/test/images/{id_test}.jpg")

    if not label_path.exists():
        return None

    img = cv2.imread(str(image_path))
    if img is None:
        return None

    h, w = img.shape[:2]

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
    """Simule un FrameStore en renvoyant toujours la même image de test."""
    def __init__(self, image_path):
        self.frame = cv2.imread(str(image_path))
        if self.frame is None:
            raise FileNotFoundError(f"Impossible de charger l'image : {image_path}")

    def get_frame(self, robot_id):
        return self.frame.copy()

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        id_test = sys.argv[1] if int(sys.argv[1])<13 else 1
    else:
        id_test=1


    test_image_path = f"../Dataset/test/images/{id_test}.jpg"

    frame_store = FakeFrameStore(test_image_path)
    detector = DetectionByFrame(robot_id=1)

    visible, annotated, angle = detector.isthereRobot(frame_store)

    detector.distance_robot()
    print(detector)
    print(visible, angle)

    box = box_attendue(id_test)
    print("box attendue : ", box)

    img_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 6))
    plt.imshow(img_rgb)
    plt.title("Box prédite")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
