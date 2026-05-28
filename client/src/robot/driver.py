#! /usr/bin/env python3
from threading import Thread
import time

from config import Config
from src.robot.controller import WifiBot, Reference
import src.utils.math_utils as mu


class RobotDriver(WifiBot):

    def __init__(self, serPath = Config.Robot.SERIAL_PORT):
        if Config.is_prod:
            super().__init__(serPath)
            self.relative_ticks = Reference(self.getOdom(is_setup=True)) # Voir 'controller.py/Reference'

    
        self.position = mu.Position(x0=0, y0=0, theta0=0)
        self.speed = Config.Robot.SPEED
        self.local_config = {
            "mode": "manual",
            }

        self.sensors = None # Sensors() TODO
        self.current_objective = 0 # POUR LES MODES AUTO


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
    
    
    # Pour le mode AUTO --------------------------------- #
    def forwardByDistance(self, distance:float, is_local_instr: bool = True):
        """ Avance d'une certaine distance, donnée en cm. 
        is_local_instr : si vrai, on ne met pas a jour l'objectif global. """

        # Init the odometry : the robot need to be in movement to get the odometry.
        ref = Reference(self.getOdom(is_setup=True))
        if is_local_instr:
            distance_in_ticks = mu.distanceInTickForForward(distance)

            self.setMovingSpeed()
            print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")
            while ref.l < distance_in_ticks and ref.r < distance_in_ticks:
                time.sleep(0.05)
                self.updateOdomReference(ref)
                # print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")

            # Stop the movement, and record overshoot
            self.stopMoving()
            time.sleep(1)

            self.updateOdomReference(ref)
            print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")

            overL, overR =  ref.l - distance_in_ticks, ref.r - distance_in_ticks
            over = mu.avg(overL, overR) / Config.Robot.TICKS_PER_CM

            self.position.updateForLinearMovement(mu.avg(ref.l, ref.r))

            print(
            f'forwardByDistance() : d={distance}cm ({distance_in_ticks}t),\n\
                over={over}cm ({mu.avg(overL, overR)})'
            )

            self.printStatus()
        
        else: ## Mode appelé seulement par la méthode 'goto'

            self.updateOdomReference(self.relative_ticks) # S'assurer qu'on commence à 0
            self.setMovingSpeed()

            # MODIFIER LA 1e CONDITION POUR 'LES CAPTEUR NE DÉTÈCTENT PAS D'OBSTACLE' TODO
            while self.sensors and self.current_objective != 0:
                time.sleep(0.05)
                self.updateOdomReference(self.relative_ticks)
                step = mu.avg(self.relative_ticks.l, self.relative_ticks.r) # ON CHOISI DE PRENDRE LA MOYENNE
                self.current_objective -= step 
                self.position.updateForLinearMovement(step)


            # Stop the movement, dans tous les cas
            self.stopMoving()
            time.sleep(1)

            # Gestion de l'overshoot
            self.updateOdomReference(self.relative_ticks)
            self.current_objective -= mu.avg(self.relative_ticks.l, self.relative_ticks.r)


            if self.sensors:
                print(f"forwardByDistance(global): OBSTACLE stopped me at r={self.current_objective / Config.Robot.TICKS_PER_CM} from objective")
            else:
                print(f'forwardByDistance(global): DONE.')
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

        self.position.updateForTankRotation(ref.l, ref.r)

        print(
          f'forwardByDistance() : theta={angle}° ({distance_in_ticks}t),\n\
            over={over}° ({mu.avg(overL, overR)})'
        )

        self.printStatus()


    def avoidObstacle(self):
        angles = [45, -45, -90, 90, 180]
        correction_distance = 10 # Arbitraire, TODO le mettre en variable d'environment, et prendre plus petit que la distance minimale des capteurs !

        for a in angles:
            self.rotateByAngle(a) # TODO : OR ONLY ROTATE SENSORS
            if not self.sensors: # TODO : CHANGER À, SI LES CAPTEURS NE DÉTECTENT PAS D'OBSTACLE
                self.forwardByDistance(correction_distance)
                return correction_distance, a

        raise Exception("Robot.avoidObstacle() : Je suis bloqué...")


    def goto(self, r0, theta0):
        """ Aller à un objectif donné en radial, tout en évitant les potentiels obstacles. """
        r, theta = r0, theta0

        self.current_objective = mu.distanceInTickForForward(r)
        self.rotateByAngle(theta)
        self.forwardByDistance(r, is_local_instr=False)

        while self.current_objective != 0:
            d, alpha = self.avoidObstacle()
            r, theta = mu.calculate_new_polar(r, alpha, d)
            self.current_objective = mu.distanceInTickForForward(r)
            self.rotateByAngle(theta)
            self.forwardByDistance(r, is_local_instr=False)

    def goto_cartesian(x1,y1,x2,y2):
        r, theta = mu.convert_cartesian_to_radial(x1,y1,x2,y2)
        self.goto(r, theta)



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

