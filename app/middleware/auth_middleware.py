from functools import wraps
from flask import request, jsonify, g
from app.errors.errors import GenericError
from app.utils.jwt_utils import decode_auth_token
from app.models import Usuario
from app.database import db
from http import HTTPStatus

#analizar mas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return GenericError(HTTPStatus.UNAUTHORIZED,HTTPStatus.UNAUTHORIZED.phrase,"Error..no tiene token..")
        #si la entrada es Bearer token , si solo viene Authorization entonces obtiene eso
        #pero si viene como Bearer token, entonces eliminar el Bearer,quedadndo con el token

        token = token.split(" ")[1] if " " in token else token#creo que es para el bearer token
        try:
            user_data = decode_auth_token(token)
            print(f"estoy en el metodo token_required {user_data}")

            if not user_data:
                return jsonify({"error": "Token inválido o expirado"}), 401

            usuario = db.session.get(Usuario, user_data["sub"])  

            if not usuario:
                return GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Usuario..no encontrado")

            g.current_user = usuario  # Guardamos el usuario en `g`

            return f(*args, **kwargs)     
        except GenericError:
            db.session.rollback()
            raise  # Relanza GenericError para que lo maneje @app.errorhandler
        except Exception as e:
            db.session.rollback()
            raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             

    return decorated

