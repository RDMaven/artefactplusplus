
# Positions --------------------------------------------- #
class Position:
    def __init__(self, x0=0, y0=0, theta0=0):
        self.x = x0
        self.y = y0
        self.theta = theta0

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

    