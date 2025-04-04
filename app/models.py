from datetime import datetime
from datetime import timezone

#muy importante importar correctamente la base de datos definida en database
from app.database import db
from sqlalchemy import Boolean, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.enums.enums import Sesion

""""
# from flask_sqlalchemy import SQLAlchemy
#manera anterior
# db = SQLAlchemy()

# class Usuario(db.Model):
#     __tablename__ = 'usuarios'
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(80),nullable = False)
#     email = db.Column(db.String(120),unique = True,nullable = False)
#     password = db.Column(db.String(200),nullable=False)
#     rol_id = db.Column(db.Integer,db.ForeignKey('roles.id'),nullable=False)
#     rol = db.relationship('Rol',backref = db.backref('usuarios',lazy = True))
#     def __repr__(self):
#         return f'<Usuario {self.username}>'



# # Modelo de Rol
# class Rol(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(80), unique=True, nullable=False)
#     permisos = db.relationship('Permisos', secondary='rol_permisos', backref=db.backref('roles', lazy='dynamic'))

#     def __repr__(self):
#         return f'<Rol {self.nombre}>'

# # Modelo de Permiso
# class Permisos(db.Model):
#     __tablename__ = 'permisos'
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(80), unique=True, nullable=False)

#     def __repr__(self):
#         return f'<Permisos {self.nombre}>'

# # Tabla intermedia entre Role y Permission (Relación muchos a muchos)
# class RolPermisos(db.Model):
#     __tablename__ = 'rol_permisos'
#     rol_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
#     permiso_id = db.Column(db.Integer, db.ForeignKey('permisos.id'), primary_key=True)
"""
""""
tambien podriamos definir en una case esto
cada quie instanciemos un objeto  se dispara este metodo,seria para validaciones en todo caso
 def __init__(self, **kwargs):
        if 'email' in kwargs:
            validate_email(kwargs['email'])
        if 'password' in kwargs:
            self.set_password(kwargs.pop('password'))
        super().__init__(**kwargs)
"""


# Mixin para funcionalidad común
#clase para que hereden los demas 
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), 
                                               onupdate=datetime.now(timezone.utc))

class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    def soft_delete(self):
        """Realiza eliminación lógica"""
        self.is_deleted = True
        db.session.commit()

    """para obtener usuarios activos o usuarios que no an sido eliminados fisicamente"""
    @classmethod
    def get_active(cls):
        """Filtra solo registros no eliminados"""
        return cls.query.filter_by(is_deleted=False)

# Modelo de Usuario
class Usuario(db.Model, TimestampMixin,SoftDeleteMixin):
    __tablename__ = 'usuarios'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    nombre: Mapped[str] = mapped_column(String(80),nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    rol_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('roles.id'), nullable=False)
    # Relación con el modelo Rol
    #esto hace que la clase Rol tenga un atributo usuarios
    rol: Mapped["Rol"] = relationship('Rol', back_populates='usuarios')

    def __repr__(self):
        return f'<Usuario {self.username}>'

# Modelo de Rol
class Rol(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'roles'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # Relaciones
    #back_populates cuadra con rol refinido en Usuario
    usuarios: Mapped[list["Usuario"]] = relationship('Usuario', back_populates='rol')
    permisos: Mapped[list["Permiso"]] = relationship(
        'Permiso', 
        secondary='rol_permiso',
        back_populates='roles'
    )

    def __repr__(self):
        return f'<Rol {self.nombre}>'

# Modelo de Permiso
class Permiso(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'permisos'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # Relación con roles
    roles: Mapped[list["Rol"]] = relationship(
        'Rol', 
        secondary='rol_permiso',
        back_populates='permisos'
    )

    def __repr__(self):
        return f'<Permiso {self.nombre}>'

# Tabla intermedia para relación muchos-a-muchos
class RolPermiso(db.Model, TimestampMixin):
    __tablename__ = 'rol_permiso'
    rol_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('roles.id'), primary_key=True)
    permiso_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('permisos.id'), primary_key=True)

class BitacoraUsuario(db.Model,TimestampMixin):
    __tablename__ = 'bitacora_usuarios'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ip : Mapped[str] = mapped_column(String,nullable=False)
    username : Mapped[str] = mapped_column(String(40))
    tipo_accion : Mapped[str] = mapped_column(String(1))
    def __repr__(self):
        return f"<Bitacora_usuario> ip: {self.ip}\n username: {self.username}\ntipo_accion: {Sesion.get_by_char(self.tipo_accion).get_descripcion()}"