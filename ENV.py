from dotenv import load_dotenv
from os import environ

load_dotenv()

class Env:
    static_directory = str(environ["static_directory"])
    id_camera = int(environ["id_camera"])