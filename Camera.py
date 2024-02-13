from PIL import Image
from io import BytesIO


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
