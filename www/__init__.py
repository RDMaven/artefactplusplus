from flask import Flask, Response, send_from_directory

# Ajouter (salement) le dossier parent au path
import sys
sys.path.append('../src')
import src.camera.image as im
from config import Config


app = Flask(__name__,static_folder = Config.Path.STATIC_DIRECTORY, static_url_path="/")

@app.route('/video')
def video():
    print(type(Config.ID_CAMERA))
    return Response(im.capture_video(Config.ID_CAMERA), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return send_from_directory('pages/','index.html')

@app.route('/camera')
def camera_page():
    return send_from_directory('pages/','camera.html')

