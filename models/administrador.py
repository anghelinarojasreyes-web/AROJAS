from models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, nombre, correo, contrasena):
        super().__init__(nombre, correo, contrasena)

    def mostrar_rol(self):
        return "Administrador"