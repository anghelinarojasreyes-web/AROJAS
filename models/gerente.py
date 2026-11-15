from models.usuario import Usuario

class Gerente(Usuario):
    def __init__(self, nombre, correo, contrasena=None, id_gerente=None):
        super().__init__(nombre, correo, contrasena)
        self.id_gerente = id_gerente
        self.departamento = None

    @property
    def id_gerente(self):
        return self._id_gerente

    @id_gerente.setter
    def id_gerente(self, valor):
        if valor is not None and (not isinstance(valor, int) or valor <= 0):
            raise ValueError("ID de gerente inválido")
        self._id_gerente = valor

    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, valor):
        self._departamento = valor

    def asignar_departamento(self, departamento):
        self.departamento = departamento

    def consultar_departamento(self):
        if self.departamento:
            return self.departamento.nombre
        return "Sin departamento asignado"

    def puede_editar_empleado(self, empleado):
        if empleado.departamento:
            return empleado.departamento.gerente == self.id_gerente
        return False

    def mostrar_rol(self):
        return "Gerente"

    def __str__(self):
        return f"Gerente [ID: {self.id_gerente}] | {self.nombre} | {self.correo}"
