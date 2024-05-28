from dataclasses import dataclass

from mongoengine import Document, StringField, IntField, ListField, ObjectIdField


@dataclass()
class LyricGame(Document):
    lyrics = ListField(StringField(required=True))
    acordes = ListField(ObjectIdField(required=True))
    velocidad = IntField(required=True)
    cancion = ObjectIdField(required=True)

    meta = {'collection': 'lyricGame'}

    def __init__(self, lyrics, acordes, velocidad, cancion,*args, **kwargs):
        super(LyricGame, self).__init__(*args, **kwargs)
        self.lyrics = lyrics
        self.acordes = acordes
        self.velocidad = velocidad
        self.cancion = cancion

    def to_dict(self):
        return {
            'lyrics': self.lyrics,
            'acordes': self.acordes,
            'velocidad': self.velocidad,
            'cancion': self.cancion
        }