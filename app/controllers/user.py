from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from app.controllers.auth import obtener_ip
from app.errors.errors import GenericError
from app.models import BitacoraUsuario, Usuario
from http import HTTPStatus
from app.database import db
from app.schemas.user_schema_body import UserEditRequest, UserPasswordRequest
from app.utils.enums.enums import Sesion
#from app.schemas.schemas import UsuarioSchema

bcrypt = Bcrypt()
usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/test',methods = ["GET"])
def testing():
    id = autenticated_user_id()
    return jsonify({"message": "User created successfully",
                    "Persona":{
                        "id":2,
                        "nombre":f"fernando {id}"
                    }}), 201




@usuario_bp.route('/me',methods=["GET"])
@jwt_required()
#es posible usarlo el id
def autenticated_user_id():
    current_user = get_jwt_identity() #obtiene el id del usuario autenticado
    print(current_user)
    return jsonify({
        "message":"sexo"
    }),200


#solamente ingresa el password para resetear la contrasenia

@usuario_bp.route('/change-password',methods=["PUT"])
@jwt_required()
def change_password():
    try:
        idUsuarioAutenticado = get_jwt_identity()
        usuario = Usuario.query.filter_by(id = int(idUsuarioAutenticado)).first()
        if not usuario:
            raise GenericError(HTTPStatus.UNAUTHORIZED,HTTPStatus.UNAUTHORIZED.phrase,"Error.. usuario no autenticado..")
        body = request.get_json()
        schema = UserPasswordRequest()
        if schema.validate(body):
            raise ValidationError("Hubo un error al momento de validar los datos...")
        
        data = schema.load(body)
        print(f"data: {data}")
        #si en el caso de que no cuadren sus password,quiere decir que el usuario cambio de contra
        if not bcrypt.check_password_hash(usuario.password,data["password"]):
            usuario.password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

        bitacora_usuario = BitacoraUsuario(
            ip = obtener_ip(),
            username = usuario.username,
            tipo_accion = Sesion.ACTUALIZACION_PASSWORD._value_[0],
        )
        db.session.add(bitacora_usuario)
        #si no, quiere decir que no la cambio
        db.session.commit()
        return jsonify({
            "message":"Password Cambiada con Exito!"
        })
    except GenericError :
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR,HTTPStatus.INTERNAL_SERVER_ERROR.phrase,str(e))



@usuario_bp.route('/edit',methods=["PUT"])
@jwt_required()
def editAtributtes():
    try:
        idUsuarioAutenticado = get_jwt_identity()
        usuario = Usuario.query.filter_by(id = int(idUsuarioAutenticado)).first()
        if not usuario:
            raise GenericError(HTTPStatus.UNAUTHORIZED,HTTPStatus.UNAUTHORIZED.phrase,"Error.. usuario no autenticado..")
        body = request.get_json()
        schema = UserEditRequest()
        if schema.validate(body):
            raise ValidationError("Error...Formato de datos no valido...")
        data = schema.load(body)

        usuario.username = data["username"]
        usuario.nombre = data["nombre"]

        bitacora_usuario = BitacoraUsuario(
            ip = obtener_ip(),
            username = usuario.username,
            tipo_accion = Sesion.ACTUALIZACION_DATA._value_[0],
        )
        db.session.add(bitacora_usuario)
        db.session.commit()
        return jsonify({
            "message":"campos modificados con exito!"
            })
    except GenericError:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR,HTTPStatus.INTERNAL_SERVER_ERROR.phrase,f"Error..algo salio mal..{str(e)}")

#faltaria el de editar perfil




