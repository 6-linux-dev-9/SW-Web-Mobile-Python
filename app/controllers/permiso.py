from flask import Blueprint, jsonify, request
from http import HTTPStatus

from marshmallow import ValidationError
from app.errors.errors import GenericError
from app.models import Permiso
from app.schemas.permission_schema_body import PermissionRequest
from app.database import db
from app.schemas.schemas import PermisoSchema

permiso_bp = Blueprint("permiso",__name__)
@permiso_bp.route('/create',methods=["POST"])
def crearPermisos():
    try:
        body = request.get_json()
        schema = PermissionRequest()
        if schema.validate(body):
            raise GenericError(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,"Error Datos No validos...")
        #datos validados

        data = schema.load(body) #lo pasa a diccionario

        print(data)

        permiso = Permiso.query.filter_by(nombre = data["nombre"]).first()

    #si encuentra el mismo permiso capaz y ya fue insertado entonces solamente cambia el estado de eliminado a false
        if permiso:
            permiso.is_deleted = False
            db.session.commit()
            return jsonify(PermisoSchema().dump(permiso)),HTTPStatus.CREATED

        #en el caso de que el permiso sea nuevo

        nuevo_permiso = Permiso(
            nombre = data["nombre"]
        )
        db.session.add(nuevo_permiso)

        db.session.commit()

        return jsonify(PermisoSchema().dump(nuevo_permiso)),HTTPStatus.CREATED
        
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             

    
@permiso_bp.route('/<int:id>/update',methods=["PUT"])
def update(id):
    try:
        # Obtenemos el rol por el id proporcionado en la URL
        #con eso accedemos al id de la url
        permiso = Permiso.query.get(id)
        
        if not permiso:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Permiso no encontrado..")
        
        # Obtenemos los datos del cuerpo de la solicitud
        body = request.get_json()
        
        # Validamos los datos con el esquema
        schema = PermissionRequest()
        if schema.validate(body):
            raise ValidationError("Hubo un error en la validación de datos..")
        
        # Cargamos los datos validados
        data = schema.load(body)
        
        # Actualizamos el rol
        permiso.nombre = data["nombre"]
        
        # Guardamos los cambios en la base de datos
        db.session.commit()
        
        return jsonify(PermisoSchema().dump(permiso)),HTTPStatus.CREATED
        
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados                       str(err))
    
@permiso_bp.route('/<int:id>/delete',methods=["DELETE"])
def delete(id):
    try:
        permiso = Permiso.query.get(id)
        if not permiso:
                raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Permiso no encontrado..")
        #realizamos el softDelete
        permiso.soft_delete()
        
        return jsonify({
            "message":"Rol eliminado con exito"
        })
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados                              str(e))

@permiso_bp.route('/list',methods=["GET"])
def getAll():
    roles = Permiso.query.all()  
    return jsonify(PermisoSchema(many=True).dump(roles))


@permiso_bp.route('/<int:id>/get',methods=["GET"])
def findById(id):
    try:
        permiso = Permiso.query.get(id)
        if not permiso:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Permiso no encontrado..")
        return jsonify(PermisoSchema().dump(permiso)),HTTPStatus.OK
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados                    #             str(e))
        




        
