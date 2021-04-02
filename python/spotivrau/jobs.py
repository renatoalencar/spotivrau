from .lib.storage import FileStorage

from .app import queue, worker
from .models import Song
from .transcoder import Transcoder
from .services import TranscodeService


@worker.job('transcode')
def transcode(id):
    song = Song.objects.get(id=id)

    print(f'Processing song - {song.name}')

    storage = FileStorage(queue.app)
    transcoder = Transcoder(open(song.original_song_path, 'rb'))

    TranscodeService(song, storage, transcoder).transcode()
