import enum

import mongoengine as db


class SongStatus(enum.Enum):
    IDLE = 'idle'
    QUEDED = 'queued'
    DONE = 'done'
    ERROR = 'error'


class Song(db.Document):
    id = db.UUIDField(primary_key=True)
    name = db.StringField()

    song_path = db.StringField()
    waveform_path = db.StringField()
    original_song_path = db.StringField()

    metadata = db.DynamicField()

    status = db.EnumField(SongStatus, default=SongStatus.IDLE)
