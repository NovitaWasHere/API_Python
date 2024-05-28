from bson import json_util
from flask import request, jsonify
from bson.objectid import ObjectId
from models.Mascota import Mascota


class MascotaController:
    def __init__(self, db):
        self.db = db

    def get_mascotas(self):
        try:
            # Acceder a la conexión y colección MongoDB
            collectio = self.db['Mascota']

            mascotas = []
            for post in collectio.find():
                post['_id'] = json_util.dumps(post['_id'])
                mascotas.append(post)

            print(mascotas)
            if mascotas:
                return jsonify({'exito': True, 'datos': mascotas})
            else:
                return jsonify({'exito': False, 'error': 'Mascotas no encontrados'}), 404

        except Exception as e:
            print(f"Error en MascotaController.mascotas: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def get_mascota(self, _id):
        try:
            collectio = self.db['Mascota']

            mascota = collectio.find_one({'_id': ObjectId(_id)})

            if mascota:
                mascota['_id'] = str(mascota['_id'])
                return jsonify({'exito': True, 'datos': mascota})
            else:
                return jsonify({'exito': False, 'error': 'Mascota no encontrado'}), 404

        except Exception as e:
            print(f"Error en MascotaController.get_mascota: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def post_mascota(self):
        try:
            collectio = self.db['Mascota']

            data = request.json
            snowi = data.get('snowi')
            imgSnowi = data.get('imgSnowi')
            imgIcono = data.get('imgIcono')
            precio = data.get('precio')


            if not (snowi and imgSnowi and imgIcono and precio):
                return jsonify({'exito': False, 'error': 'Faltan campos obligatorios'}), 400

            nueva_mascota = Mascota(
               snowi = snowi,
               imgSnowi = imgSnowi,
               imgIcono = imgIcono,
               precio = precio
            )

            new_mascota = nueva_mascota.to_mongo()

            mascota = collectio.insert_one(new_mascota)

            return jsonify({'exito': True, '_id': str(mascota.inserted_id)}), 201

        except Exception as e:
            print(f"Error en MascotaController.post_mascota: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def put_mascota(self, _id):

        try:
            collectio = self.db['Mascota']
            data = request.json
            update_fields = {}

            fields = ['snowi', 'imgSnowi', 'imgIcono', 'precio']
            for field in fields:
                if field in data:
                    update_fields[field] = data[field]

            result = collectio.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})
            if result.modified_count:
                return jsonify({'exito': True, 'mensaje': 'Mascota actualizado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Mascota no encontrado o no actualizado'}), 404

        except Exception as e:
            print(f"Error en MascotaController.put_mascota: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500
