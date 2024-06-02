import os
from dotenv import load_dotenv
from flask import Blueprint
from pymongo import MongoClient
from controllers.MascotaController import MascotaController

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Conexión a MongoDB utilizando la URL de conexión desde las variables de entorno
client = MongoClient(os.getenv("MONGO_DB"))
db = client['TFG']

# Instanciamos el controlador de Mascota con la base de datos
mascota = MascotaController(db)

# Creamos el Blueprint para las rutas de Mascotas
rutasMascotas = Blueprint('rutasMascotas', __name__)

# Establecemos los endpoints de cada solicitud
rutasMascotas.add_url_rule('/all', 'get_Mascotas', mascota.get_mascotas)
rutasMascotas.add_url_rule('/esp/<_id>', 'get_Mascota', mascota.get_mascota)
rutasMascotas.add_url_rule('/agregar', 'post_Mascota', mascota.post_mascota, methods=['POST'])
rutasMascotas.add_url_rule('/<_id>', 'put_Mascota', mascota.put_mascota, methods=['PUT'])
