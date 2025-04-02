#marshmallow solo para las entradas
from marshmallow import fields, validate, pre_load, Schema


class RolRegisterRequest(Schema):
    nombre = fields.Str(
        required=True,
        validate=[
            validate.Length(min=4),  
            validate.Regexp(r'^(?!\d+$).+', error="El nombre no puede ser solo números")
        ]
    )
    
    @pre_load
    def convertir_mayusculas(self, data, **kwargs):
        if "nombre" in data and isinstance(data["nombre"], str):
            data["nombre"] = data["nombre"].upper()
        return data
