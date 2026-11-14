from models.usuario import Usuario

class Gerente(Usuario):
    def __init__(self, nombre, correo, contrasena=None, id_gerente=None):
        super().__init__(nombre, correo, contrasena)
        self.id_gerente = id_gerente
        self.departamento = None

    def asignar_departamento(self, departamento):
        self.departamento = departamento

    def consultar_departamento(self):
        if self.departamento:
            return self.departamento.nombre
        return "Sin departamento asignado"

    def __str__(self):
        return f"Gerente [ID: {self.id_gerente}] | {self.nombre} | {self.correo}"
