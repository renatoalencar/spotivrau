import io
from PIL import Image

class Thumb:
    size = (120, 120)

    def __init__(self, image):
        self.image = Image.open(image)

    def get_thumb(self):
        fp = io.BytesIO()

        new_image = self.image.resize(self.size)
        new_image.save(fp, 'png')
        fp.seek(0)

        return fp
