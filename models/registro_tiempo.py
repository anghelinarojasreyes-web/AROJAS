from datetime import datetime
import math

class RegistroTiempo:
    def __init__(self, fecha, horas_trabajadas, descripcion, empleado, proyecto, id_registro=None):
        self.id_registro = id_registro
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion = descripcion
        self.empleado = empleado
        self.proyecto = proyecto

    @property
    def id_registro(self):
        return self._id_registro

    @id_registro.setter
    def id_registro(self, valor):
        if valor is not None and (not isinstance(valor, int) or valor <= 0):
            raise ValueError("ID de registro inválido")
        self._id_registro = valor

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        try:
            datetime.strptime(valor, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD y ser válida")
        self._fecha = valor

    @property
    def horas_trabajadas(self):
        return self._horas_trabajadas

    @horas_trabajadas.setter
    def horas_trabajadas(self, valor):
        try:
            horas = float(valor)
        except (ValueError, TypeError):
            raise ValueError("Las horas deben ser un número")
        if not math.isfinite(horas) or horas <= 0:
            raise ValueError("Las horas deben ser mayores a 0")
        self._horas_trabajadas = horas

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Debe ingresar una descripción")
        self._descripcion = valor.strip()

    @property
    def empleado(self):
        return self._empleado

    @empleado.setter
    def empleado(self, valor):
        if valor is None:
            raise ValueError("Debe seleccionar un empleado")
        self._empleado = valor

    @property
    def proyecto(self):
        return self._proyecto

    @proyecto.setter
    def proyecto(self, valor):
        if valor is None:
            raise ValueError("Debe seleccionar un proyecto")
        self._proyecto = valor

    def __str__(self):
        return f"Registro [ID: {self.id_registro}] | Fecha: {self.fecha} | Horas: {self.horas_trabajadas} | Descripción: {self.descripcion} | Empleado: {self.empleado.nombre} | Proyecto: {self.proyecto.nombre}"
