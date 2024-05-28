from dataclasses import dataclass

from mongoengine import Document, StringField, ListField


@dataclass()
class Curso(Document):
    nombrePractica = StringField(required=True)
    nombreGuia = StringField(required=True)
    parte = StringField(required=True)
    orientacion =StringField(required=True)
    aprendizaje = ListField(StringField(required=True))
    conocimientos = ListField(StringField(required=True))
    teoria = ListField(StringField(required=True))
    imgTeoria = StringField(required=True)
    cuerpo = ListField(StringField(required=True))
    imgCuerpo = StringField(required=True)

    def __init__(self, nombrePractica, nombreGuia, parte, orientacion, aprendizaje, conocimientos, teoria, imgTeoria,
                 cuerpo, imgCuerpo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombrePractica = nombrePractica
        self.nombreGuia = nombreGuia
        self.parte = parte
        self.orientacion = orientacion
        self.aprendizaje = aprendizaje
        self.conocimientos = conocimientos
        self.teoria = teoria
        self.imgTeoria = imgTeoria
        self.cuerpo = cuerpo
        self.imgCuerpo = imgCuerpo

    def to_dict(self):
        return {
            'nombrePractica': self.nombrePractica,
            'nombreGuia': self.nombreGuia,
            'parte': self.parte,
            'orientacion': self.orientacion,
            'aprendizaje': self.aprendizaje,
            'conocimientos': self.conocimientos,
            'teoria': self.teoria,
            'imgTeoria': self.imgTeoria,
            'cuerpo': self.cuerpo,
            'imgCuerpo': self.imgCuerpo
        }


    meta = {'collection': 'cursos'}