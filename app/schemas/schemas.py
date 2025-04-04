from marshmallow import ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import BitacoraUsuario, Marca, Usuario, Rol, Permiso #importar los modelos
from app.database import db
from app.utils.enums.enums import Sesion


#puros esquemas para las respuestas en formato json
#para poder tener respuestas del json y que no entre a bucle supuestamente
class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario #para poder usar el esquema hacia un tipo de dato
        include_fk = True #incluye la llave foranea,(mostraria rol_id) en la serializacion
        load_instance = True #Permite desSerealizar JSON a objetos de SQLAlchemy
        sqla_session = db.session
        exclude = ["password"] #podrias excluir del modelo

    #RolSchema 
    #es como que el usuario Schema tiene un rol y solamente capturara de rol algunos atributos
    rol = fields.Nested("RolSchema",only=["id","nombre"])

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True
        sqla_session = db.session

    permisos = fields.List(fields.Nested("PermisoSchema", only=["id", "nombre"]))
    

class PermisoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permiso
        load_instance = True
        sqla_session = db.session

    roles = fields.List(fields.Nested("RolSchema", only=["id", "nombre"]))  # Evita el bucle

class BitacoraUsuarioSchema(SQLAlchemyAutoSchema):
    tipo_accion = fields.Method("get_tipo_accion")
    class Meta:
        model = BitacoraUsuario
        load_instance = True
        sqla_session = db.session
    #para parsear el dato de la bd a un dato entendible
    def get_tipo_accion(self,obj):
        try:
            return Sesion.get_by_char(obj.tipo_accion).get_descripcion()
        except (ValueError,AttributeError):
            raise ValidationError("Error en la conversion de datos")
        
class MarcasSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Marca
        load_instance = True
        sqla_session = db.session

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Marca
        load_instance = True
        sqla_session = db.session
    marcas = fields.List(fields.Nested("MarcasSchema",only=["id","nombre"]))
    
    
    

  