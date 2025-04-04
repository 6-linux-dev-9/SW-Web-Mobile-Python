from flask import Blueprint
from app.controllers.auth import auth_bp  # Ya vimos este
from app.controllers.user import usuario_bp  # Ejemplo de otro Blueprint
from app.controllers.rol import rol_bp
from app.controllers.permiso import permiso_bp
from app.controllers.marcas import marcas_bp
from app.controllers.categorias import categoria_bp
api_bp = Blueprint('api', __name__)

# Registrar Blueprints con prefijos
api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(usuario_bp, url_prefix='/usuarios')
api_bp.register_blueprint(rol_bp, url_prefix='/rol')
api_bp.register_blueprint(permiso_bp, url_prefix='/permisos')
api_bp.register_blueprint(marcas_bp,url_prefix='/marcas')
api_bp.register_blueprint(categoria_bp,url_prefix='/categorias')
