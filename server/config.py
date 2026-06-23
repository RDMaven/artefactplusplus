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
        DATA_DIRECTORY = ROOT+str(environ["DATA_DIRECTORY"])
        MAPS_DIRECTORY = ROOT+str(environ["MAPS_DIRECTORY"])
    # Working environment type (dev or prod)
    ENV = environ["APP_ENV"]  # test ou prod
    is_prod = ENV == "prod"

    # TODO Ranger ces env.
    OS_IS_LINUX=any([e in platform for e in ['linux']])
    print(f"Detected OS : {platform}.")
    
    class Web:
        PORT=int(environ["WEB_PORT"])
        HOST=(environ["WEB_HOST"])

    class Camera:
        ID = int(environ["CAMERA_ID"]) # TODO enlever, ceci est pour tester.
        CAPTURE = False

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


# compare_env_with_example()

print("+--+ Config SETUP (END) +--+")
