from spotivrau.models import Song, SongStatus


def test_single_song(client):
    song = Song(
        id='6e499cbb-dc2d-4423-b2e7-1ff568409add',
        name='C\'est Cuit',
        artist='Major Lazer',
        original_song_path='/tmp/6e499cbb-dc2d-4423-b2e7-1ff568409add.wav',
        song_path='/tmp/6e499cbb-dc2d-4423-b2e7-1ff568409add.ogg',
        waveform_path='/tmp/6e499cbb-dc2d-4423-b2e7-1ff568409add.waveform.png',
        cover_thumb_path='/tmp/6e499cbb-dc2d-4423-b2e7-1ff568409add.cover.thumb.png',
        status=SongStatus.DONE,
        metadata={
            "format": {
                "filename": "/tmp/tmplf2cm5xj",
                "nb_streams": 1,
                "nb_programs": 0,
                "format_name": "wav",
                "format_long_name": "WAV / WAVE (Waveform Audio)",
                "duration": "249.026667",
                "size": "43928350",
                "bit_rate": "1411201",
                "probe_score": 99
            }
        }
    ).save()

    data = client.get('/songs/6e499cbb-dc2d-4423-b2e7-1ff568409add').get_json()

    assert data['id'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add'
    assert data['name'] == 'C\'est Cuit'
    assert data['artist'] == 'Major Lazer'
    assert data['original_song'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add.wav'
    assert data['song'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add.ogg'
    assert data['waveform'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add.waveform.png'
    assert data['cover'] == '6e499cbb-dc2d-4423-b2e7-1ff568409add.cover.thumb.png'
    assert data['duration'] == 249
    assert data['status'] == 'done'


def test_songs(client):
    song = Song(
        id='e30eba9a-5095-4717-8b3a-8828315a5b94',
        name='March To The Sea',
        original_song_path='/tmp/e30eba9a-5095-4717-8b3a-8828315a5b94.wav',
        song_path='/tmp/e30eba9a-5095-4717-8b3a-8828315a5b94.ogg',
        waveform_path='/tmp/e30eba9a-5095-4717-8b3a-8828315a5b94.waveform.png',
        status=SongStatus.DONE
    ).save()

    data = client.get('/songs').get_json()

    assert len(data['songs']) > 0
