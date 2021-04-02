import os

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


@app.route('/songs/<string:song_id>')
def song(song_id):
    song = Song.objects.get(id=song_id)

    return {
        'id': song.id,
        'name': song.name,
        'original_song': os.path.basename(song.original_song_path),
        'song': os.path.basename(song.song_path),
        'waveform': os.path.basename(song.waveform_path)
    }
