from flask import Blueprint
from pymongo import MongoClient
from controllers.UserController import UserController

MONGO_URI=['mongodb+srv://novita:1234567890aBc@cluster.aoqznyg.mongodb.net/?retryWrites=true&w=majority']

client = MongoClient(MONGO_URI)
db = client['Ejemplo']

user = UserController(db)


# Creamos un Blueprint para definir las rutas modulares
rutasUsuarios = Blueprint('rutasUsuarios', __name__)

# Establecemos los endpoints de cada solicitud
rutasUsuarios.add_url_rule('/all', 'get_usuarios', user.get_usuarios)
rutasUsuarios.add_url_rule('/esp/<_id>', 'get_usuario', user.get_usuario)
rutasUsuarios.add_url_rule('/agregar', 'post_usuario',user.post_usuario, methods=['POST'])
#rutasUsuarios.add_url_rule('/auth', 'auth_usuario', user.auth_usuario, methods=['POST'])
rutasUsuarios.add_url_rule('/<_id>', 'put_usuario', user.put_usuario, methods=['PUT'])
rutasUsuarios.add_url_rule('/<_id>', 'delete_usuario', user.delete_usuario, methods=['DELETE'])
