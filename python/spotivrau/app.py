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

        original_song_path = self.storage.upload(id, file)

        song = self.song_class(
            id=id,
            name=name,
            original_song_path=original_song_path
        ).save()

        self.queue.enqueue('transcode', {'id': id})

        return song


@app.route('/transcode', methods=['POST'])
@service_error_serialize
def index():
    service = TranscodeService(FileStorage(app), Song, queue)
    song = service.transcode(request.form['name'], request.files['file'])

    return {'id': song.id}


def setup_app():
    import mongoengine
    import redis

    import spotivrau.commands

    app.config['UPLOAD_FOLDER'] = '/tmp'
    app.config['MONGO_CONNECTION_URI'] = 'mongodb://root:spotivrau@localhost/spotivrau?authSource=admin'
    app.config['REDIS_CONNECTION_URI'] = 'redis://localhost/0'

    mongoengine.connect(host=app.config['MONGO_CONNECTION_URI'])
    redis_connection = redis.Redis.from_url(app.config['REDIS_CONNECTION_URI'])

    app.queue.set_connection(redis_connection)

    return app
