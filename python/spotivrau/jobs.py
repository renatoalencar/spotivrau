from .lib.storage import FileStorage

from .app import queue, worker
from .models import Song
from .transcoder import Transcoder


@worker.job('transcode')
def transcode(data):
    song = Song.objects.get(id=data['id'])

    print(f'Processing song - {song.name}')

    storage = FileStorage(queue.app)
    transcoder = Transcoder(open(song.original_song_path, 'rb'))

    song.song_path = storage.store(
        transcoder.transcode('ogg'),
        song.id + '.ogg'
    )
    song.waveform_path = storage.store(
        transcoder.waveform(),
        song.id + '.waveform.png'
    )
    song.metadata = transcoder.metadata()

    song.save()
