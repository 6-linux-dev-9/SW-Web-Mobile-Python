from marshmallow import fields,validate,Schema

#para formateo de datos de entrada
#es como definir un DTO de request
class AuthRegisterSchemaBody(Schema):
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True,validate=validate.Length(min=4))

class AuthLoginSchemaBody(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)