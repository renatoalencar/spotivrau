import enum

import mongoengine as db


class Artist(db.Document):
    id = db.UUIDField(primary_key=True)
    name = db.StringField()
    picture_path = db.StringField()


class SongStatus(enum.Enum):
    IDLE = 'idle'
    QUEDED = 'queued'
    PROCESSING = 'processing'
    DONE = 'done'
    ERROR = 'error'


class Song(db.Document):
    id = db.UUIDField(primary_key=True)
    name = db.StringField()
    artist = db.StringField()

    song_path = db.StringField()
    waveform_path = db.StringField()
    original_song_path = db.StringField()

    cover_path = db.StringField()
    cover_thumb_path = db.StringField()

    metadata = db.DynamicField()

    status = db.EnumField(SongStatus, default=SongStatus.IDLE)
