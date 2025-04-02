from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Usuario, Rol, Permiso #importar los modelos
from app.database import db


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


  