from flask import Flask, render_template

STATIC_DIR = "./"
REMOTE_ROBOT_CONTROL_SERVER="http://localhost:8081" # À compléter, avec l'url vers le serveur de controles des robots (ex: "http://137.194.194.180:8081")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/", template_folder=STATIC_DIR)

@app.route("/")
def index():
    return render_template(STATIC_DIR+"index.html", robot_control_server=REMOTE_ROBOT_CONTROL_SERVER)

if __name__ == "__main__":
    app.run(debug=True, port=8082) # S'assurer que rien ne tourne déjà sur le port 8082 ! (ex: lsof -i :8082)
