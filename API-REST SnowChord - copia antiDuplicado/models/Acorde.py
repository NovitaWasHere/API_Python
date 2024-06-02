from dataclasses import dataclass

from mongoengine import Document, StringField, IntField, ListField, ObjectIdField


@dataclass()
class Acorde(Document):
    nombre = StringField(required=True)
    acorde = StringField(required=True)
    imgAcorde = StringField(required=True)

    meta = {'collection': 'acordes'}

    def __init__(self, nombre, acorde, imgAcorde, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.acorde = acorde
        self.imgAcorde = imgAcorde

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "acorde": self.acorde,
            "imgAcorde": self.imgAcorde
        }
