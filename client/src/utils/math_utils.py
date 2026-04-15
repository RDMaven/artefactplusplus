from config import Config
import math

class Ratio:
    TperM = Config.Robot.TICKS_PER_CM 
    MperT = 1 / TperM


# Positions --------------------------------------------- #
class Position:

    def __init__(self, x0=0, y0=0, theta0=0):
        self.x = x0
        self.y = y0
        self.theta = theta0
        
        self.theta_rad = math.radians(self.theta) # TOUJOURS UPDATE CECI QUAND ON UPDATE THETA.

    def updateForLinearMovement(self, real_tick_distance: int):
        real_meter_distance = real_tick_distance * Ratio.MperT

        offset_x = real_meter_distance * math.cos(self.theta_rad)
        offset_y = real_meter_distance * math.sin(self.theta_rad)
        
        self.y += round(offset_y, 2)
        self.x += round(offset_x, 2)

    def updateForTankRotation(self, real_tick_angle_left: int, real_tick_angle_right: int):
        var_angle_rad = abs(real_tick_angle_right - real_tick_angle_left) * Ratio.MperT / Config.Robot.DISTANCE_BTW_WHEELS

        self.theta_rad += var_angle_rad
        self.theta += round(math.degrees(var_angle_rad), 3)


def distanceInTickForForward(distance: float):
    """ distance : in cm """
    return int(distance * Ratio.TperM)

def distanceInTickForRotation(angle: float):
    """ angle : in degrees """
    return int(1/2 * abs(math.radians(angle) * Config.Robot.DISTANCE_BTW_WHEELS * Ratio.TperM))



# Numbers ----------------------------------------------- #
def avg(*args):
    return sum(args)/len(args)

def normaliser_degrees(degrees):
    """
    Replacer une mesure en degré dans -180,180,
    avec des exceptions.
    """
    excluded = [360, 1080]
    if degrees not in excluded:
        degrees = (degrees + 180) % 360 - 180
    return degrees

    