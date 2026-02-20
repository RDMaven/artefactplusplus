from dotenv import load_dotenv, find_dotenv,dotenv_values
from os import environ
from sys import platform


print("+--+ Config SETUP +--+")
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
    OS_IS_WIN=not any([e in platform for e in ['linux', 'darwin']])
    print(f"Detected OS : {platform} (OS_IS_WIN={OS_IS_WIN})")
    
    class Web:
        PORT=int(environ["WEB_PORT"])



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

        

def compare_env_with_example():
    # Import env files
    env = dict(dotenv_values(".env"))
    env_ex = dict(dotenv_values(".env.example"))

    # 
    changed=0
    for k,v in env.items():
        if v == "":
            print(f'ERROR : Key {k} has no value in .env.')

    for k,v in env_ex.items():
        if k not in env:
            changed+=1
            print(f"Missing environment variable : {k}. Replacing by default value.")
            with open('.env', 'a') as f:
                f.write(f'\n\n#Copied from .env.example.\n{k}={v}')
    if changed:
        print(f"Added {changed} variables to .env.")

    print("Loaded .env")


compare_env_with_example()

print("+--+ Config SETUP (END) +--+")
