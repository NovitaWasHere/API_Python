from typing import List
from datetime import datetime
from mongoengine import Document, StringField

class Usuario(Document):
    nombre = StringField(required=True)
    apellidos = StringField(required=True)
    correo = StringField(required=True)
    contra = StringField(required=True)


    meta = {'collection': 'usuarios'}
