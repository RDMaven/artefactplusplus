from src.robot.driver import RobotDriver
from src.camera.camera import CameraMove

# ======================================================= #
# STARTUP =============================================== #
# ======================================================= #
robot = RobotDriver()
camera = CameraMove()

# camera.demo(1)

# DEBUG ================================================= #
#robot.runInteractive()
#robot.setMovingSpeed(100, -100)
# robot.forwardByDistance(10)
