from dataclasses import dataclass
from enum import Enum
from mongoengine import Document, StringField, IntField, ObjectIdField


@dataclass()
class Instrumento(Enum):
    guitarra = 1
    piano = 2


class Cancion(Document):
    nombre = StringField(required=True)
    artista = StringField(required=True)
    instrumento = StringField(choices=[i.value for i in Instrumento])
    tiempo = IntField(required=True)
    dificultad = IntField(required=True)
    genero = StringField(required=True)
    imgCancion = StringField(required=True)
    lyrics = ObjectIdField(required=True)
    reproducciones = IntField(required=True)

    meta = {'collection': 'canciones', 'allow_inheritance': True}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = kwargs.get('nombre', self.nombre)
        self.artista = kwargs.get('artista', self.artista)
        self.instrumento = kwargs.get('instrumento', self.instrumento)
        self.tiempo = kwargs.get('tiempo', self.tiempo)
        self.dificultad = kwargs.get('dificultad', self.dificultad)
        self.genero = kwargs.get('genero', self.genero)
        self.imgCancion = kwargs.get('imgCancion', self.imgCancion)
        self.lyrics = kwargs.get('lyrics', self.lyrics)
        self.reproducciones = kwargs.get('reproducciones', self.reproducciones)

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'artista': self.artista,
            'instrumento': self.instrumento,
            'tiempo': self.tiempo,
            'dificultad': self.dificultad,
            'genero': self.genero,
            'imgCancion': self.imgCancion,
            'lyrics': self.lyrics,
            'reproducciones': self.reproducciones
        }
