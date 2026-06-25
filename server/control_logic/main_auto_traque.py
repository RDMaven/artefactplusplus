from pathlib import Path

SERVER_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(SERVER_DIR))

from IA_MODEL.Scripts.Detection import detector 
from www.routes.utils.utils_video import *

last_seen_time = 0
target_position = None

while last_seen_time < 30:
    frame = FrameStore.get_frame

