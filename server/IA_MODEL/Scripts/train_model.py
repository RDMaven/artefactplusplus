from ultralytics import YOLO

# import os
# import time
# import random
# import pandas as pd
# import cv2
# from tqdm.auto import tqdm
# from PIL import Image
# import shutil

model = YOLO('yolov8n.pt') 
model.train(data='dataset/data.yaml', epochs=100, imgsz=320)

