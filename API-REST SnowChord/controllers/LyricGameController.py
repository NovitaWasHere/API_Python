import bcrypt
from bson import json_util
from flask import request, jsonify
from bson.objectid import ObjectId

from models.LyricGame import LyricGame


class LyricGameController:
    def __init__(self, db):
        self.db = db

    def get_lyricGames(self):
        try:
            # Acceder a la conexión y colección MongoDB
            collectio = self.db['LyricGame']

            lyrics = []
            for post in collectio.find():
                post['_id'] = json_util.dumps(post['_id'])
                lyrics.append(post)

            print(lyrics)
            if lyrics:
                return jsonify({'exito': True, 'datos': lyrics})
            else:
                return jsonify({'exito': False, 'error': 'lyrics no encontradas'}), 404

        except Exception as e:
            print(f"Error en LyricGameController.get_lyricGames: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500


    def get_lyricGame(self, _id):
        try:
            collectio = self.db['LyricGame']

            lyric = collectio.find_one({'_id': ObjectId(_id)})

            if lyric:
                lyric['_id'] = str(lyric['_id'])
                lyric['cancion'] = str(lyric['cancion'])
                lyric['acordes'] = [str(acorde_id) for acorde_id in lyric['acordes']]
                return jsonify({'exito': True, 'datos': lyric})
            else:
                return jsonify({'exito': False, 'error': 'lyric no encontrado'}), 404

        except Exception as e:
            print(f"Error en LyricGameController.get_lyricGame: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def post_lyricGame(self):
        try:
            collectio = self.db['LyricGame']

            data = request.json
            lyrics = data.get('lyrics')
            acordes = data.get('acordes')
            velocidad = data.get('velocidad')
            cancion = data.get('velocidad')

            if not (lyrics and acordes and velocidad):
                return jsonify({'exito': False, 'error': 'Faltan campos obligatorios'}), 400

            nuevo_lg = LyricGame(
                lyrics=lyrics,
                acordes=acordes,
                velocidad=velocidad,
                cancion=cancion
            )

            new_lG = nuevo_lg.to_mongo()

            lg = collectio.insert_one(new_lG)

            return jsonify({'exito': True, '_id': str(lg.inserted_id)}), 201

        except Exception as e:
            print(f"Error en LyricGameController.post_lyricGame: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def put_lyricGame(self,_id):

        try:
            collectio = self.db['LyricGame']
            data = request.json
            lyrics = data.get('lyrics')
            acordes = data.get('acordes')
            velocidad = data.get('velocidad')

            update_fields = {}
            if lyrics is not None:
                update_fields['lyrics'] = lyrics
            if acordes is not None:
                update_fields['acordes'] = acordes
            if velocidad is not None:
                update_fields['velocidad'] = velocidad

            result = collectio.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})
            if result.modified_count:
                return jsonify({'exito': True, 'mensaje': 'lyric actualizado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'lyric no encontrada' + str(result)}), 404

        except Exception as e:
            print(f"Error en LyricGameController.put_lyricGame: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def delete_lyricGame(self,_id):

        try:
            collectio = self.db['LyricGame']

            result = collectio.delete_one({'_id': ObjectId(_id)})
            if result.deleted_count:
                return jsonify({'exito': True, 'mensaje': 'lyric eliminada correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'lyric no encontrada'}), 404

        except Exception as e:
            print(f"Error en LyricGameController.delete_lyricGame: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500
