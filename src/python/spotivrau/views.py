import os

from flask import request
from .lib.storage import FileStorage
from .lib.service import service_error_serialize

from .app import app, queue
from .models import Song, SongStatus, Artist
from .services import EnqueueTranscodeService, ArtistService
from .thumb import Thumb


@app.route('/transcode', methods=['POST'])
@service_error_serialize
def index():
    service = EnqueueTranscodeService(FileStorage(app), Song, Thumb, queue)
    song = service.transcode(
        request.form.get('name'),
        request.form.get('artist'),
        request.files.get('file', None),
        request.files.get('cover', None)
    )

    return { 'id': str(song.id) }


def serialize_song(song):
    serialized_song = {
        'id': song.id,
        'name': song.name,
        'artist': song.artist,
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


def serialize_artist(artist):
    artist_dict = {
        'id': str(artist.id),
        'name': artist.name,
    }

    if artist.picture_path is not None:
        artist_dict['picture'] = os.path.basename(artist.picture_path)

    return artist_dict


@app.route('/artist', methods=['POST'])
def create_artist():
    service = ArtistService(Artist, FileStorage(app))

    artist = service.create(
        request.form.get('name'),
        request.files.get('picture')
    )

    return serialize_artist(artist)


@app.route('/artists')
def list_artists():
    artists = Artist.objects.all()

    return {
        'artists': list(map(serialize_artist, artists))
    }
