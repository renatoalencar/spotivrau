import magic

from spotivrau.jobs import transcode
from spotivrau.models import Song, SongStatus
from .utils import file_fixture_path

def test_transcode(current_app):
    song = Song(
        id='a11a5c4d-a01c-486c-ad5f-e37dca23e918',
        name='Lost European',
        original_song_path=file_fixture_path('Images - Lost European.wav')
    ).save()

    transcode(id=song.id)

    song = Song.objects.get(id=song.id)

    assert magic.from_file(song.song_path, mime=True) == 'audio/ogg'
    assert magic.from_file(song.waveform_path, mime=True) == 'image/png'
    assert song.metadata['format']['duration'] == '249.026667'
    assert song.status == SongStatus.DONE
