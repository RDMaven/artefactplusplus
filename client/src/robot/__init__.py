from src.robot.driver import RobotDriver
from config import Config


robot = RobotDriver(Config.Robot.SERIAL_PORT)
#robot.runInteractive()
#robot.setMovingSpeed(100, -100)
# robot.forwardByDistance(10)
from src.camera.Camera_move import Camera_move

inst = Camera_move(Config.Camera.ID)
inst.camera_up(100)
inst.reset_camera_up()
inst.camera_up(-100)
inst.reset_camera_up()