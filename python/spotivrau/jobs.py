from spotivrau import queue
from .models import Song
from .worker import Worker

from .transcoder import Transcoder
from .storage import FileStorage

worker = Worker(queue)

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
