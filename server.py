from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from time import time

from KSPConn import KSPConnection
from CameraConn import CameraConnection
from ConnManager import ConnectionManager

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

    conn_manager.emit_setup()

    debug(f"Client connected: {request.sid}")


def broadcast_values():
    debug("Values broadcast started!")
    while True:
        conn_manager.emit_values()

        socket_io.sleep(0.1)


def broadcast_ping():
    debug("Ping broadcast started!")
    while True:
        socket_io.emit("pong", f"{time():.2f}")

        socket_io.sleep(2)


@socket_io.on("pong")
def handle_ping(time_0):
    emit("ping", f"{((time()-float(time_0))*1000):.2f}")

@socket_io.on("disconnect")
def handle_disconnect():
    clients.remove(request.sid)
    
    debug(f"Client disconnected: {request.sid}")


if __name__ == "__main__":
    debug("Starting...")
    socket_io.start_background_task(broadcast_ping)

    cam_conn = CameraConnection()
    ksp_conn = KSPConnection()

    conn_manager = ConnectionManager(socket_io.emit, ksp_conn, cam_conn)

    socket_io.start_background_task(broadcast_values)

    debug("Running")

    socket_io.run(app, host="0.0.0.0", port=8765)
