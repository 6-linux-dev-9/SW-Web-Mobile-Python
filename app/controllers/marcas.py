from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.database import db
from app.errors.errors import GenericError
from http import HTTPStatus

from app.models import Marca
from app.schemas.marcas_schema_body import MarcaRequest
from app.schemas.pagination_shema import PaginatedResponse
from app.schemas.schemas import MarcasSchema

marcas_bp = Blueprint('marca',__name__)

@marcas_bp.route("/create",methods=["POST"])
def create_marca():
    try:
        body = request.get_json()
        schema = MarcaRequest()
        if schema.validate(body):
            raise ValidationError("Error..Hubo un error al validar los datos...")
        data = schema.load(body)

        marca = Marca.query.filter_by(nombre = data["nombre"]).first()
        if marca:
            marca.is_deleted = False
            db.session.commit()
            return jsonify({
                "message":"Marca Creada con Exito",
                "marca":MarcasSchema().dump(marca)
            }),HTTPStatus.CREATED
        marca = Marca(
            nombre = data["nombre"]
        )
        db.session.add(marca)
        db.session.commit()
        return jsonify({
            "message": "Marca Creada con Exito",
            "marca": MarcasSchema().dump(marca)
        }),HTTPStatus.CREATED
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             
    
@marcas_bp.route("/<int:id>/update",methods=["PUT"])
def update_marca(id):
    try:

        body = request.get_json()
        schema = MarcaRequest()
        if schema.validate(body):
            raise ValidationError("Error..Hubo un error al validar los datos...")
        data = schema.load(body)

        marca = Marca.query.get(id)
        if not marca:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Marca no Encontrada..")
        
        marca.nombre = data["nombre"]
        db.session.commit()
        return jsonify({
            "message": "Marca Actualizada con Exito",
            "marca": MarcasSchema().dump(marca)
        }),HTTPStatus.CREATED
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             
    
@marcas_bp.route('/<int:id>/delete',methods=["DELETE"])
def delete_marca(id):
    try:
        marca = Marca.query.get(id)
        if not marca:
                raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Marca no encontrada..")
        #realizamos el softDelete
        marca.soft_delete()
        
        return jsonify({
            "message":"Rol eliminado con exito"
        })
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados                 #


#obtiene la lista de marcas no eliminadas
@marcas_bp.route('/list',methods=["GET"])
def getAll():
    return MarcasSchema().dump(Marca.get_active(),many=True)

@marcas_bp.route('/list-paginate',methods=["GET"])
def getPaginate():
    try:
        return PaginatedResponse.paginate(Marca.get_active(),MarcasSchema)
    except Exception as e:
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR,HTTPStatus.INTERNAL_SERVER_ERROR.phrase,f"Error..hubo un error inesperado..{str(e)}")
    
