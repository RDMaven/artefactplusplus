from flask import Flask, Response, send_from_directory, render_template
from flask_sock import Sock

# Ajouter (salement) le dossier parent au path
import sys
sys.path.append('../src')
import src.camera.image as im
from config import Config

from src.robots.base_robot import robot_instance

# sockets=[]


app = Flask(
    __name__,
    static_folder = Config.Path.STATIC_DIRECTORY, 
    static_url_path = "/",
    template_folder=Config.Path.TEMPLATES_DIRECTORY
)

sock = Sock(app)


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
    return Response(im.capture_video(Config.ID_CAMERA, Config.OS_IS_LINUX), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video/<int:robot_id>')
# def video():
#     return TODO : get frames from each robot !!!

@app.route('/camera')
def camera_page():
    return send_from_directory('pages/','camera.html')


@sock.route("/ws")
def ws(ws):
    while True:
        data = ws.receive()
        try:
            data = json.loads(data)
        except Exception as e:
            print(f"Socket error: Invalid JSON: {e}\nMessage: {data}")
            continue
        event = data.get("event")
        if event is None:
            print(f"Socket error: No event field: {data}")
            return
        if not isinstance(event, str):
            print(f"Socket error: event should be a str, received {event}\nMessage: {data}")
            continue
        
        # Move event
        if event == "move":
            x = data.get("x")
            y = data.get("y")

            if x == None or not isinstance(x, (float, int)):
                print(f"Socket error: Invalid x field\nMessage: {data}")
                continue
            if y == None or not isinstance(y, (float, int)):
                print(f"Socket error: Invalid y field\nMessage: {data}")
                continue
            robot.moveManual(float(x), float(y))

        else:
            log(f"Socket error: Unknown event {event}\nMessage: {data}")



