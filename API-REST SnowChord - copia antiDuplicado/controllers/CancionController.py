from bson import json_util
from flask import request, jsonify
from bson.objectid import ObjectId
from models.Cancion import Cancion


class CancionController:
    def __init__(self, db):
        self.db = db

    def get_canciones(self):
        try:
            # Acceder a la conexión y colección MongoDB
            collectio = self.db['Canciones']

            canciones = []
            for post in collectio.find():
                post['_id'] =  str(post['_id'])
                post['lyrics'] = str(post['lyrics'])
                canciones.append(post)

            print(canciones)

            if canciones:
                return jsonify({'exito': True, 'datos': canciones})
            else:
                return jsonify({'exito': False, 'error': 'Cursos no encontrados'}), 404

        except Exception as e:
            print(f"Error en CancionesController.get_canciones: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def get_cancion(self, _id):
        try:
            collection = self.db['Canciones']
            cancion = collection.find_one({'_id': ObjectId(_id)})

            if cancion:
                cancion['_id'] = str(cancion['_id'])
                cancion['lyrics'] = str(cancion['lyrics'])
                return jsonify({'exito': True, 'datos': cancion})
            else:
                return jsonify({'exito': False, 'error': 'Canción no encontrada'}), 404

        except Exception as e:
            print(f"Error en CancionController.get_cancion: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def post_cancion(self):
        try:
            collection = self.db['Canciones']
            data = request.json

            nueva_cancion = Cancion(
                nombre=data.get('nombre'),
                artista=data.get('artista'),
                instrumento=data.get('instrumento'),
                tiempo=data.get('tiempo'),
                dificultad=data.get('dificultad'),
                genero=data.get('genero'),
                imgCancion=data.get('imgCancion'),
                lyrics=ObjectId(data.get('lyrics')),
                reproducciones = data.get('reproducciones')
            )

            cancion_dict = nueva_cancion.to_dict()
            cancion = collection.insert_one(cancion_dict)

            return jsonify({'exito': True, '_id': str(cancion.inserted_id)})

        except Exception as e:
            print(f"Error en CancionController.post_cancion: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def put_cancion(self, _id):
        try:
            collection = self.db['Canciones']
            data = request.json

            update_fields = {}
            for key, value in data.items():
                if key in ['nombre', 'artista', 'instrumento', 'tiempo', 'dificultad', 'genero', 'imgCancion',
                           'lyrics','reproducciones']:
                    update_fields[key] = value

            result = collection.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})

            if result.modified_count:
                return jsonify({'exito': True, 'mensaje': 'Canción actualizada correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Canción no encontrada'}), 404

        except Exception as e:
            print(f"Error en CancionController.put_cancion: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def delete_cancion(self, _id):
        try:
            collection = self.db['Canciones']

            result = collection.delete_one({'_id': ObjectId(_id)})
            if result.deleted_count:
                return jsonify({'exito': True, 'mensaje': 'Canción eliminada correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Canción no encontrada'}), 404

        except Exception as e:
            print(f"Error en CancionController.delete_cancion: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500


