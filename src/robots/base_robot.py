#! /usr/bin/env python3
import serial
from threading import Thread
from time import sleep
from .robot_controller import WifiBot

# Ajouter (salement) le dossier parent au path
import sys
sys.path.append('../../')

from config import Config


class Robot(WifiBot):
    def __init__(self, serPath):
        super().__init__(serPath)
    
    def setSpeed(self, l:int, r:int):
        self.setLeftSpeed(l)
        self.setRightSpeed(r)

    def moveManual(self, x:float ,y:float ):
        assert(x >= -1 and x <= 1 and y >= -1 and y <= 1, "moveManual : a recu un x ou y hors de [-1,1]")
        print("LOLOLOLOLOLOLOLO")

        # # Différentiel
        # left = y - (x * Config.Motor.TURN_FACTOR)
        # right = y + (x * Config.Motor.TURN_FACTOR)

        # # Normaliser : fwd+right => left = 1 + (+0.5) = 1.5 ~> = 1        
        # norm = max(1.0, abs(left), abs(right))
        # left = round(left/norm)
        # right = round(right/norm)

        # self.setSpeed(left, right)


# TODO Enlever cette instance temporaire
robot_instance = Robot("/dev/ttyUSB0")
robot_instance.start()


if __name__ == "__main__":
   wb = Robot("/dev/ttyUSB0")
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

