from datetime import datetime
import re
import bcrypt
from bson import json_util
from flask import request, jsonify
from bson.objectid import ObjectId

from models.Usuario import Usuario, Student


class UserController:
    def __init__(self, db):
        self.db = db

    def get_usuarios(self):
        try:
            # Acceder a la conexión y colección MongoDB
            collectio = self.db['Users']

            users = []
            for post in collectio.find():
                post['_id'] = str(post['_id'])  # Convertir ObjectId a string

                # Convertir snowiSelected a string si existe
                if 'snowiSelected' in post:
                    post['snowiSelected'] = str(post['snowiSelected'])

                # Convertir elementos de inventario a string si existe
                if 'inventario' in post:
                    post['inventario'] = [str(item) if isinstance(item, ObjectId) else item for item in
                                          post['inventario']]

                # Convertir elementos de reproducidas a string si existe
                if 'reproducidas' in post:
                    post['reproducidas'] = [str(item) if isinstance(item, ObjectId) else item for item in
                                            post['reproducidas']]

                users.append(post)

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

            id_usuario = str(usuario['_id'])
            snowi_usuario = str(usuario['snowiSelected'])

            student = Student(
                id=id_usuario,
                nombre=usuario['nombre'],
                correo=usuario['correo'],
                contra=usuario['contra'],
                creacionUser=usuario['creacionUser'],
                admin=usuario['admin'],
                noti=usuario['noti'],
                snows=usuario['snows'],
                nivel=usuario['nivel'],
                generos=usuario['generos'],
                inventario=usuario['inventario'],
                snowiSelected=snowi_usuario,
                reproducidas=usuario['reproducidas'],
                perfectos=usuario['perfectos'],
                cancionesC=usuario['cancionesC'],
                juegos=usuario['juegos'],
                faciles=usuario['faciles'],
                medios=usuario['medios'],
                dificiles=usuario['dificiles']
            )
            usuario_dict = student.to_dict()

            if usuario:
                return jsonify({'exito': True, 'datos': usuario_dict})
            else:
                return jsonify({'exito': False, 'error': 'Usuarios no encontrado'}), 404

        except Exception as e:
            print(f"Error en UserController.get_usuario: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def post_usuario(self):
        try:
            collectio = self.db['Users']

            data = request.json
            nombre = data.get('nombre')
            correo = data.get('correo')
            contra = data.get('contra')
            noti = data.get('not')
            notificacion = False

            if not (nombre and correo and contra):
                return jsonify({'exito': False, 'Faltan campos obligatorios': str(nombre, correo, contra)}), 400

            if noti is not False:
                notificacion = True

            patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            if not re.match(patron_correo, correo):
                return jsonify({'exito': False, 'error': 'El correo electronico no es valido'}), 400

            hash_contra = bcrypt.hashpw(contra.encode(), bcrypt.gensalt()).decode()

            # Crear una instancia de Usuario
            nuevo_usuario = Usuario(
                nombre=nombre,
                correo=correo,
                contra=hash_contra,
                creacionUser=datetime.now(),
                admin=False,
                noti=notificacion
            )

            new_user = nuevo_usuario.to_mongo()

            correoA = nuevo_usuario.correo.lstrip().rstrip()

            verificacionExistente = collectio.find_one({"correo": correoA})

            if verificacionExistente is not None:
                return jsonify({'exito': False, 'error': 'El correo ya esta en uso'}), 409

            usuario = collectio.insert_one(new_user)

            nuevo_usuario_id = str(usuario.inserted_id)

            nuevo_usuario_insertado = collectio.find_one({"_id": ObjectId(nuevo_usuario_id)})

            if nuevo_usuario_insertado is not None:
                datos_usuario = {
                    'id': nuevo_usuario_id,
                    'nombre': nuevo_usuario_insertado['nombre'],
                    'correo': nuevo_usuario_insertado['correo'],
                    'creacionUser': nuevo_usuario_insertado['creacionUser'],
                    'admin': nuevo_usuario_insertado['admin'],
                    'noti': nuevo_usuario_insertado['noti']
                }

                return jsonify({'exito': True, '_id': datos_usuario})

        except Exception as e:
            print(f"Error en UserController.post_usuario: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def put_usuario(self, _id):

        try:
            collectio = self.db['Users']
            data = request.json
            nombre = data.get('nombre')
            apellidos = data.get('apellidos')
            correo = data.get('correo')
            contra = data.get('contra')
            notificacion = data.get('not')

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
            if notificacion is not None:
                update_fields['nombre'] = notificacion

            result = collectio.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})
            if result.modified_count:
                return jsonify({'exito': True, 'mensaje': 'Usuario actualizado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Usuario no encontrado' + str(result)}), 404

        except Exception as e:
            print(f"Error en UserController.put_usuario: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def delete_usuario(self, _id):

        try:
            collectio = self.db['Users']

            result = collectio.delete_one({'_id': ObjectId(_id)})
            if result.deleted_count:
                return jsonify({'exito': True, 'mensaje': 'Usuario eliminado correctamente'})
            else:
                return jsonify({'exito': False, 'error': 'Usuario no encontrado'}), 404

        except Exception as e:
            print(f"Error en UserController.delete_usuario: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def auth_usuario(self):
        try:
            data = request.json
            correo = data.get('correo')
            contra = data.get('contra')
            collectio = self.db['Users']

            usuario = collectio.find_one({'correo': correo})

            if usuario:
                if bcrypt.checkpw(contra.encode(), usuario['contra'].encode()):

                    id_usuario = str(usuario['_id'])
                    usuario_snowiSelected = str(usuario['snowiSelected'])

                    student = Student(
                        id=id_usuario,
                        nombre=usuario['nombre'],
                        correo=usuario['correo'],
                        contra=usuario['contra'],
                        creacionUser=usuario['creacionUser'],
                        admin=usuario['admin'],
                        noti=usuario['noti'],
                        snows=usuario['snows'],
                        nivel=usuario['nivel'],
                        generos=usuario['generos'],
                        inventario=usuario['inventario'],
                        snowiSelected=usuario_snowiSelected,
                        reproducidas=usuario['reproducidas'],
                        perfectos=usuario['perfectos'],
                        cancionesC=usuario['cancionesC'],
                        juegos=usuario['juegos'],
                        faciles=usuario['faciles'],
                        medios=usuario['medios'],
                        dificiles=usuario['dificiles']
                    )

                    json_student = student.to_dict()

                    return jsonify({'exito': True, 'datos': json_student}), 200
                else:
                    return jsonify({'exito': False, 'error': 'Contraseña incorrecta'}), 401
            else:
                return jsonify({'exito': False, 'error': 'Usuario no encontrado'}), 404

        except Exception as e:
            print(f"Error en UserController.auth_usuario: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def verificarCorreo(self):
        try:
            collectio = self.db['Users']
            data = request.json
            correo = data.get('correo')

            correoA = correo.lstrip().rstrip()

            verificacionExistente = collectio.find_one({"correo": correoA})

            if verificacionExistente is not None:
                return jsonify({'exito': False, 'error': 'El correo ya esta en uso'}), 409

            # Devolver la respuesta con el _id del nuevo usuario
            return jsonify({'exito': True, 'valido': 'es valido'})

        except Exception as e:
            print(f"Error en UserController.verificarCorreo: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500

    def put_Student(self, _id):
        try:
            collectio = self.db['Users']
            data = request.json
            update_fields = {}

            nombre = data.get('nombre')
            try:
                if nombre is not None and any(c.isalpha() for c in nombre) and nombre.strip():
                    update_fields['nombre'] = nombre
            except Exception as e:
                print(f"Error en UserController.put_student: {e}")
                return jsonify({'exito': False, 'error': 'Error en el nombre'}), 500
            correo = data.get('correo')
            try:
                if correo is not None and any(c.isalpha() for c in correo) and correo.strip():
                    update_fields['correo'] = correo
            except Exception as e:
                print(f"Error en UserController.put_student: {e}")
                return jsonify({'exito': False, 'error': 'Error en el email'}), 500

            contra = data.get('contra')
            try:
                if contra is not None and any(c.isalpha() for c in contra):
                    hash_contra = bcrypt.hashpw(contra.encode(), bcrypt.gensalt()).decode()
                    update_fields['contra'] = hash_contra
            except Exception as e:
                print(f"Error en UserController.put_student: {e}")
                return jsonify({'exito': False, 'error': 'Error en el contra'}), 500

            notificacion = data.get('not')
            if notificacion is not None:
                update_fields['notificacion'] = notificacion

            snows = data.get('snows')
            if snows is not None:
                update_fields['snows'] = snows

            nivel = data.get('nivel')
            if nivel is not None:
                update_fields['nivel'] = nivel

            generos = data.get('generos')
            if generos is not None:
                update_fields['generos'] = generos

            inventario = data.get('inventario')
            if inventario is not None:
                # Convertir elementos del inventario a ObjectId y añadir a la base de datos sin sobrescribir
                inventario_ids = [ObjectId(item) for item in inventario]
                existing_inventory = collectio.find_one({'_id': ObjectId(_id)}, {'inventario': 1}).get('inventario', [])
                update_fields['inventario'] = list(set(existing_inventory + inventario_ids))

            snowiSelected = data.get('snowiSelected')
            if snowiSelected is not None:
                try:
                    update_fields['snowiSelected'] = ObjectId(snowiSelected)
                except Exception as e:
                    return {"status": "error", "message": "Invalid ObjectId format"}, 400

            reproducidas = data.get('reproducidas')
            if reproducidas is not None:
                # Convertir elementos de reproducidas a ObjectId y mantener solo los 3 más recientes
                reproducidas_ids = [ObjectId(item) for item in reproducidas]
                existing_reproducidas = collectio.find_one({'_id': ObjectId(_id)}, {'reproducidas': 1}).get(
                    'reproducidas', [])

                updated_reproducidas = existing_reproducidas[:]
                for item in reproducidas_ids:
                    if item not in updated_reproducidas:
                        updated_reproducidas.append(item)

                if len(updated_reproducidas) > 3:
                    updated_reproducidas = updated_reproducidas[-3:]
                update_fields['reproducidas'] = updated_reproducidas

            perfectos = data.get('perfectos')
            if perfectos is not None:
                update_fields['perfectos'] = perfectos

            cancionesC = data.get('cancionesC')
            if cancionesC is not None:
                update_fields['cancionesC'] = cancionesC

            juegos = data.get('juegos')
            if juegos is not None:
                update_fields['juegos'] = juegos

            faciles = data.get('faciles')
            if faciles is not None:
                update_fields['faciles'] = faciles

            medios = data.get('medios')
            if medios is not None:
                update_fields['medios'] = medios

            dificiles = data.get('dificiles')
            if dificiles is not None:
                update_fields['dificiles'] = dificiles

            print(update_fields)
            print("Se ha actualizado")

            result = collectio.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})

            if result.modified_count:

                usuario = collectio.find_one({'_id': ObjectId(_id)})

                student = Student(
                    nombre=usuario.get('nombre'),
                    correo=usuario.get('correo'),
                    contra=usuario.get('contra'),
                    creacionUser=usuario.get('creacionUser', datetime.now()),
                    admin=usuario.get('admin', False),
                    noti=usuario.get('notificacion'),
                    snows=usuario.get('snows'),
                    nivel=usuario.get('nivel'),
                    generos=usuario.get('generos'),
                    inventario=usuario.get('inventario'),
                    snowiSelected=usuario.get('snowiSelected'),
                    perfectos=usuario.get('perfectos'),
                    cancionesC=usuario.get('cancionesC'),
                    juegos=usuario.get('juegos'),
                    faciles=usuario.get('faciles'),
                    medios=usuario.get('medios'),
                    dificiles=usuario.get('dificiles')
                )

                if usuario is not None:

                    json_student = student.to_dict()
                    print(json_student)

                    return jsonify({'exito': True, 'datos': json_student})
                else:
                    return jsonify({'exito': False, 'mensaje': "NO SE HA BUSCADO"})

            else:
                return jsonify({'exito': False, 'error': 'Usuario no encontrado'}), 404

        except Exception as e:
            print(f"Error en UserController.put_student: {e}")
            return jsonify({'exito': False, 'error': 'Error en el servidor'}), 500
