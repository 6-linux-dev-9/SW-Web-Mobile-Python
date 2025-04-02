from marshmallow import Schema, validate, fields,pre_load

#esta clase hereda de la clase Rol todos sus metodos
class PermissionRequest(Schema):
    # Agregar nuevos campos específicos para la clase PermissionRequest
    nombre = fields.Str(
        required=True,
        validate=[
            validate.Length(min=4),  # Validación para que el permiso tenga al menos 4 caracteres
            validate.Regexp(r'^(?!\d+$).+', error="El nombre no puede ser solo números")
        ]
    )
    id = fields.Integer(required=False) # es un campo opcional, puede que este en algun modelo, como tambien puede que no

    # Si necesitas realizar un pre-carga adicional (por ejemplo, convertir a mayúsculas) para algún campo específico de PermissionRequest, puedes hacerlo aquí
    @pre_load
    def convertir_mayusculas_permiso(self, data, **kwargs):
        if "nombre" in data and isinstance(data["nombre"], str):
            data["nombre"] = data["nombre"].upper()
        return data