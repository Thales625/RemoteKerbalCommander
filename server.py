from flask import Flask, render_template, request
from flask_socketio import SocketIO

from KSPConn import KSPConnection
from CameraConn import CameraConn

def debug(text:str):
    print(f"Server> {text}")

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socket_io = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


clients = set()

@socket_io.on("connect")
def handle_connect():
    clients.add(request.sid)

    ksp_conn.emit_setup(socket_io.emit)

    debug(f"Client connected: {request.sid}")


def broadcast():
    while ksp_conn.connected:
        ksp_conn.emit_values(socket_io.emit)

        socket_io.sleep(0.05)


@socket_io.on("disconnect")
def handle_disconnect():
    clients.remove(request.sid)
    
    debug(f"Client disconnected: {request.sid}")


if __name__ == "__main__":
    cam_conn = CameraConn()

    ksp_conn = KSPConnection([{"id": cam.id, "get_image": cam.get_image} for cam in cam_conn.cameras])

    socket_io.start_background_task(broadcast)

    debug("Running")

    socket_io.run(app, host="0.0.0.0", port=8765)
