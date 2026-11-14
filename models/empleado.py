from models.usuario import Usuario
from datetime import datetime

class Empleado(Usuario):
    def __init__(self, nombre, correo, direccion, telefono, fecha_inicio, salario, departamento=None, id_empleado=None):
        super().__init__(nombre, correo)
        self.id_empleado = id_empleado
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_inicio = fecha_inicio
        self.salario = salario
        self.departamento = departamento

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        if not valor.strip():
            raise ValueError("Debe ingresar una dirección")
        self._direccion = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor.isdigit():
            raise ValueError("El teléfono debe contener solo números")

        if len(valor) != 9:
            raise ValueError("El teléfono debe tener 9 dígitos")

        self._telefono = valor

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor):
        try:
            datetime.strptime(valor, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD y ser válida")

        self._fecha_inicio = valor

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        if valor < 0:
            raise ValueError("El salario no puede ser negativo")
        self._salario = valor

    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, valor):
        self._departamento = valor

    def __str__(self):
        departamento = self.departamento.nombre if self.departamento else "Sin departamento"
        return f"Empleado [ID: {self.id_empleado}] | {self.nombre} | {self.correo} | {self.direccion} | {self.telefono} | {self.fecha_inicio} | ${self.salario} | {departamento}"
