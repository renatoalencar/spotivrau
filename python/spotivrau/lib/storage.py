import os
import magic
import shutil

class FileStorage:
    def __init__(self, app):
        self.app = app

    def full_path(self, path):
        return os.path.join(self.app.config['UPLOAD_FOLDER'], path)

    def upload(self, name, file):
        base, ext = os.path.splitext(file.filename)
        full_path = self.full_path(name + ext)

        file.save(full_path)

        return full_path

    def store(self, file, name):
        full_path = self.full_path(name)

        shutil.copyfileobj(file, open(full_path, 'wb'))

        return full_path

    def valid_type(self, file):
        buf = file.stream.read(2048)
        file.stream.seek(0)

        type, ext = magic.from_buffer(buf, mime=True).split('/')

        return type in ['audio', 'video']
