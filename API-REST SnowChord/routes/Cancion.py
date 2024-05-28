import os

from dotenv import load_dotenv
from flask import Blueprint
from pymongo import MongoClient
from controllers.CancionController import CancionController

load_dotenv()
client = MongoClient(os.getenv("MONGO_DB"))
db = client['TFG']

cancion = CancionController(db)


# Creamos un Blueprint para definir las rutas modulares
rutasCanciones = Blueprint('rutasCanciones', __name__)

# Establecemos los endpoints de cada solicitud
rutasCanciones.add_url_rule('/all', 'get_canciones', cancion.get_canciones)
rutasCanciones.add_url_rule('/esp/<_id>', 'get_cancion', cancion.get_cancion)
rutasCanciones.add_url_rule('/agregar', 'post_cancion',cancion.post_cancion, methods=['POST'])
rutasCanciones.add_url_rule('/<_id>', 'put_cancion', cancion.put_cancion, methods=['PUT'])
rutasCanciones.add_url_rule('/<_id>', 'delete_cancion', cancion.delete_cancion, methods=['DELETE'])
