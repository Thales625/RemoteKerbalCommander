import grpc
import cam_pb2
from cam_pb2_grpc import CameraStreamStub

from Camera import Camera

ADDRESS = 'localhost'
PORT = 5077

def debug(text:str):
    print(f"CameraConn > {text}")

class CameraConn:
    def __init__(self) -> None:
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
            exit()

        self.cameras = [Camera(id, self.stub.GetCameraTexture, cam_pb2.GetCameraTextureRequest) for id in cameras_id]

if __name__ == '__main__':
    CameraConn()