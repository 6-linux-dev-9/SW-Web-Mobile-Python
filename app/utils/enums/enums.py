from enum import Enum

from app.errors.errors import GenericError
from http import HTTPStatus
class Sesion(Enum):

    LOGIN = ('I',"INICIO DE SESION")
    LOGOUT = ('C',"CIERRE DE SESION")
    REGISTRO_DE_USUARIO = ('R',"REGISTRO DE USUARIO")
    ACTUALIZACION_PASSWORD = ('P',"ACTUALIZACION DE PASSWORD")
    ACTUALIZACION_DATA = ('U',"ACTUALIZACION DE DATOS")
    DELETE_ACCOUNT = ('D',"ELIMINACION DE CUENTA")
    BLOCK_ACCOUNT = ('B',"BLOCKEO DE CUENTA")

    @classmethod
    #cls se refiere a la clase misma
    def get_by_char(cls,db_caracter):
        for action in cls:
            if action.value[0] == db_caracter:
                return action  #RETORNA EL ATRIBUTO ENUM COMO POR EJEMPLO BLOCK_ACCOUNT
            #POR LO TANTO DEBES HACER UN GET DESCRIPTION PARA OBTENER SU VALOR REAL
        raise GenericError(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,f"Error..Caracter de accion no valido {db_caracter}")
    
    def get_descripcion(self):
        return self.value[1]
    def get_caracter(self):
        return self.value[0]
    


class EstadoServicio(Enum):
    PENDIENTE= 'PD',
    PAGADO = 'PG'

class EstadoProducto(Enum):
    DISPONIBLE = "D"
    NO_DISPONIBLE = "ND" 