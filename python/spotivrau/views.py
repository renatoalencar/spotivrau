from flask import request
from .lib.storage import FileStorage
from .lib.service import service_error_serialize

from .app import app, queue
from .models import Song
from .services import EnqueueTranscodeService


@app.route('/transcode', methods=['POST'])
@service_error_serialize
def index():
    service = EnqueueTranscodeService(FileStorage(app), Song, queue)
    song = service.transcode(request.form['name'], request.files['file'])

    return { 'id': str(song.id) }
