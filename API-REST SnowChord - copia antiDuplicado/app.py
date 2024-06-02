from dotenv import load_dotenv
from models.Server import Server

# Configurar dotenv
load_dotenv()

# Creamos nuestro servidor
server = Server()

# Al encender la aplicación, iniciamos el servidor
server.listen()

