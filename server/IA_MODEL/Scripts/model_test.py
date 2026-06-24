from pathlib import Path
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

Version = 3
#1 train à 10 epochs (pb de détection sur les images "loufoques")
#2 train à 20 epochs
#3 train à 100 epochs

WEIGHTS = "../Results/best_v" + str(Version) + ".pt"
IMAGES_DIR = "../Dataset/test/images"
LABELS_DIR = "../Dataset/test/labels"
CONF = 0.5
IMGSZ = 320

def draw_predicted_box(image, result):
    """Dessine les bounding boxes prédites par le modèle (en rouge)."""
    img = image.copy()
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = float(box.conf[0])
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 5)
        cv2.putText(img, f"{conf:.2f}", (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return img


def draw_ground_truth_box(image, label_path):
    """Dessine les bounding boxes annotées manuellement (en bleu), à partir d'un fichier YOLO .txt."""
    img = image.copy()
    h, w = img.shape[:2]

    if not label_path.exists():
        cv2.putText(img, "Pas de label trouvé", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return img

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

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 5)

    return img


def main():
    model = YOLO(WEIGHTS)
    images_dir = Path(IMAGES_DIR)
    labels_dir = Path(LABELS_DIR)

    image_paths = sorted(
        [p for p in images_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    )

    if not image_paths:
        print(f"Aucune image trouvée dans {images_dir}")
        return

    results = model.predict(source=str(images_dir), conf=CONF, imgsz=IMGSZ, verbose=False)

    for image_path, result in zip(image_paths, results):
        image = cv2.imread(str(image_path))

        img = draw_predicted_box(image, result)
        img = draw_ground_truth_box(img, labels_dir / f"{image_path.stem}.txt")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.figure(figsize=(10, 6))
        plt.imshow(img_rgb)
        plt.title("Box prédite en bleue et attendue en rouge")
        plt.axis("off")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()