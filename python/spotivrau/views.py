from flask import request

from .app import app, queue
from .models import Song
from .storage import FileStorage
from .service import service_error_serialize
from .services import TranscodeService

@app.route('/transcode', methods=['POST'])
@service_error_serialize
def index():
    service = TranscodeService(FileStorage(app), Song, queue)
    song = service.transcode(request.form['name'], request.files['file'])

    return { 'id': song.id }
