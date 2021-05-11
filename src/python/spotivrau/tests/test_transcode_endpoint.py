import magic

from spotivrau.models import Song, SongStatus
from .utils import file_fixture, uploaded_media_path


def transcode_song(client, **data):
    return client.post(
        '/transcode',
        data=data,
        content_type='multipart/form-data'
    )

def test_transcode(client):
    response = transcode_song(
        client,
        name='Lost European',
        artist='Images',
        file=file_fixture('Images - Lost European.wav'),
        cover=file_fixture('420.jpg'),
    )

    data = response.get_json()

    id = data['id']
    song_path = uploaded_media_path(client, id + '.wav')
    cover_path = uploaded_media_path(client, id + '.cover.jpg')
    cover_thumb_path = uploaded_media_path(client, id + '.cover.thumb.png')

    song = Song.objects.get(id=id)

    assert response.status_code == 200

    # Should have persisted the raw file
    assert magic.from_file(song_path, mime=True) == 'audio/x-wav'

    # Should have generated thumbnail
    assert magic.from_file(cover_thumb_path, mime=True) == 'image/png'

    # Should have enqueued a transcode message
    assert client.application.queue._pop_has('transcode', {'id': id})

    # Should have persisted the song in the database
    assert song is not None
    assert song.original_song_path == song_path
    assert song.name == 'Lost European'
    assert song.status == SongStatus.QUEDED
    assert song.cover_path == cover_path
    assert song.cover_thumb_path == cover_thumb_path
    assert song.artist == 'Images'


def test_invalid_file(client):
    response = transcode_song(
        client,
        name='Lost European',
        file=file_fixture('Invalid file.txt'),
    )

    data = response.get_json()
    message = data['message']

    assert response.status_code == 400
    assert message == 'Invalid file'
