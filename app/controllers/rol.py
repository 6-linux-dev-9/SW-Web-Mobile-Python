from http import HTTPStatus
from flask import Blueprint, request,jsonify
from marshmallow import ValidationError
#from psycopg2 import IntegrityError #usaremos el request para acceder al request, jsonify para usar respuestas json
from app.errors.errors import GenericError
from app.models import Permiso, Rol #hacemos referencia al modelo usuario por a ese modelo consultaremos
from app.database import db  #usaremos la instancia a la base de datos
from app.schemas.permission_schema_body import PermissionRequest
from app.schemas.rol_schema_body import RolRegisterRequest
from app.schemas.schemas import RolSchema   #usamos un esquema de validacion de tipos

rol_bp = Blueprint('rol', __name__) #por defecto se nombra un blueprint 

@rol_bp.route('/create', methods=["POST"]) 
def create():
    try:
        #recibimos los datos
        body = request.get_json()
        print(f"body = {body}")
        schema = RolRegisterRequest()
        if schema.validate(body): #si hay errores
            raise ValidationError("Hubo un error en la validacion de datos..")
        #ya validado los datos
        data = schema.load(body) #ya es JSON
        print(f"data: {data}")
        rol = Rol.query.filter_by(nombre = data["nombre"]).first()
        #si encontro un rol con el mismo nombre ,solo actualizar su estado del softdelete
        if rol:
            rol.is_deleted = False
            db.session.commit()
            schema_response = RolSchema()
            response = schema_response.dump(rol)
            return jsonify({
                "message": "Rol creado exitosamente",  # Mensaje adicional
                "data": response  # Los datos del rol creado
            }), HTTPStatus.CREATED  # Código de estado 201
        nuevo_rol = Rol(
            nombre = data["nombre"]
        )    
        #insertamos en la bd
        db.session.add(nuevo_rol)
        db.session.commit()
        #para serializar la respuesta
        schema_response = RolSchema()
        response = schema_response.dump(nuevo_rol)
        #agregamos un mensaje,solamente para probar
        return jsonify({
            "message": "Rol creado exitosamente",  # Mensaje adicional
            "data": response  # Los datos del rol creado
        }), HTTPStatus.CREATED  # Código de estado 201
    #tira un 200 aunque no lo definamos
        
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             
    
@rol_bp.route('/<int:id>/update',methods=["PUT"])
def update(id):
    try:
        # Obtenemos el rol por el id proporcionado en la URL
        #con eso accedemos al id de la url
        rol = Rol.query.get(id)
        
        if not rol:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Rol no encontrado..")
        
        # Obtenemos los datos del cuerpo de la solicitud
        body = request.get_json()
        
        # Validamos los datos con el esquema
        schema = RolRegisterRequest()
        if schema.validate(body):
            raise ValidationError("Hubo un error en la validación de datos..")
        
        # Cargamos los datos validados
        data = schema.load(body)
        
        # Actualizamos el rol
        rol.nombre = data["nombre"]
        
        # Guardamos los cambios en la base de datos
        db.session.commit()
        
        # Para serializar la respuesta
        schema_response = RolSchema()
        response = schema_response.dump(rol)
        
        # Retornamos el rol actualizado con un mensaje y código de estado 200
        return jsonify({
            "message": "Rol actualizado exitosamente",
            "data": response
        }), HTTPStatus.OK  # Código 200 para éxito
        
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             
    
@rol_bp.route('/<int:id>/delete',methods=["DELETE"])
def delete(id):
    try:
        rol = Rol.query.get(id)
        if not rol:
                raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Rol no encontrado..")
        #realizamos el softDelete
        rol.soft_delete()
        
        return jsonify({
            "message":"Rol eliminado con exito"
        })
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             

@rol_bp.route('/list',methods=["GET"])
def getAll():
    roles = Rol.query.all()  
    return jsonify(RolSchema(many=True).dump(roles))

@rol_bp.route('/test',methods=["GET"])
def test():
    return jsonify({"message":"Testeando"})

#viene un cuerpo permiso completo
"""
sirve para asignar un permiso a un rol
{
    id:1,
    nombre: "CREAR USUARIO"
}
"""
@rol_bp.route('/<int:id_rol>/asignar',methods=["POST"])
def assigPermissionToRole(id_rol):
    try:
        rol = Rol.query.get(id_rol)

        if not rol:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Rol no encontrado..")
        body = request.get_json()
        schema = PermissionRequest()
        if schema.validate(body):
            raise ValidationError("Error en la definicion de datos.")

        data = schema.load(body)

        permiso = Permiso.query.get(data["id"])
        if not permiso:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Permiso no encontrado..")
        
        #necesito verificar si el permiso a insertar ya esta asignado en el rol, lo normal seria hacer un for, pero haber que pasa

        #validacion si el permisos ya esta en rol.permisos
        if permiso in rol.permisos:
            raise GenericError(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,"Error..El Permiso ya se encuentra asignado al sistema")
        rol.permisos.append(permiso)
        db.session.commit()
        return jsonify(RolSchema().dump(rol))
    
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:# aunque no se si esto funcione
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados
    
@rol_bp.route("/<int:id_rol>/permiso/<int:id_permiso>",methods=["DELETE"])
def deletePermissionForRole(id_rol,id_permiso):
    try:
        rol = Rol.query.get(id_rol)

        if not rol:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Rol no encontrado..")
       
        permiso = Permiso.query.get(id_permiso)
        if not permiso:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error Permiso no encontrado..")
        
        #necesito verificar si el permiso a insertar ya esta asignado en el rol, lo normal seria hacer un for, pero haber que pasa

        #validacion si el permisos ya esta en rol.permisos
        rol.permisos.remove(permiso)
        db.session.commit()
        return jsonify(RolSchema().dump(rol))
    
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:# aunque no se si esto funcione
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados

