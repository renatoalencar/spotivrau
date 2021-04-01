from spotivrau import queue
from .models import Song
from .worker import Worker
from .transcoder import Transcoder

worker = Worker(queue)

@worker.job('transcode')
def transcode(data):
    song = Song.objects.get(id=data['id'])

    print(f'Processing song - {song.name}')

    transcoder = Transcoder(song.original_song_path)

    transcoder.transcode('/tmp/' + song.id + '.ogg')
