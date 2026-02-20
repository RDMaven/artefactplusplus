from flask import Flask, Response, send_from_directory, render_template

# Ajouter (salement) le dossier parent au path
import sys
sys.path.append('../src')
import src.camera.image as im
from config import Config


app = Flask(
    __name__,
    static_folder = Config.Path.STATIC_DIRECTORY, 
    static_url_path = "/",
    template_folder=Config.Path.TEMPLATES_DIRECTORY
)

@app.route('/')
def index():
    return send_from_directory('pages/','index.html')

@app.route('/<int:robot_id>/')
def robot_page(robot_id=1):
    if robot_id not in [1,2,3]: # TODO : change the condition to a check of the currently available robots (from robot services).
        return f"Asked for robot <strong>{robot_id}</strong>. That robot does not exist. The robot_id has to be between 1 and 3."
    else:
        return render_template('robot.html', robot_id = robot_id)


@app.route('/video')
def video():
    print(type(Config.ID_CAMERA))
    return Response(im.capture_video(Config.ID_CAMERA), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera')
def camera_page():
    return send_from_directory('pages/','camera.html')

