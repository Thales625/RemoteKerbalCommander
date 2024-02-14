import grpc
import cam_pb2
from cam_pb2_grpc import CameraStreamStub

from PIL import Image
from io import BytesIO

def debug(text:str):
    print(f"CameraConn > {text}")

ADDRESS = 'localhost'
PORT = 5077

WIDTH = 180
HEIGHT = 180
QUANTIZE = 32

class Camera:
    def __init__(self, id, stub, text_req) -> None:
        self.id = id
        self.text_req = text_req(cameraId=self.id)
        self.stub = stub

    def get_image(self):
        img_byte = self.stub(self.text_req).texture
        image = Image.open(BytesIO(img_byte))
        image = image.resize((WIDTH, HEIGHT), Image.NEAREST)
        image = image.quantize(QUANTIZE)

        image_bytes = BytesIO()
        image.save(image_bytes, format="png")

        return image_bytes.getvalue()

class CameraConnection:
    def __init__(self) -> None:
        self.on_error = lambda reason: None

        self.cameras = []

        self.channel = grpc.insecure_channel(f"{ADDRESS}:{PORT}")
        self.stub = CameraStreamStub(self.channel)
        self.connected = False

        # CHECK CONNECTION
        try:
            self.stub.GetAverageFps(cam_pb2.GetAverageFpsRequest())
        except grpc.RpcError:
            debug("Connection refused!")
            return

        self.connected = True

        self.update_cameras()

    def update_cameras(self):
        active_cams_req = cam_pb2.GetActiveCameraIdsRequest()
        active_cams_res = self.stub.GetActiveCameraIds(active_cams_req)

        cameras_id = active_cams_res.cameras

        if len(cameras_id) <= 0:
            debug("No cameras has found")

        self.cameras = [Camera(id, self.stub.GetCameraTexture, cam_pb2.GetCameraTextureRequest) for id in cameras_id]

if __name__ == '__main__':
    CameraConnection()