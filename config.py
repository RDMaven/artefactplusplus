from dotenv import load_dotenv, find_dotenv
from os import environ

load_dotenv()

class Config:
    """
    Clean main class to manage environment variables.
    """

    # General paths
    class Path:
        ROOT = find_dotenv()[:-4] # The .env is in the root.
        STATIC_DIRECTORY = ROOT+str(environ["STATIC_DIRECTORY"])
        TEMPLATES_DIRECTORY = ROOT+str(environ["TEMPLATES_DIRECTORY"])

    # Working environment type (dev or prod)
    ENV = environ["APP_ENV"]  # test ou prod
    is_prod = ENV == "prod"

    # TODO Ranger ces env.
    ID_CAMERA = int(environ["ID_CAMERA"])


    class Robot:
        WHEELS_DIAMETER = 0
        WHEELS_DISTANCE = 0

    # class Motor:
    #     TIMEOUT = int(environ["MOTOR_TIMEOUT"])
    #     SPEED = int(environ["MOTOR_SPEED"])
    #     TURN_FACTOR = float(environ["MOTOR_TURN_FACTOR"])
    #     TO_REAL_SPEED_FACTOR = float(environ["MOTOR_TO_REAL_SPEED_FACTOR"])
    #     TICKS_PER_CM = int(environ["MOTOR_TICKS_PER_CM"])
    #     TICKS_PER_DEGREE = int(environ["MOTOR_TICKS_PER_DEGREE"])
