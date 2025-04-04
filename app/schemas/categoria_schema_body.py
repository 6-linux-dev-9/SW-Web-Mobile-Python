
from marshmallow import fields,validate,Schema

class CategoriaRequest(Schema):
    id = fields.Int(required=False)
    nombre = fields.Str(required=True)