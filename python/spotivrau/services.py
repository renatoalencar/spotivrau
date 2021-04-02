import uuid

from .service import ServiceError


class TranscodeService:
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

        return song
