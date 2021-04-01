import uuid
from flask import Flask, request

from .models import Song
from .storage import FileStorage
from .service import ServiceError, service_error_serialize
from .queue import Queue

app = Flask(__name__)
queue = Queue(app)


class TranscodeService:
    def __init__(self, storage, song_class, queue):
        self.storage = storage
        self.song_class = song_class
        self.queue = queue

    def transcode(self, name, file):
        id = str(uuid.uuid4())

        if not self.storage.valid_type(file):
            raise ServiceError('Invalid file')

        original_song_path = self.storage.store(id, file)

        self.queue.enqueue('transcode', {'id': id})

        return self.song_class(
            id=id,
            name=name,
            original_song_path=original_song_path
        ).save()


@app.route('/transcode', methods=['POST'])
@service_error_serialize
def index():
    service = TranscodeService(FileStorage(app), Song, queue)
    song = service.transcode(request.form['name'], request.files['file'])

    return {'id': song.id}
