# routes/LyricGame.py
import os
from dotenv import load_dotenv
from flask import Blueprint
from pymongo import MongoClient
from controllers.LyricGameController import LyricGameController

# Cargar variables de entorno
load_dotenv()
client = MongoClient(os.getenv("MONGO_DB"))
db = client['TFG']

# Inicializamos el controlador
lyric_game_controller = LyricGameController(db)

# Creamos un Blueprint para definir las rutas modulares
rutasLyricGames = Blueprint('rutasLyricGames', __name__)

# Establecemos los endpoints de cada solicitud
rutasLyricGames.add_url_rule('/all', 'get_lyricGames', lyric_game_controller.get_lyricGames)
rutasLyricGames.add_url_rule('/esp/<_id>', 'get_lyricGame', lyric_game_controller.get_lyricGame)
rutasLyricGames.add_url_rule('/agregar', 'post_lyricGame', lyric_game_controller.post_lyricGame, methods=['POST'])
rutasLyricGames.add_url_rule('/<_id>', 'put_lyricGame', lyric_game_controller.put_lyricGame, methods=['PUT'])
rutasLyricGames.add_url_rule('/<_id>', 'delete_lyricGame', lyric_game_controller.delete_lyricGame, methods=['DELETE'])
