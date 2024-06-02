from bson import json_util
from flask import request, jsonify
from bson.objectid import ObjectId
from models.Curso import Curso


class CursoController:
    def __init__(self, db):
        self.db = db

    def get_cursos(self):
        try:
            # Acceder a la conexión y colección MongoDB
            collectio = self.db['Curso']

            cursos = []
            for post in collectio.find():
                post['_id'] = json_util.dumps(post['_id'])
                cursos.append(post)

            print(cursos)
            if cursos:
                return jsonify({'exito': True, 'datos': cursos})
            else:
                return jsonify({'exito': False, 'error': 'Cursos no encontrados'}), 404

        except Exception as e:
            print(f"Error en CursoController.get_cursos: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def get_curso(self, _id):
        try:
            collectio = self.db['Curso']

            curso = collectio.find_one({'_id': ObjectId(_id)})

            if curso:
                curso['_id'] = str(curso['_id'])
                return jsonify({'exito': True, 'datos': curso})
            else:
                return jsonify({'exito': False, 'error': 'Curso no encontrado'}), 404

        except Exception as e:
            print(f"Error en CursoController.get_curso: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def post_curso(self):
        try:
            collectio = self.db['Curso']

            data = request.json
            nombrePractica = data.get('nombrePractica')
            nombreGuia = data.get('nombreGuia')
            parte = data.get('parte')
            orientacion = data.get('orientacion')
            aprendizaje = data.get('aprendizaje')
            conocimientos = data.get('conocimientos')
            teoria = data.get('teoria')
            imgTeoria = data.get('imgTeoria')
            cuerpo = data.get('cuerpo')
            imgCuerpo = data.get('imgCuerpo')

            if not (nombrePractica and nombreGuia and parte and orientacion and aprendizaje and conocimientos and teoria and imgTeoria and cuerpo and imgCuerpo):
                return jsonify({'exito': False, 'error': 'Faltan campos obligatorios'}), 400

            nuevo_curso = Curso(
                nombrePractica=nombrePractica,
                nombreGuia=nombreGuia,
                parte=parte,
                orientacion=orientacion,
                aprendizaje=aprendizaje,
                conocimientos=conocimientos,
                teoria=teoria,
                imgTeoria=imgTeoria,
                cuerpo=cuerpo,
                imgCuerpo=imgCuerpo
            )

            new_curso = nuevo_curso.to_mongo()

            curso = collectio.insert_one(new_curso)

            return jsonify({'exito': True, '_id': str(curso.inserted_id)}), 201

        except Exception as e:
            print(f"Error en CursoController.post_curso: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def put_curso(self, _id):

        try:
            collectio = self.db['Curso']
            data = request.json
            update_fields = {}

            fields = ['nombrePractica', 'nombreGuia', 'parte', 'orientacion', 'aprendizaje', 'conocimientos', 'teoria', 'imgTeoria', 'cuerpo', 'imgCuerpo']
            for field in fields:
                if field in data:
                    update_fields[field] = data[field]

            result = collectio.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})
            if result.modified_count:
                return jsonify({'exito': True, 'mensaje': 'Curso actualizado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Curso no encontrado o no actualizado'}), 404

        except Exception as e:
            print(f"Error en CursoController.put_curso: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def delete_curso(self, _id):

        try:
            collectio = self.db['Curso']

            result = collectio.delete_one({'_id': ObjectId(_id)})
            if result.deleted_count:
                return jsonify({'exito': True, 'mensaje': 'Curso eliminado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Curso no encontrado'}), 404

        except Exception as e:
            print(f"Error en CursoController.delete_curso: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500
