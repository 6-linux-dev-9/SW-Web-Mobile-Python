from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.database import db
from app.errors.errors import GenericError
from app.models import Categoria, Marca, MarcaCategoria
from app.schemas.categoria_schema_body import CategoriaRequest
from app.schemas.schemas import CategoriaSchema
from http import HTTPStatus

categoria_bp = Blueprint('categoria',__name__)

@categoria_bp.route('/create',methods=["POST"])
def createCategoria():
    try:     
        body = request.get_json()
        schema = CategoriaRequest()
        if schema.validate(body):
            raise ValidationError("Error..Hubo un error en la validacion de datos")
        data = schema.load(body)

        categoria = Categoria(
            nombre = data["nombre"]
        )
        db.session.add(categoria)
        db.session.commit()
        return jsonify({
            "message":"categoria creada con exito",
            "categoria":CategoriaSchema().dump(categoria)
        })
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             
    
@categoria_bp.route('/<int:id>/update',methods=["PUT"])
def updateCategoria(id):
    try:
        body = request.get_json()
        schema = CategoriaRequest()
        if schema.validate(body):
            raise ValidationError("Error..Hubo un error al validar los datos...")
        data = schema.load(body)

        categoria = Categoria.query.get(id)
        if not categoria:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Categoria no Encontrada..")
        
        categoria.nombre = data["nombre"]
        db.session.commit()
        return jsonify({
            "message": "Marca Actualizada con Exito",
            "categoria": CategoriaSchema().dump(categoria)
        }),HTTPStatus.CREATED
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             
    
@categoria_bp.route("/<int:id>/delete",methods=["DELETE"])
def delete_category(id):
    try:
        category = Categoria.query.get(id)
        if not category:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Categoria no encontrada...")
        category.soft_delete()
        return jsonify({
            "message":"categoria eliminada con exito",
        }),201
    except GenericError:
        db.session.rollback()
        raise  # Relanza GenericError para que lo maneje @app.errorhandler
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados             
    
@categoria_bp.route('/<int:id>/agregar-marcas',methods=["POST"])
def add_marca_to_category(id):
    try:
        category = Categoria.query.get(id)
        if not category:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Categoria no encontrada...")
        body = request.get_json()
        schema = CategoriaRequest()
        if schema.validate(body):
            raise ValidationError("Error en la validacion de datos")
        data = schema.load(body)
        marca = Marca.query.get(data["id"])
        if not marca:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Categoria no encontrada...")
        if marca in category.marcas:
            raise GenericError(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,"Error..La marca ya esta en el asiganada a esta categoria..")
        category.marcas.append(marca)
        db.session.commit()
        return jsonify({
            "message":"marca agregada con exito",
            "categoria":CategoriaSchema().dump(category)
        })
    except GenericError:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados


@categoria_bp.route('/<int:id_categoria>/marca/<int:id_marca>',methods=["DELETE"])
def eliminar_marca_de_categoria(id_categoria,id_marca):

    try:
        category = Categoria.query.get(id_categoria)
        if not category:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Categoria no encontrada...")
        marca = Marca.query.get(id_marca)
        if not marca:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Marca no encontrada...")
        if marca not in category.marcas:
            raise GenericError(HTTPStatus.NOT_FOUND,HTTPStatus.NOT_FOUND.phrase,"Error..Marca no encontrada en la categoria...")

        category.marcas.remove(marca)
        db.session.commit()
        return jsonify({
            "message":"marca eliminada con Exito",
            "categoria":CategoriaSchema().dump(category)
        })
    except GenericError:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise GenericError(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, str(e))  # Solo errores inesperados


    


        
