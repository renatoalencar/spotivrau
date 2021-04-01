import mongoengine as db


class Song(db.Document):
    id = db.StringField(primary_key=True)
    name = db.StringField()
    original_song_path = db.StringField()
