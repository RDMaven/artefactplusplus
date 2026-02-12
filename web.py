import image as im
from flask import Flask, Response, send_from_directory
from ENV import Env

app = Flask(__name__,static_folder = Env.static_directory, static_url_path="/")

@app.route('/video')
def video():
    print(type(Env.id_camera))
    return Response(im.capture_video(Env.id_camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return send_from_directory(Env.static_directory,'index.html')