from flask import Flask
from flask_cors import CORS
import os
from pymongo import MongoClient
from routes.User import rutasUsuarios
from controllers.UserController import UserController

class Server:

    def __init__(self) -> None:
        try:
            mongo_url = os.getenv("MONGO_DB")
            if not mongo_url:
                raise Exception("Variable de entorno 'MONGO_DB' no encontrada.")

            self.app = Flask(__name__)
            self.port = 3000
            self.rutasApi = {
                "usuarios": "/usuarios/",
            }
            self.cliente_mongo = MongoClient(mongo_url)
            self.db = self.cliente_mongo["Ejemplo"]
            self.routes()
        except Exception as e:
            print(f"Error al iniciar el servidor: {e}")

    def routes(self) -> None:
        try:
            self.app.register_blueprint(rutasUsuarios, url_prefix=self.rutasApi["usuarios"])
        except Exception as e:
            print(f"Error al registrar las rutas: {e}")

    def listen(self) -> None:
        try:
            self.app.run(port=self.port)
        except Exception as e:
            print(f"Error al iniciar la aplicación: {e}")


if __name__ == "__main__":
    servidor = Server()
    servidor.listen()
