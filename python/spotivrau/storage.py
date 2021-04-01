import os
import magic

class FileStorage:
    def __init__(self, app):
        self.app = app

    def store(self, name, file):
        base, ext = os.path.splitext(file.filename)
        full_path = os.path.join(self.app.config['UPLOAD_FOLDER'], name + ext)

        file.save(full_path)

        return full_path

    def valid_type(self, file):
        buf = file.stream.read(2048)
        file.stream.seek(0)

        type, ext = magic.from_buffer(buf, mime=True).split('/')

        return type in ['audio', 'video']
