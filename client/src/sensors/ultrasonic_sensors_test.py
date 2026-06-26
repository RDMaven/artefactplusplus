# Ultrasonic ranging module

import time, threading, traceback
import RPi.GPIO as GPIO


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



MODE_SENSOR = True
DANGER_DISTANCE = 20
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

        while True:
            self.right_distance = self.SensorRight.distance()
            self.left_distance = self.SensorLeft.distance()

            self.obstacle_in_front = (self.left_distance < DANGER_DISTANCE and \
                                        self.right_distance < DANGER_DISTANCE)

            if verbose:
                print(f"ULTRASONIC - L={round(self.left_distance, 1)}cm, R={round(self.right_distance, 1)}cm, Obstacle={self.obstacle_in_front}")

            time.sleep(self.time_interval)

        # Cleanup when done
        self.SensorLeft.destroy()
        self.SensorRight.destroy()

    def start(self, verbose=False):

        # Si mode auto + pas de thread deja en cours pour les capteurs
        if True and (self._thread is None or not self._thread.is_alive()):
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
    try:
        sensors.loop(verbose = True)
    except:
        traceback.print_exc()
    finally:
        GPIO.cleanup()

