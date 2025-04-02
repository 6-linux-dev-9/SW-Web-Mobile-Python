# importa de app/database el metodo init_db
# se dispara el init de database
from flask_marshmallow import Marshmallow
from app.database import init_db
from flask import Flask
#from flask_bcrypt import Bcrypt
from app.config.config import Config
from flask_jwt_extended import JWTManager
from app.controllers.auth import bcrypt

#no se de donde lo importa pero yo le creo
from dotenv import load_dotenv
#importamos para hacer uso de los handler
from app.errors.errors import registrar_error_handler 

#importa de controllers el auth, es decir todos los metodos de auth
from app.routers.index import api_bp 

#
# Cargar variables de entorno del .env al sistema parece
#o con source .env 
load_dotenv()

#se inicializa el hashing de contrasenias
# bcrypt = Bcrypt()
#se inicializa para manejar la creacion de tokens JWT
jwt = JWTManager()
ma = Marshmallow()
def create_app():
    app = Flask(__name__)

    # Cargar configuración desde config.py
    #con esto cargamos la configuracion que esta en app/config/config/Config 
    app.config.from_object(Config)

    # inicizamos la bd y las migraciones que estan en database/__init__
    init_db(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    # Registrar Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")

    #registrar el handler
    registrar_error_handler(app)
    
    return app
