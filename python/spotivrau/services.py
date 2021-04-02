import uuid

from .lib.service import ServiceError

from .models import SongStatus


class EnqueueTranscodeService:
    def __init__(self, storage, song_class, queue):
        self.storage = storage
        self.song_class = song_class
        self.queue = queue

    def transcode(self, name, file):
        id = str(uuid.uuid4())

        if not self.storage.valid_type(file):
            raise ServiceError('Invalid file')

        original_song_path = self.storage.upload(id, file)

        song = self.song_class(
            id=id,
            name=name,
            original_song_path=original_song_path
        ).save()

        self.queue.enqueue('transcode', {'id': id})

        song.status = SongStatus.QUEDED
        song.save()

        return song


class TranscodeService:
    format = 'ogg'
    waveform_format = 'png'

    def __init__(self, song, storage, transcoder):
        self.song = song
        self.storage = storage
        self.transcoder = transcoder

    def transcode(self):
        self.song.song_path = self.storage.store(
            self.transcoder.transcode(self.format),
            str(self.song.id) + '.' + self.format
        )
        self.song.waveform_path = self.storage.store(
            self.transcoder.waveform(),
            str(self.song.id) + '.waveform.' + self.waveform_format
        )
        self.song.metadata = self.transcoder.metadata()
        self.song.status = SongStatus.DONE

        self.song.save()
