import image as im
from flask import Flask, Response, send_from_directory

static_directory = "./"         #possiblement à changer

app = Flask(__name__,static_folder=static_directory, static_url_path="/")

@app.route('/video')
def video():
    return Response(im.capture_video(2), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return send_from_directory(static_directory,'index.html')