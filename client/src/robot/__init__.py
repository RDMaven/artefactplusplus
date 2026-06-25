from src.robot.driver import RobotDriver
from src.camera.camera import CameraMove
from ws_queue import messages
import random
import traceback
import src.utils.network_utils as nu

# ======================================================= #
# STARTUP =============================================== #
# ======================================================= #
ser = None
try:
    robot = RobotDriver()
    camera = CameraMove()
    try:
        ser = nu.get_port()
    except:
        traceback.print_exc()


    robot.forwardByDistance(20)
except Exception as e:
    print(e)
    traceback.print_exc()
    
finally:
    robot.sensors.stop()
    robot.stop_printing_position()
    if ser :
        ser.close()
# camera.demo(1)

# En attendant de pouvoir renvoyer le signal, celle-ci remplace.
def get_signal():
    if ser:
        messages.put({"signal": nu.get_rsrp(ser)[0]})
    else:
        messages.put({"signal": random.randint(0,100)})

# DEBUG ================================================= #
#robot.runInteractive()
#robot.setMovingSpeed(100, -100)
# robot.forwardByDistance(10)
