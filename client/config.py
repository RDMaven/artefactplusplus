# Fichier de configuration des variables d'environment : classification, typage, vérification d'intégrité.

from dotenv import load_dotenv, find_dotenv,dotenv_values
from os import environ
from sys import platform


print("= Loading robot configuration =============================")
load_dotenv()
    
class Config:
    """ Gestionnaire organisé des variables d'environment. """

    # Working environment type (dev or prod)
    ENV = environ["APP_ENV"]  # /any/ ou prod
    is_prod = (ENV == "prod")

    OS_IS_LINUX=any([e in platform for e in ['linux']])
    print(f"Detected OS : {platform}.")
    
    class Web:
        PORT=int(environ["WEB_PORT"])
        HOST=(environ["WEB_HOST"])

    class Camera:
        ID = int(environ["CAMERA_ID"])
        FPS = int(environ["CAMERA_FPS"])

    class Robot:
        ID = int(environ["ROBOT_ID"])
        CLOCK=0.05
        SERIAL_PORT = str(environ["ROBOT_SERIAL_PORT"])
        MODE = "manual"
        WHEELS_DIAMETER = float(environ["ROBOT_WHEELS_DIAMETER"])
        DISTANCE_BTW_WHEELS = float(environ["ROBOT_DISTANCE_BTW_WHEELS"])
        SPEED = int(environ["ROBOT_SPEED"])
        # SPEED_MANUAL = int(environ["ROBOT_SPEED_MANUAL"])
        # SPEED_AUTO = int(environ["ROBOT_SPEED_AUTO"])
        TURN_FACTOR=float(environ["ROBOT_TURN_FACTOR"])
        TICKS_PER_CM=float(environ["ROBOT_TICKS_PER_CM"])
        OBSTACLE_AVOIDANCE_DISTANCE = int(environ["ROBOT_OBSTACLE_AVOIDANCE_DISTANCE"])

    class Sensors:
        OBSTACLE_DANGER_DISTANCE = int(environ["SENSORS_OBSTACLE_DANGER_DISTANCE"])


def compare_env_with_example():
    """ Compare '.env' avec '.env.example', pour vérifier l'intégralité du fichier."""
    # Import env files
    env = dict(dotenv_values(".env"))
    env_ex = dict(dotenv_values(".env.example"))

    changed=0
    for k,v in env.items():
        if v == "":
            print(f'ERROR    : Key {k} has no value in .env.')

    for k,v in env_ex.items():
        if k not in env:
            changed+=1
            print(f"MISSING  : {k}. Replacing by default value.")
            with open('.env', 'a') as f:
                f.write(f'\n{k}={v} # Copied from .env.example.\n')
    if changed:
        print(f"Added {changed} variables to .env.")


    print("Successfully loaded and verified the '.env' file.")


compare_env_with_example()

print("===========================================================")
