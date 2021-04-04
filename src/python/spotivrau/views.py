import os

from flask import request
from .lib.storage import FileStorage
from .lib.service import service_error_serialize

from .app import app, queue
from .models import Song, SongStatus
from .services import EnqueueTranscodeService
from .thumb import Thumb


@app.route('/transcode', methods=['POST'])
@service_error_serialize
def index():
    service = EnqueueTranscodeService(FileStorage(app), Song, Thumb, queue)
    song = service.transcode(
        request.form['name'],
        request.files.get('file', None),
        request.files.get('cover', None)
    )

    return { 'id': str(song.id) }


def serialize_song(song):
    serialized_song = {
        'id': song.id,
        'name': song.name,
        'original_song': os.path.basename(song.original_song_path),
        'status': song.status.value
    }

    if song.status == SongStatus.DONE:
        serialized_song['song'] = os.path.basename(song.song_path)
        serialized_song['waveform'] = os.path.basename(song.waveform_path)

        if song.cover_thumb_path is not None:
            serialized_song['cover'] = os.path.basename(song.cover_thumb_path)

        if song.metadata is not None:
            serialized_song['duration'] = int(
                float(song.metadata['format']['duration'])
            )

    return serialized_song


@app.route('/songs')
def songs():
    songs = Song.objects.all()

    return {
        'songs': list(map(serialize_song, songs))
    }


@app.route('/songs/<string:song_id>')
def song(song_id):
    song = Song.objects.get(id=song_id)

    return serialize_song(song)
