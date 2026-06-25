from pathlib import Path
from www.routes.utils.message_parse_and_build import message_builder 

SERVER_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(SERVER_DIR))

from IA_MODEL.Scripts.Detection import detector 
from www.routes.utils.utils_video import *

async def traque(client_ws, x0, y0):
    last_seen_time = 0
    target_position = None
    mode = "SEARCH"

    while True:
        isVisible, image_box, theta = detector.isthereRobot()
        # TODO capteurs

        if isVisible:
            mode = "FOLLOW"

        if mode == "FOLLOW":
            await client_ws.send(message_builder("goto_radial", client_ws.id, 1, theta)) #r=1, theta
            
            # TODO capteurs de proximité (if dist else stop)

        if mode == "SEARCH":
            ité = 0
            while ité < 36:
                await client_ws.send(message_builder("goto_radial", client_ws.id, 0, 20)) #r=0, theta en deg
                isVisible, image_box, theta = detector.isthereRobot()
                if isVisible:
                    mode = "FOLLOW"
                    break
            if mode != "FOLLOW":
                print("J'ai perdu le robot ! fin de la traque...")
                return




