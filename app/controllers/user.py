from flask import Blueprint, jsonify


usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/test',methods = ["GET"])
def testing():
    return jsonify({"message": "User created successfully",
                    "Persona":{
                        "id":2,
                        "nombre":"fernando"
                    }}), 201