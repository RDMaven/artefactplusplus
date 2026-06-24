from src.robot.driver import RobotDriver
from src.camera.camera import CameraMove
from ws_queue import messages
import random
# ======================================================= #
# STARTUP =============================================== #
# ======================================================= #
robot = RobotDriver()
camera = CameraMove()

# camera.demo(1)

# En attendant de pouvoir renvoyer le signal, celle-ci remplace.
def get_signal():
    messages.append({"signal": random.randint(0,42)})

# DEBUG ================================================= #
#robot.runInteractive()
#robot.setMovingSpeed(100, -100)
# robot.forwardByDistance(10)
