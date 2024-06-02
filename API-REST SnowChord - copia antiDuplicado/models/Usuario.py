from dataclasses import dataclass
from enum import Enum

from mongoengine import Document, StringField, DateTimeField, BooleanField, IntField, ListField, ObjectIdField


@dataclass()
class Usuario(Document):
    id = IntField(primary_key=True)
    nombre = StringField(required=True)
    correo = StringField(required=True)
    contra = StringField(required=True)
    creacionUser =DateTimeField(required=True)
    admin =BooleanField(default=False)
    noti = BooleanField(default=False)

    meta = {'collection': 'usuarios', 'allow_inheritance': True}

    def __init__(self, nombre, correo, contra, creacionUser, admin, noti, *args, **kwargs):
        super(Usuario, self).__init__(*args, **kwargs)
        self.nombre = nombre
        self.correo = correo
        self.contra = contra
        self.creacionUser = creacionUser
        self.admin = admin
        self.noti = noti


@dataclass()
class Role(Enum):
    default = 1
    editor = 2



@dataclass()
class Admin(Usuario):
    rol =  Role = Role.default


@dataclass()
class Student(Usuario):
    snows = IntField(required=True)
    nivel = IntField(required=True)
    generos = ListField(required=True)
    inventario = ListField(required=True)
    reproducidas = ListField(required=True)
    snowiSelected = ObjectIdField(required=True)
    perfectos = IntField()
    cancionesC = IntField()
    juegos = IntField()
    faciles = IntField()
    medios = IntField()
    dificiles = IntField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snows = kwargs.get('snows', self.snows)
        self.nivel = kwargs.get('nivel', self.nivel)
        self.generos = kwargs.get('generos', self.generos)
        self.inventario = kwargs.get('inventario', self.inventario)
        self.reproducidas = kwargs.get('reproducidas', self.reproducidas)
        self.snowiSelected = kwargs.get('snowiSelected', self.snowiSelected)
        self.perfectos = kwargs.get('perfectos', self.perfectos)
        self.cancionesC = kwargs.get('cancionesC', self.cancionesC)
        self.juegos = kwargs.get('juegos', self.juegos)
        self.faciles = kwargs.get('faciles', self.faciles)
        self.medios = kwargs.get('medios', self.medios)
        self.dificiles = kwargs.get('dificiles', self.dificiles)

    def to_dict(self):
        return {
            'id': str(self.id),
            'nombre': self.nombre,
            'correo': self.correo,
            'contra': self.contra,
            'creacionUser': self.creacionUser.isoformat(),
            'admin': self.admin,
            'noti': self.noti,
            'snows': self.snows,
            'nivel': self.nivel,
            'generos': self.generos,
            'inventario': str(self.inventario),
            'snowiSelected': str(self.snowiSelected),
            'reproducidas': str(self.reproducidas),
            'perfectos': self.perfectos,
            'cancionesC': self.cancionesC,
            'juegos': self.juegos,
            'faciles': self.faciles,
            'medios': self.medios,
            'dificiles': self.dificiles
        }
