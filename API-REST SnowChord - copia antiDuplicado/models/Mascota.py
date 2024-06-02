from dataclasses import dataclass

from mongoengine import Document, StringField, ListField, IntField


@dataclass()
class Mascota(Document):
    snowi= StringField(required=True)
    imgSnowi = StringField(required=True)
    imgIcono = StringField(required=True)
    precio = IntField(required=True)

    def __init__(self,snowi,imgSnowi,imgIcono,precio,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snowi = snowi
        self.imgSnowi = imgSnowi
        self.imgIcono = imgIcono
        self.precio = precio

    def to_dict(self):
        return {
            "snowi": self.snowi,
            "imgSnowi": self.imgSnowi,
            "imgIcono": self.imgIcono,
            "precio": self.precio
        }

    meta = {'collection': 'mascota'}