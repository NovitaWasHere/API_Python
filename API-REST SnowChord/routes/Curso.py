import os

from dotenv import load_dotenv
from flask import Blueprint
from pymongo import MongoClient
from controllers.CursoController import CursoController

load_dotenv()
client = MongoClient(os.getenv("MONGO_DB"))
db = client['TFG']

curso = CursoController(db)


# Creamos un Blueprint para definir las rutas modulares
rutasCursos = Blueprint('rutasCursos', __name__)

# Establecemos los endpoints de cada solicitud
rutasCursos.add_url_rule('/all', 'get_cursos', curso.get_cursos)
rutasCursos.add_url_rule('/esp/<_id>', 'get_curso', curso.get_curso)
rutasCursos.add_url_rule('/agregar', 'post_curso',curso.post_curso, methods=['POST'])
rutasCursos.add_url_rule('/<_id>', 'put_curso', curso.put_curso, methods=['PUT'])
rutasCursos.add_url_rule('/<_id>', 'delete_curso', curso.delete_curso, methods=['DELETE'])
