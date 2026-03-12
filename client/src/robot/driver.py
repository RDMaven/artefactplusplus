#! /usr/bin/env python3
from threading import Thread
from time import sleep

from config import Config
# if Config.is_prod:
from src.robot.controller import WifiBot



class RobotDriver(WifiBot):
    """ WifiBot methods :
    setLeftSpeed   | setRightSpeed 
    setLeftForward | setRightForward 
    sendCmd 
    updateStatus 
    printStatus 
    runSendCmd 
    runUpdateStatus 
    runInteractive
    """
    def __init__(self, serPath):
        if Config.is_prod:
            super().__init__(serPath)
        self.local_config = {
            "mode": "manual",
            "speed": Config.Robot.SPEED,
            }

    def setLocalParameter(self, parameter_name, new_value):
        # ASSERT
        match parameter_name:
            case "mode":
                assert new_value in ['auto', 'manual'], f"Asked to set to an unknown mode : {new_mode}"
            case "speed":
                assert type(new_value) == int and new_value > 0, f"Bad new speed given ({new_value}). Expected strictly positive int" 
            case _:
                raise KeyError(f"Unknown parameter name : {parameter_name}")
        self.local_config[parameter_name] = new_value
        print(f"Updated config : {self.local_config}")

    def setSpeed(self, l:int, r:int):
        if not Config.is_prod:
            print(f"setSpeed : sLF={l>=0}, sRF={r>=0}, sLS={abs(l)}, sRS={abs(r)}")
            return
        self.setLeftForward( (l >= 0)) # Update the wheel directions
        self.setRightForward((r >= 0)) # //
        self.setLeftSpeed( abs(l)) # Set the speeds
        self.setRightSpeed(abs(r)) # //

    def moveManual(self, x:float ,y:float ):
        assert x >= -1 and x <= 1 and y >= -1 and y <= 1, "moveManual : a recu un x ou y hors de [-1,1]"
        
        # Différentiel
        left = y - (x * Config.Robot.TURN_FACTOR)
        right = y + (x * Config.Robot.TURN_FACTOR)

        # Normaliser : ex, fwd+right => left = 1 + (+0.5) = 1.5 ~> = 1        
        norm = max(1, abs(left), abs(right))
        left /= norm
        right /= norm

        # Scale
        left *= Config.Robot.SPEED_MANUAL
        right *= Config.Robot.SPEED_MANUAL

        self.setSpeed(round(left,1), round(right,1))




# # TODO Enlever cette instance temporaire
# robot_instance = Robot(Config.Robot.SERIAL_PORT)
# robot_instance.start()


if __name__ == "__main__":
   wb = RobotDriver(Config.Robot.SERIAL_PORT)
   wb.start()
   sleep(1)

   print("--------------------------")
   wb.printStatus()
   print("--------------------------")
   wb.runInteractive()
#    wb.setLeftSpeed(200)
#    wb.setRightSpeed(200)
#    wb.setLeftForward(True)
#    wb.setRightForward(False)
#    sleep(3)
   wb.printStatus()
   print("--------------------------")

#    wb.setLeftSpeed(40)
#    sleep(2)
#    wb.printStatus()
#    print("--------------------------")
#    wb.setRightSpeed(40)
#    sleep(2)
#    wb.printStatus()
#    print("--------------------------")
#    wb.setLeftForward(True)
#    sleep(2)
#    wb.printStatus()
#    print("--------------------------")
#    wb.setRightForward(True)
#    sleep(2)
#    wb.printStatus()
#    print("--------------------------")
   wb.stop()

