import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from routes.Cancion import rutasCanciones
from routes.Curso import rutasCursos
from routes.LyricGame import rutasLyricGames
from routes.User import rutasUsuarios
from routes.Mascota import rutasMascotas
from routes.Acorde import rutasAcordes

class Server:

    def __init__(self) -> None:
        try:
            mongo_url = os.getenv("MONGO_DB")
            if not mongo_url:
                raise Exception("Variable de entorno 'MONGO_DB' no encontrada.")

            self.app = Flask(__name__)
            self.port = 3000
            self.rutasApi = {
                "usuarios":"/usuarios/",
                "canciones":"/canciones/",
                "lyricGames":"/lyricGames/",
                "cursos":"/cursos/",
                "mascotas":"/mascotas/",
                "acordes":"/acordes/"
            }
            self.cliente_mongo = MongoClient(mongo_url)
            self.configurar_cors()
            self.routes()
        except Exception as e:
            print(f"Error al iniciar el servidor: {e}")

    def routes(self) -> None:
        try:
            self.app.register_blueprint(rutasUsuarios, url_prefix=self.rutasApi["usuarios"])
            self.app.register_blueprint(rutasCanciones, url_prefix=self.rutasApi["canciones"])
            self.app.register_blueprint(rutasLyricGames, url_prefix=self.rutasApi["lyricGames"])
            self.app.register_blueprint(rutasCursos, url_prefix=self.rutasApi["cursos"])
            self.app.register_blueprint(rutasMascotas, url_prefix=self.rutasApi["mascotas"])
            self.app.register_blueprint(rutasAcordes, url_prefix=self.rutasApi["acordes"])

        except Exception as e:
            print(f"Error al registrar las rutas: {e}")

    def configurar_cors(self) -> None:
        CORS(self.app)
    def listen(self) -> None:
        try:
            self.app.run(port=self.port)
        except Exception as e:
            print(f"Error al iniciar la aplicación: {e}")


if __name__ == "__main__":
    servidor = Server()
    servidor.listen()
