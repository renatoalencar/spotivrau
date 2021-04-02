import json
from spotivrau.models import Song, SongStatus


def test_transcode(client):
    song = Song(
        id='6e499cbb-dc2d-4423-b2e7-1ff568409add',
        name='C\'est Cuit',
        original_song_path='/tmp/6e499cbb-dc2d-4423-b2e7-1ff568409add.wav',
        song_path='/tmp/6e499cbb-dc2d-4423-b2e7-1ff568409add.ogg',
        waveform_path='/tmp/6e499cbb-dc2d-4423-b2e7-1ff568409add.waveform.png',
    ).save()

    response = client.get('/songs/6e499cbb-dc2d-4423-b2e7-1ff568409add')

    data = json.loads(response.data)

    assert data['id'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add'
    assert data['name'] == 'C\'est Cuit'
    assert data['original_song'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add.wav'
    assert data['song'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add.ogg'
    assert data['waveform'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add.waveform.png'
