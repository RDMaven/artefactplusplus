# Ultrasonic ranging module

#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import threading

from config import Config


class SingleUltrasonicSensor:

    def __init__(self, TRIG=11, ECHO=12):
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


MODE_SENSOR = (Config.Robot.MODE == "auto")

class UltrasonicSensors:
    def __init__(self):
        self.time_interval = 0.3

        self.SensorFront = SingleUltrasonicSensor(TRIG=11, ECHO=12)
        self.SensorBack  = SingleUltrasonicSensor(TRIG=15, ECHO=16)
        self.front_distance = None
        self.back_distance  = None

        self.obstacle_in_front = False
        self.obstacle_behind = False

        self._thread = None

    def loop(self, verbose=False):

        while Config.Robot.MODE == "auto":
            self.front_distance = self.SensorFront.distance()
            self.back_distance = self.SensorBack.distance()

            self.obstacle_in_front = (self.front_distance < Config.Sensors.OBSTACLE_DANGER_DISTANCE)
            self.obstacle_behind = (self.back_distance < Config.Sensors.OBSTACLE_DANGER_DISTANCE)

            if verbose:
                print(f"Ultrasonic Front sensor : {round(self.front_distance, 1)}cm")
                print(f"Ultrasonic Back sensor  : {round(self.back_distance, 1)}cm")

            time.sleep(self.time_interval)

        # Cleanup when done
        self.SensorFront.destroy()
        self.SensorBack.destroy()

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


if __name__ == "__main__":
    sensors = UltrasonicSensors()
    sensors.loop(verbose = True)


