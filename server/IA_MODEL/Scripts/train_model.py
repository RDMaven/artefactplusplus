from ultralytics import YOLO
from pathlib import Path
import shutil

DATA = "../Dataset/data.yaml"
BASE_MODEL = "yolov8n.pt"

OUTPUT_DIR = Path("../Results")
RUNS_DIR = Path("runs/detect")

OUTPUT_DIR.mkdir(exist_ok=True)

existing = sorted(OUTPUT_DIR.glob("best_v*.pt"))

if not existing:
    version = 1
else:
    last = existing[-1].stem
    version = int(last.split("_v")[1]) + 1

final_name = OUTPUT_DIR / f"best_v{version}.pt"

model = YOLO(BASE_MODEL)

results = model.train(
    data=DATA,
    epochs=100,
    imgsz=320,
    verbose=False
)

run_dir = Path(results.save_dir)
best_pt = run_dir / "weights" / "best.pt"

shutil.copy(best_pt, final_name)

print(f"Model saved: {final_name}")

if run_dir.exists():
    shutil.rmtree(run_dir)

print("runs/ deleted cleanly")