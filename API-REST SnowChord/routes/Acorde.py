# routes/LyricGame.py
import os
from dotenv import load_dotenv
from flask import Blueprint
from pymongo import MongoClient
from controllers.AcordeController import AcordeController

# Cargar variables de entorno
load_dotenv()
client = MongoClient(os.getenv("MONGO_DB"))
db = client['TFG']

# Inicializamos el controlador
acorde_controller = AcordeController(db)

# Creamos un Blueprint para definir las rutas modulares
rutasAcordes = Blueprint('rutasAcordes', __name__)

# Establecemos los endpoints de cada solicitud
rutasAcordes.add_url_rule('/all', 'get_acordes', acorde_controller.get_acordes)
rutasAcordes.add_url_rule('/esp/<_id>', 'get_acorde', acorde_controller.get_acorde)
rutasAcordes.add_url_rule('/agregar', 'post_acorde', acorde_controller.post_acorde, methods=['POST'])
rutasAcordes.add_url_rule('/<_id>', 'put_acorde', acorde_controller.put_acorde, methods=['PUT'])
rutasAcordes.add_url_rule('/<_id>', 'delete_acorde', acorde_controller.delete_acorde, methods=['DELETE'])
