from marshmallow import fields, validate,Schema
class UserPasswordRequest(Schema):
    password = fields.Str(required=True,validate=validate.Length(min=4))

class UserEditRequest(Schema):
    username= fields.Str(required=True,validate=validate.Length(min=0))
    nombre = fields.Str(required=True,validate=validate.Length(min=6))
    #podrian venir otros atributos mas que complementen con la informacion del usuario
    