#from marshmallow import fields, validate,Schema
from marshmallow import fields,Schema
class MarcaRequest(Schema):
    nombre = fields.Str(required=True)
    #se puede agregar mas validacions aqui abajo

