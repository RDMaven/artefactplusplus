from src.robot.driver import RobotDriver
from src.camera.camera import CameraMove
from src.robot.kalodo import Kalodo

# ======================================================= #
# STARTUP =============================================== #
# ======================================================= #
robot = RobotDriver()
camera = CameraMove()
kalodo = Kalodo()

# camera.demo(1)

# DEBUG ================================================= #
#robot.runInteractive()
#robot.setMovingSpeed(100, -100)
# robot.forwardByDistance(10)
