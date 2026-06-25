#! /usr/bin/env python3
import time
import threading

from config import Config
from src.robot.controller import WifiBot, Reference, ReferenceSimple
from src.sensors.ultrasonic_sensors import UltrasonicSensors
import src.utils.math_utils as mu
from ws_queue import messages

if Config.is_prod:
    from src.sensors.kalmanFilter.kalman_for_odometry import Kalman


class RobotDriver(WifiBot):

    def __init__(self, serPath = Config.Robot.SERIAL_PORT):
        if Config.is_prod:
            super().__init__(serPath)
            self.relative_ticks = Reference(self.getOdom(is_setup=True)) # Voir 'controller.py/Reference'

    
        self.position = mu.Position(x0=0, y0=0, theta0=0)

        self._outputing_position = False
        self._thread_position = None

        if Config.is_prod:
            self.kalman = Kalman()

        self.speed = Config.Robot.SPEED
        self.timeout = Config.Robot.CLOCK # TODO modifier au besoin

        self.sensors = UltrasonicSensors()

        if Config.Robot.MODE == "auto":
            self.sensors.start()

        self.current_objective = 0 # POUR LES MODES AUTO

    def KALODO(self, x_kalman, y_kalman, theta_kalman):
        x_odo, y_odo, theta_odo = self.position.get()

    def updatePositionLinear(self, ref):
        self.updateOdomReference(ref)
        self.position.updateForLinearMovement(mu.avg(ref.l, ref.r))
        self.kalman.kalman_one_turn()


    def updatePositionTankRotation(self, ref):
        self.updateOdomReference(ref)
        # self.position.updateForTankRotation(ref.l, ref.r)
        self.kalman.kalman_one_turn()
        # print(self.kalman.get_theta())
        self.position.updateForTankRotationForceKalman(self.kalman.get_theta())


####################################

    def _print_position_loop(self):
        f = open('positions.txt', 'a')
        while self._outputing_position:
            tstr = f'{self.position.__str__():50} | {self.kalman.__str__():50}'
            print(tstr)
            f.write(tstr+'\n')
            time.sleep(self.timeout)
        f.close()

    def start_printing_position(self):
        if self._thread_position is None or not self._thread_position.is_alive():
            self._outputing_position = True
            self._thread_position = threading.Thread(
                target=self._print_position_loop,
                daemon=True
            )
            self._thread_position.start()

    def stop_printing_position(self):
        self._outputing_position = False

######################################

    def setLocalParameter(self, parameter_name, new_value):
        match parameter_name:
            case "mode":
                assert new_value in ['auto', 'manual'], f"Asked to set to an unknown mode : {new_mode}"
                Config.Robot.MODE = new_value
                if new_value == "auto":
                    self.sensors.start()

            case "speed":
                assert type(new_value) == int and new_value > 0, f"Bad new speed given ({new_value}). Expected strictly positive int" 
                self.speed = new_value

            case "position":
                assert type(new_value) == list and len(new_value) == 3, f"Bad values for position : {new_value}"
                x,y,t = new_value
                self.position.set(x,y,t)
                
            case _:
                raise KeyError(f"Unknown parameter name : {parameter_name}")
        print(f"Updated config : ({parameter_name} : {new_value})")


    def setMovingSpeed(self, l:int = Config.Robot.SPEED, r:int = Config.Robot.SPEED, reverse = False):
        if not Config.is_prod:
            print(f"setMovingSpeed (test): sLF={l>=0}, sRF={r>=0}, sLS={abs(l)}, sRS={abs(r)}")
            return
        if reverse:
            l = -l
            r = -r

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
        l = -l
        r = -r

        # Scale
        l *= self.speed
        r *= self.speed

        if l == 0.0 and r == 0.0:
            self.stop()
        else:
            self.setMovingSpeed(round(l,1), round(r,1))
    
    
    # Pour le mode AUTO --------------------------------- #
    def forwardByDistance(self, distance:float, is_local_instr: bool = True, speed = Config.Robot.SPEED):
        """ Avance d'une certaine distance, donnée en cm. 
        is_local_instr : si vrai, on ne met pas a jour l'objectif global. """

        # Init the odometry : the robot need to be in movement to get the odometry.
        ref = ReferenceSimple(self.getOdom(is_setup=True))
        
        if is_local_instr:
            distance_in_ticks = (mu.distanceInTickForForward(distance))
            self.start_printing_position()

            self.setMovingSpeed(reverse=(distance < 0)) # Pas le choix, on l'a monté à l'envers

            while ref.is_less_than(abs(distance_in_ticks)):
                time.sleep(self.timeout)
                self.updatePositionLinear(ref)
                # print(f"l={ref.accl}, r={ref.accr} : {distance_in_ticks}")

            # Stop the movement, and record overshoot
            self.stopMoving()
            for _ in range(int(1.5 / self.timeout)):
                time.sleep(self.timeout)
                self.updatePositionLinear(ref)

            # print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")

            overL, overR =  ref.accl - distance_in_ticks, ref.accr - distance_in_ticks
            over = round(mu.avg(overL, overR) / Config.Robot.TICKS_PER_CM,2)

            # time.sleep(self.timeout)
            # self.updatePositionLinear(ref)

            print(f'DRIVER - Forward(d={distance}cm ({distance_in_ticks}t)). Went {over+distance}cm. Over by {over}cm ({mu.avg(overL, overR)}t).')

            self.stop_printing_position()
            self.printStatus()
        
        else: ## Mode appelé seulement par la méthode 'goto'

            # On connait deja l'objectif, pas besoin de calculer distance_in_ticks
            self.start_printing_position()

            # Récupérer le signe initial de current objective : lorsqu'on change de signe, on a dépassé l'objectif.
            current_objective_was_positive =  (self.current_objective >= 0)

            def changed_sign(v_was_positive, v_new):
                """ Condition d'arret pour la boucle : si obj change de sens ou si obj = 0 """
                return (v_was_positive ^ (v_new >= 0)) or v_new == 0

            self.setMovingSpeed(reverse=(self.current_objective < 0), l=speed, r=speed) # Pas le choix, on l'a monté à l'envers

            while not self.sensors.obstacle_in_front and not changed_sign(current_objective_was_positive, self.current_objective):
                time.sleep(self.timeout)
                self.updatePositionLinear(ref) # self.updatePositionLinear(self.relative_ticks)
                step = mu.avg(ref.l, ref.r) # ON CHOISI DE PRENDRE LA MOYENNE
                self.current_objective -= step
                # print(ref.l, ref.r, step, self.current_objective)

            # Stop the movement, dans tous les cas
            self.stopMoving()
            for _ in range(int(1.5 / self.timeout)):
                time.sleep(self.timeout)
                self.updatePositionLinear(ref)
                self.current_objective -= mu.avg(ref.l, ref.r)
                
            # Gestion de l'overshoot
            # self.current_objective -= mu.avg(ref.l, ref.r)


            self.stop_printing_position()

            if self.sensors.obstacle_in_front:
                print(f"DRIVER - GOTO_Forward OBSTACLE stopped me at r={self.current_objective / Config.Robot.TICKS_PER_CM} from objective.")
            else:
                print(f'DRIVER - GOTO_Forward DONE (L\'objectif est à {round(self.current_objective / Config.Robot.TICKS_PER_CM,2)}cm).')
                self.printStatus()


    def rotateByAngle(self, angle:float):
        """ Tourne d'un certain angle, donné en degrés. """
        angle = mu.normaliser_degrees(angle)

        # Init the odometry : the robot need to be in movement to get the odometry.
        ref = ReferenceSimple(self.getOdom(is_setup=True))
        distance_in_ticks = mu.distanceInTickForRotation(angle)
        pre_theta = self.position.theta

        self.start_printing_position()

        dir = -1 if angle < 0 else 1 # A ajuster
        self.setMovingSpeed((-dir) * Config.Robot.SPEED, dir * Config.Robot.SPEED)
        print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")
        while ref.is_less_than(distance_in_ticks):
            time.sleep(self.timeout)
            self.updatePositionTankRotation(ref)
            # print(f"l={ref.l}, r={ref.r} : {distance_in_ticks}")

        # Stop the movement, and record overshoot
        self.stopMoving()
        # time.sleep(1)
        for _ in range(int(1.5 / self.timeout)):
            time.sleep(self.timeout)
            self.updatePositionTankRotation(ref)


        # self.updateOdomReference(ref)
        overL, overR =  (ref.accl) - (distance_in_ticks), (ref.accr) - (distance_in_ticks)
        over = mu.angleFromTicks(overL, overR) #mu.avg(overL, overR) / Config.Robot.TICKS_PER_CM

        # self.position.updateForTankRotation(ref.l, ref.r)

        # print(
        #   f'forwardByDistance() : theta={angle}° ({distance_in_ticks}t),\n\
        #     effectif : {mu.angleFromTicks(ref.accl, ref.accr)} (accl={ref.accl}, accr={ref.accr}) \n\
        #     over={over}° (l={overL}, r={overR})'
        # )

        self.position.updateForTankRotationEndOfMvt(pre_theta, ref.accl, ref.accr, self.kalman.get_theta())
        time.sleep(self.timeout)
        # TODO : comparer avec kalman

        print(f"DRIVER - Rotate : Demande={angle}° ({distance_in_ticks}t) | total_l={ref.accl} total_r={ref.accr}, TOTAL={mu.angleFromTicks(ref.accl, ref.accr)}")
        # with open("valeurs.txt", 'a') as f:
        #     f.write(f"DRIVER - Rotate : Demande={angle}° ({distance_in_ticks}t) | total_l={ref.accl} total_r={ref.accr}\n")

        self.stop_printing_position()
        self.printStatus()


    def avoidObstacle(self):
        """ Évitement d'obstacles pour l'avant. """
        angles = [45, -45, -90, 90, 180]
        correction_distance = Config.Robot.OBSTACLE_AVOIDANCE_DISTANCE # Arbitraire, TODO le mettre en variable d'environment, et prendre plus petit que la distance minimale des capteurs !

        # On test de tourner à des angles successifs pour voir si ça débloque le robot.
        for i in range(len(angles)):
            if i == 0:
                self.rotateByAngle(angles[i])
            else:
                self.rotateByAngle(-angles[i-1]+angles[i]) # Calcul du nouvel angle effectif pour le robot : on "annule" l'angle précédent pour repartir de 0

            if not self.sensors.obstacle_in_front:
                self.forwardByDistance(correction_distance)
                return correction_distance, angles[i]

        raise Exception("Robot.avoidObstacle() : Je suis bloqué...")


    def goto(self, r0, theta0):
        """ Aller à un objectif donné en radial, tout en évitant les potentiels obstacles. """
        r, theta = r0, theta0
        print("DRIVER - Starting goto")
        self.current_objective = mu.distanceInTickForForward(r)
        if theta:
            self.rotateByAngle(theta)
        self.forwardByDistance(r, is_local_instr=False)
        temp_divided_speed = Config.Robot.SPEED

        while abs(self.current_objective/Config.Robot.TICKS_PER_CM) > 10: # Tolérence de 10cm autour de l'objectif
            if self.sensors.obstacle_in_front:
                d, alpha = self.avoidObstacle()
                r, theta = mu.calculate_new_polar(r, alpha, d)
                self.current_objective = mu.distanceInTickForForward(r)
                self.rotateByAngle(theta)
                self.forwardByDistance(0, is_local_instr=False) # r n'est pas requis dans ce cas, on ne regarde que current_objective
            else:
                temp_divided_speed //= 2
                self.forwardByDistance(0, is_local_instr=False, speed=temp_divided_speed)

    def goto_cartesian(self, x2, y2):
        """ Aller à une position, donnée en cartésien. """
        x1,y1, theta1 = self.position.get()
        r, theta = mu.convert_cartesian_to_radial(x1,y1,theta1,x2,y2)
        print(f"DRIVER - Goto cartésien ({x1,y1} -> {(x2,y2)}) a calculé r={r}, theta={theta}")
        self.goto(r, theta)
        messages.append({"ack": "goto"})



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

