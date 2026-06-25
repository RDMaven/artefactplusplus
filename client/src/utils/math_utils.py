from config import Config
import math

class Ratio:
    """ Definition des ratios Ticks - CM """
    TperM = Config.Robot.TICKS_PER_CM 
    MperT = 1 / TperM

class RegressionRot:
    A = 18.43
    B = 145

    def getTicks(angle):
        assert angle > 40, "Angle trop petit"
        return RegressionRot.A*angle+RegressionRot.B

    def getAngle(ticks):
        return round((ticks-RegressionRot.B)/RegressionRot.A,2)

# ======================================================= #
# Gestion de la position, mises à jour par odométrie ==== #
# ======================================================= #

class Position:

    def __init__(self, x0=0.0, y0=0.0, theta0=0.0):
        self.x = x0
        self.y = y0
        self.theta = theta0
        
        self.theta_rad = math.radians(self.theta) # TOUJOURS UPDATE CECI QUAND ON UPDATE THETA.

    def get(self):
        return self.x, self.y, self.theta

    def set(self, x, y, theta):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
    
    def __str__(self):
        return f"Odometry position : x={self.x}, y={self.y}, theta={self.theta}°"


    def updateForLinearMovement(self, real_tick_distance: int):
        real_meter_distance = real_tick_distance * Ratio.MperT

        offset_x = real_meter_distance * math.cos(self.theta_rad)
        offset_y = real_meter_distance * math.sin(self.theta_rad)
        
        self.y = round(self.y + offset_y, 2)
        self.x = round(self.x + offset_x, 2)

    def updateForTankRotation(self, real_tick_angle_left: int, real_tick_angle_right: int):
        # var_angle_rad = abs(real_tick_angle_right - real_tick_angle_left) * Ratio.MperT / Config.Robot.DISTANCE_BTW_WHEELS
        # la formules est fause : TODO
        var_angle_deg = angleFromTicks(real_tick_angle_left, real_tick_angle_right)
        if real_tick_angle_left < 0:
            var_angle_deg = -var_angle_deg

        self.theta_rad += math.radians(var_angle_deg)
        self.theta = round(self.theta + var_angle_deg, 3)

    def updateForTankRotationEndOfMvt(self, pre_theta, total_ticks_l, total_ticks_r, theta_kalman):
        # var_angle_rad = abs(real_tick_angle_right - real_tick_angle_left) * Ratio.MperT / Config.Robot.DISTANCE_BTW_WHEELS
        # la formules est fause : TODO
        var_angle_deg = angleFromTicks(total_ticks_l, total_ticks_r)
        if total_ticks_l < 0:
            var_angle_deg = -var_angle_deg

        average = avg(var_angle_deg, theta_kalman)

        self.theta_rad = math.radians(pre_theta+average)
        self.theta = round(pre_theta + average, 3)

    def updateForTankRotationForceKalman(theta):
        self.theta = theta
        self.theta_rad = math.radians(theta)

# ======================================================= #
# Conversion en ticks de cm et angles =================== #
# ======================================================= #

def distanceInTickForForward(distance: float):
    """ distance : in cm """
    return int(distance * Ratio.TperM)

def distanceInTickForRotation(angle: float):
    """ angle : in degrees """
    # return int(1/2 * abs(math.radians(angle) * Config.Robot.DISTANCE_BTW_WHEELS * Ratio.TperM))
    # return int(math.pi*Config.Robot.DISTANCE_BTW_WHEELS*(angle/360)*Ratio.TperM)
    if abs(angle) >= 40:
        return RegressionRot.getTicks(abs(angle)) # TODO changer le abs pour gérer
    else:
        return int(math.pi*Config.Robot.DISTANCE_BTW_WHEELS*(angle/360)*Ratio.TperM)


def angleFromTicks(tl, tr):
    # return (tr-tl)*180/(math.pi*Config.Robot.DISTANCE_BTW_WHEELS*Ratio.TperM)
    return RegressionRot.getAngle(avg(abs(tl), abs(tr)))

# ======================================================= #
# Fonctions maths diverses ============================== #
# ======================================================= #

def avg(*args):
    return sum(args)/len(args)

def normaliser_degrees(degrees):
    """ Replacer une mesure en degré dans -180,180, avec des exceptions. """
    excluded = [360, 1080]
    if degrees not in excluded:
        degrees = (degrees + 180) % 360 - 180
    return degrees

def calculate_new_polar(r0, alpha, d):
    """ Voici l'énoncé que cette fonction résout :
    Soit, A, B et O. On note r0 = AO, d = AB, OAB = alpha.
    Déterminer r = BO et theta = ABO.
    Utile pour recalculer les paramètre de mouvement après avoir évité un obstacle.
    """
    alpha_rad = math.radians(alpha)

    cosalpha = math.cos(alpha_rad)

    r2 = r0**2 + d**2 - 2*r0*d*cosalpha
    r = math.sqrt(r2)

    theta = math.degrees(math.asin( (math.sqrt((r2 - (r*cosalpha)**2)))/r ))
    theta = round(theta, 2)

    return r, theta

def convert_cartesian_to_radial(x1,y1,theta1, x2,y2):
    """ Obtenir (r,theta) pour aller du point (x1,y1,theta1) à (x2,y2). """
    dx = x2 - x1
    dy = y2 - y1

    # Distance
    r = math.hypot(dx, dy)

    # Angle
    theta_target_deg = math.degrees(math.atan2(dy, dx))
    theta2 = theta_target_deg - theta1
    theta2 = (theta2 + 180) % 360 - 180

    return r, theta2


