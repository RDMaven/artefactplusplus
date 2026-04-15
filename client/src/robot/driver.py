#! /usr/bin/env python3
from threading import Thread
import time

from config import Config
from src.robot.controller import WifiBot, Reference
import src.utils.math_utils as mu


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
    
        self.position = mu.Position(x0=0, y0=0, theta0=0)
        self.speed = Config.Robot.SPEED
        self.local_config = {
            "mode": "manual",
            }

    def setLocalParameter(self, parameter_name, new_value):
        # ASSERT
        match parameter_name:
            case "mode":
                assert new_value in ['auto', 'manual'], f"Asked to set to an unknown mode : {new_mode}"
                self.local_config[parameter_name] = new_value
            case "speed":
                assert type(new_value) == int and new_value > 0, f"Bad new speed given ({new_value}). Expected strictly positive int" 
                self.speed = new_value
            case _:
                raise KeyError(f"Unknown parameter name : {parameter_name}")
        print(f"Updated config : {self.local_config}")


    def setMovingSpeed(self, l:int = Config.Robot.SPEED, r:int = Config.Robot.SPEED):
        if not Config.is_prod:
            print(f"setMovingSpeed (test): sLF={l>=0}, sRF={r>=0}, sLS={abs(l)}, sRS={abs(r)}")
            return

        self.forceStart()

        # print(f"setMovingSpeed (prod) : sLF={l>=0}, sRF={r>=0}, sLS={abs(l)}, sRS={abs(r)}")
        self.setLeftForward( (l >= 0)) # Update the wheel directions
        self.setRightForward((r >= 0)) # //
        self.setLeftSpeed( abs(l)) # Set the speeds
        self.setRightSpeed(abs(r)) # //


    def stopMoving(self):
        self.setMovingSpeed(0,0)


    # POUR LE MODE MANUEL ------------------------------- #
    def moveManual(self, l:float ,r:float ):
        assert l >= -1 and l <= 1 and r >= -1 and r <= 1, "moveManual : a recu un x ou y hors de [-1,1]"

        # Scale
        l *= self.speed
        r *= self.speed

        if l == 0.0 and r == 0.0:
            self.stop()
        else:
            self.setMovingSpeed(round(l,1), round(r,1))
    

    # OLD - TODO ENLEVER 'POUR LE MODE MANUEL' ---------- #
    def moveManualJoystick(self, x:float ,y:float ):
        assert x >= -1 and x <= 1 and y >= -1 and y <= 1, "moveManual : a recu un x ou y hors de [-1,1]"

        # Différentiel
        left = y - (x * Config.Robot.TURN_FACTOR)
        right = y + (x * Config.Robot.TURN_FACTOR)

        # Normaliser : ex, fwd+right => left = 1 + (+0.5) = 1.5 ~> = 1        
        norm = max(1, abs(left), abs(right))
        left /= norm
        right /= norm

        # Scale
        left  *= self.speed
        right *= self.speed

        if x == 0.0 and y == 0.0:
            self.stop()
        else:
            self.setMovingSpeed(round(left,1), round(right,1))


    # Pour le mode AUTO --------------------------------- #
    def forwardByDistance(self, distance:float):
        """ Avance d'une certaine distance, donnée en cm. """

        # Init the odometry : the robot need to be in movement to get the odometry.
        ref = Reference(self.getOdom(is_setup=True))
        distance_in_ticks = mu.distanceInTickForForward(distance)

        self.setMovingSpeed()
        print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")
        while ref.l < distance_in_ticks and ref.r < distance_in_ticks:
            time.sleep(0.05)
            self.updateOdomReference(ref)
            print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")

        # Stop the movement, and record overshoot
        self.stopMoving()
        time.sleep(1)

        self.updateOdomReference(ref)
        print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")

        overL, overR =  ref.l - distance_in_ticks, ref.r - distance_in_ticks
        over = mu.avg(overL, overR) / Config.Robot.TICKS_PER_CM

        print(
          f'forwardByDistance() : d={distance}cm ({distance_in_ticks}t),\n\
            over={over}cm ({mu.avg(overL, overR)})'
        )

        self.printStatus()


    def rotateByAngle(self, angle:float):
        """ Tourne d'un certain angle, donné en degrés. """
        angle = mu.normaliser_degrees(angle)

        # Init the odometry : the robot need to be in movement to get the odometry.
        ref = Reference(self.getOdom(is_setup=True))
        distance_in_ticks = mu.distanceInTickForRotation(angle)

        dir = -1 if angle < 0 else 1 # A ajuster
        self.setMovingSpeed((-dir) * Config.Robot.SPEED, dir * Config.Robot.SPEED)
        print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")
        while abs(ref.l) < distance_in_ticks and abs(ref.r) < distance_in_ticks:
            time.sleep(0.05)
            self.updateOdomReference(ref)
            print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")

        # Stop the movement, and record overshoot
        self.stopMoving()
        time.sleep(1)

        self.updateOdomReference(ref)
        overL, overR =  abs(ref.l - distance_in_ticks), abs(ref.r - distance_in_ticks)
        over = mu.avg(overL, overR) / Config.Robot.TICKS_PER_CM

        print(
          f'forwardByDistance() : theta={angle}° ({distance_in_ticks}t),\n\
            over={over}° ({mu.avg(overL, overR)})'
        )

        self.printStatus()



if __name__ == "__main__":
   wb = RobotDriver(Config.Robot.SERIAL_PORT)
   wb.start()
   sleep(1)
   print("--------------------------")
   wb.printStatus()
   print("--------------------------")
   wb.runInteractive()
   wb.printStatus()
   print("--------------------------")
   wb.stop()

