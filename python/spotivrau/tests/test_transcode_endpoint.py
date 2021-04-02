import os
import json
import io

from spotivrau.models import Song

dirname = os.path.dirname(os.path.realpath(__file__))

def test_transcode(client):
    response = client.post(
        '/transcode',
        data={
            'name': 'Lost European',
            'file': open(
                os.path.join(dirname, 'fixtures/Images - Lost European.wav'),
                'rb'
            )
        },
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)

    id = data['id']
    song_path = os.path.join(
        client.application.config['UPLOAD_FOLDER'],
        id + '.wav'
    )
    song = Song.objects.get(id=id)

    assert response.status_code == 200

    # Should have persisted the raw file
    assert os.path.exists(song_path)

    # Should have enqueued a transcode message
    assert client.application.queue._pop_has('transcode', {'id': id})

    # Should have persisted the song in the database
    assert song is not None
    assert song.original_song_path == song_path
    assert song.name == 'Lost European'


def test_invalid_file(client):
    response = client.post(
        '/transcode',
        data={
            'name': 'Lost European',
            'file': open(
                os.path.join(dirname, 'fixtures/Invalid file.txt'),
                'rb'
            )
        },
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    message = data['message']

    assert response.status_code == 400
    assert message == 'Invalid file'
