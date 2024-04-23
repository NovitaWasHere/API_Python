from typing import Union
import bcrypt
from bson import json_util
from flask import request, jsonify, Response
from bson.objectid import ObjectId
from pymongo import MongoClient


class UserController:
    def __init__(self, db):
        self.db = db

    def get_usuarios(self):
        try:
            # Acceder a la conexión y colección MongoDB
            collectio = self.db['Users']

            users = []
            for post in collectio.find():
                post['_id'] = json_util.dumps(post['_id'])
                users.append(post)

            print(users)
            # Verificar si hay usuarios y devolver una respuesta adecuada
            if users:
                return jsonify({'exito': True, 'datos': users})
            else:
                return jsonify({'exito': False, 'error': 'Usuarios no encontrado'}), 404

        except Exception as e:
            print(f"Error en UserController.get_usuarios: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500


    def get_usuario(self, _id):
        try:
            # Acceder a la conexión y colección MongoDB
            collectio = self.db['Users']

            usuario = collectio.find_one({'_id': ObjectId(_id)})

            if usuario:
                usuario['_id'] = str(usuario['_id'])
                return jsonify({'exito': True, 'datos': usuario})
            else:
                return jsonify({'exito': False, 'error': 'Usuarios no encontrado'}), 404

        except Exception as e:
            print(f"Error en UserController.get_usuarios: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def post_usuario(self):
        try:
            collectio = self.db['Users']

            data = request.json
            nombre = data.get('nombre')
            apellidos = data.get('apellidos')
            correo = data.get('correo')
            contra = data.get('contra')

            if not (nombre and apellidos and correo and contra):
                return jsonify({'exito': False, 'error': 'Faltan campos obligatorios'}), 400

            hash_contra = bcrypt.hashpw(contra.encode(), bcrypt.gensalt()).decode()

            nuevo_usuario = {
                'nombre': nombre,
                'apellidos': apellidos,
                'correo': correo,
                'contra': hash_contra,
                'instrumentos': []
            }

            # Insertar el nuevo usuario en la colección
            usuario = collectio.insert_one(nuevo_usuario)

            # Obtener el _id del usuario insertado
            id_usuario = usuario.inserted_id

            # Devolver la respuesta con el _id del nuevo usuario
            return jsonify({'exito': True, '_id': str(id_usuario)})

        except Exception as e:
            print(f"Error en UserController.post_usuario: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def put_usuario(self,_id):

        try:
            collectio = self.db['Users']
            data = request.json
            nombre = data.get('nombre')
            apellidos = data.get('apellidos')
            correo = data.get('correo')
            contra = data.get('contra')

            # Verificaciones de atributos nulos
            update_fields = {}
            if nombre is not None:
                update_fields['nombre'] = nombre
            if apellidos is not None:
                update_fields['apellidos'] = apellidos
            if correo is not None:
                update_fields['correo'] = correo
            if contra is not None:
                hash_contra = bcrypt.hashpw(contra.encode(), bcrypt.gensalt()).decode()
                update_fields['contra'] = hash_contra

            result = collectio.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})
            if result.modified_count:
                return jsonify({'exito': True, 'mensaje': 'Usuario actualizado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Usuario no encontrado' + str(result)}), 404

        except Exception as e:
            print(f"Error en UserController.post_usuario: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def delete_usuario(self,_id):

        try:
            collectio = self.db['Users']

            result = collectio.delete_one({'_id': ObjectId(_id)})
            if result.deleted_count:
                return jsonify({'exito': True, 'mensaje': 'Usuario eliminado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Usuario no encontrado'}), 404

        except Exception as e:
            print(f"Error en UserController.post_usuario: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500


#    def auth_usuario(self):
#       data = request.json
#       correo = data.get('correo')
#       contra = data.get('contra')

#       usuario = db.Usuario.find_one({'correo': correo})
#       if usuario and bcrypt.checkpw(contra.encode(), usuario['contra']):
#           return jsonify({'exito': True, 'datos': usuario})
#       else:
#           return jsonify({'exito': False, 'error': 'Credenciales inválidas'}), 401