from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from KSPConn import KSPConnection
from CameraConn import CameraConn

from PIL import Image
from io import BytesIO

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

    emit("setup", ksp_conn.setup_message)

    print("Client connected:", request.sid)


@socket_io.on("disconnect")
def handle_disconnect():
    clients.remove(request.sid)
    print("Client disconnected:", request.sid)


def broadcast():
    while ksp_conn.connected:
        socket_io.emit("update", ksp_conn.get_values())

        if cam_conn.connected:
            img_byte = cam_conn.get_image(0)

            image = Image.open(BytesIO(img_byte))
            image = image.resize((128, 128), Image.NEAREST)
            image = image.quantize(16)

            image_bytes = BytesIO()
            image.save(image_bytes, format="png")

            socket_io.emit("camera", image_bytes.getvalue())

        socket_io.sleep(1)



if __name__ == "__main__":
    cam_conn = CameraConn()

    ksp_conn = KSPConnection()
    
    socket_io.start_background_task(broadcast)

    print("> Running")

    socket_io.run(app, host="0.0.0.0", port=8765)
