import json

from bson import json_util
from flask import request, jsonify
from bson.objectid import ObjectId
from models.Acorde import Acorde


class AcordeController:
    def __init__(self, db):
        self.db = db

    def get_acordes(self):
        try:
            # Acceder a la conexión y colección MongoDB
            collectio = self.db['Acordes']

            lyrics = []
            for post in collectio.find():
                post['_id'] = json_util.dumps(post['_id'])
                post['_id'] = json.loads(post['_id'])['$oid']
                lyrics.append(post)

            if lyrics:
                return jsonify({'exito': True, 'datos': lyrics})
            else:
                return jsonify({'exito': False, 'error': 'lyrics no encontradas'}), 404

        except Exception as e:
            print(f"Error en AcordeController.get_acordes: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500


    def get_acorde(self, _id):
        try:
            collectio = self.db['Acordes']

            lyric = collectio.find_one({'_id': ObjectId(_id)})

            if lyric:
                lyric['_id'] = str(lyric['_id'])
                return jsonify({'exito': True, 'datos': lyric})
            else:
                return jsonify({'exito': False, 'error': 'lyric no encontrado'}), 404

        except Exception as e:
            print(f"Error en AcordeController.get_acorde: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def post_acorde(self):
        try:
            collectio = self.db['Acordes']

            data = request.json
            nombre = data.get('nombre')
            acorde = data.get('acorde')
            imgAcorde = data.get('velocidad')

            if not (nombre and acorde and imgAcorde):
                return jsonify({'exito': False, 'error': 'Faltan campos obligatorios'}), 400

            nuevo_lg = Acorde(
                nombre=nombre,
                acorde=acorde,
                imgAcorde=imgAcorde
            )

            new_lG = nuevo_lg.to_mongo()

            lg = collectio.insert_one(new_lG)

            return jsonify({'exito': True, '_id': str(lg.inserted_id)}), 201

        except Exception as e:
            print(f"Error en AcordeController.post_acorde: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def put_acorde(self,_id):

        try:
            collectio = self.db['Acordes']
            data = request.json
            nombre = data.get('nombre')
            acorde = data.get('acorde')
            imgAcorde = data.get('velocidad')

            update_fields = {}
            if nombre is not None:
                update_fields['nombre'] = nombre
            if acorde is not None:
                update_fields['acorde'] = acorde
            if imgAcorde is not None:
                update_fields['imgAcorde'] = imgAcorde

            result = collectio.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})
            if result.modified_count:
                return jsonify({'exito': True, 'mensaje': 'lyric actualizado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'lyric no encontrada' + str(result)}), 404

        except Exception as e:
            print(f"Error en AcordeController.put_acorde: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def delete_acorde(self,_id):

        try:
            collectio = self.db['Acordes']

            result = collectio.delete_one({'_id': ObjectId(_id)})
            if result.deleted_count:
                return jsonify({'exito': True, 'mensaje': 'lyric eliminada correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'lyric no encontrada'}), 404

        except Exception as e:
            print(f"Error en AcordeController.delete_acorde: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500
