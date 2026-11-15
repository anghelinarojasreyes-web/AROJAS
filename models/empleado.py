from models.usuario import Usuario
from datetime import datetime

class Empleado(Usuario):
    def __init__(self, nombre, correo, direccion, telefono, fecha_inicio, salario, departamento=None, id_empleado=None, contrasena=None):
        super().__init__(nombre, correo, contrasena)
        self.id_empleado = id_empleado
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_inicio = fecha_inicio
        self.salario = salario
        self.departamento = departamento

    @property
    def id_empleado(self):
        return self._id_empleado

    @id_empleado.setter
    def id_empleado(self, valor):
        if valor is not None and (not isinstance(valor, int) or valor <= 0):
            raise ValueError("ID de empleado inválido")
        self._id_empleado = valor

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Debe ingresar una dirección")
        self._direccion = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.isdigit():
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
        try:
            numero = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El salario debe ser un número")
        if numero < 0:
            raise ValueError("El salario no puede ser negativo")
        self._salario = numero

    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, valor):
        self._departamento = valor

    def mostrar_rol(self):
        return "Empleado"

    def __str__(self):
        departamento = self.departamento.nombre if self.departamento else "Sin departamento"
        return f"Empleado [ID: {self.id_empleado}] | {self.nombre} | {self.correo} | {self.direccion} | {self.telefono} | {self.fecha_inicio} | ${self.salario} | {departamento}"
