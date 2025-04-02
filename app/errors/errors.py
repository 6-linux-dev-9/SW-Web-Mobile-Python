from datetime import datetime, timezone
from http import HTTPStatus
from flask import jsonify
from marshmallow import ValidationError

#una clase de error general
#cada vez que lanze esta excepcion se dispara

#se asume que el status del error lo importaremos de python,el mensaje nos inventamos o creamos un enum
class GenericError(Exception):
    def __init__(self, status,error,message):
        self.status = status
        self.error = error
        self.message = message
    def __str__(self):
        return f"{self.error}: {self.message}"

def registrar_error_handler(app):
    #se dispara cuando se lanza la excepcion generica ,tirando un json de error,claro que debemos pasarle algunos datos
    @app.errorhandler(GenericError)
    # 404,"Not Found","Error DTO no encontrado",
    #recibira un objeto GenericError
    def handle_backend_error(error):
        return jsonify({"error":error.error,
                        "message":error.message,
                        "fecha":datetime.now(timezone.utc)}),error.status
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"error":HTTPStatus.BAD_REQUEST,
                        "message":error.messages,
                        "fecha":datetime.now(timezone.utc)}),HTTPStatus.BAD_REQUEST
    
    



    
