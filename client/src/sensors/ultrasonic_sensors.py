# Ultrasonic ranging module

import time
import threading
from config import Config

if Config.is_prod:
    import RPi.GPIO as GPIO

    class SingleUltrasonicSensor:

        def __init__(self, TRIG=11, ECHO=12):
            # GPIO.cleanup()
            self.TRIG = TRIG
            self.ECHO = ECHO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.TRIG, GPIO.OUT)
            GPIO.setup(self.ECHO, GPIO.IN)

        def distance(self):
            GPIO.output(self.TRIG, 0)
            time.sleep(0.000002)

            GPIO.output(self.TRIG, 1)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, 0)

            while GPIO.input(self.ECHO) == 0:
                a = 0
            time1 = time.time()
            while GPIO.input(self.ECHO) == 1:
                a = 1
            time2 = time.time()

            during = time2 - time1
            return during * 340 / 2 * 100

        def destroy(self):
            GPIO.cleanup()

else:
    class SingleUltrasonicSensor:
        def __init__(self, TRIG=11, ECHO=12):
            self.TRIG = TRIG
            self.ECHO = ECHO

        def distance(self):
            time.sleep(0.000002)

            time.sleep(0.00001)
            return 42

        def destroy(self):
            pass


MODE_SENSOR = (Config.Robot.MODE == "auto")

class UltrasonicSensors:
    def __init__(self):
        self.time_interval = 0.3

        self.SensorRight = SingleUltrasonicSensor(TRIG=11, ECHO=12)
        self.SensorLeft  = SingleUltrasonicSensor(TRIG=15, ECHO=16)
        self.left_distance = None
        self.rignt_distance = None

        self.obstacle_in_front = False

        self._thread = None

    def loop(self, verbose=False):

        while Config.Robot.MODE == "auto":
            self.right_distance = self.SensorRight.distance()
            self.left_distance = self.SensorLeft.distance()

            self.obstacle_in_front = (self.left_distance < Config.Sensors.OBSTACLE_DANGER_DISTANCE and \
                                        self.right_distance < Config.Sensors.OBSTACLE_DANGER_DISTANCE)

            if verbose:
                print(f"ULTRASONIC - L={round(self.left_distance, 1)}cm, R={round(self.right_distance, 1)}cm, Obstacle={self.obstacle_in_front}")

            time.sleep(self.time_interval)

        # Cleanup when done
        self.SensorLeft.destroy()
        self.SensorRight.destroy()

    def start(self, verbose=False):

        # Si mode auto + pas de thread deja en cours pour les capteurs
        if Config.Robot.MODE == "auto" and (self._thread is None or not self._thread.is_alive()):
            self._thread = threading.Thread(
                target=self.loop,
                args=(verbose,),
                daemon=True
            )
            self._thread.start()

    def stop(self):
        if self._thread is not None:
            self._thread.join()
        self.SensorLeft.destroy()
        self.SensorRight.destroy()


if __name__ == "__main__":
    sensors = UltrasonicSensors()
    sensors.loop(verbose = True)


