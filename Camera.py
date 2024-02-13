class Camera:
    def __init__(self, id, text_req) -> None:
        self.id = id
        self.text_req = text_req(cameraId=self.id)

    def get_image(self, stub):
        return stub(self.text_req).texture
