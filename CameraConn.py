import grpc
import greet_pb2
import greet_pb2_grpc

from Camera import Camera

import numpy as np
import cv2

class CameraConn:
    def __init__(self) -> None:
        self.server_address = 'localhost'
        self.server_port = 5077

        self.cameras = []

        self.channel = grpc.insecure_channel(f"{self.server_address}:{self.server_port}")
        self.stub = greet_pb2_grpc.CameraStreamStub(self.channel)
        self.connected = False

        # CHECK CONNECTION
        try:
            self.stub.GetAverageFps(greet_pb2.GetAverageFpsRequest())
        except grpc.RpcError:
            print("CamConn > Connection refused!")
            return

        self.connected = True

        self.update_cameras()
        #self.show_images()

    def update_cameras(self):
        active_cams_req = greet_pb2.GetActiveCameraIdsRequest()
        active_cams_res = self.stub.GetActiveCameraIds(active_cams_req)

        cameras_id = active_cams_res.cameras

        if len(cameras_id) <= 0:
            print("No cameras has found")
            exit()

        self.cameras = [Camera(id, greet_pb2.GetCameraTextureRequest) for id in cameras_id]

    def get_image(self, i):
        return self.cameras[i].get_image(self.stub.GetCameraTexture)
        #return [camera.get_image(self.stub.GetCameraTexture) for camera in self.cameras]
    
    def show_images(self):
        while True:
            for camera in self.cameras:
                img_bytes = camera.get_image(self.stub.GetCameraTexture)

                image_np = np.frombuffer(img_bytes, np.uint8)

                image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

                cv2.imshow(f'cam: {camera.id}', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                

if __name__ == '__main__':
    CameraConn()