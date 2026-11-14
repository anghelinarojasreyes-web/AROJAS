from datetime import datetime

class RegistroTiempo:
    def __init__(self, fecha, horas_trabajadas, descripcion, empleado, proyecto, id_registro=None):
        self.id_registro = id_registro
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion = descripcion
        self.empleado = empleado
        self.proyecto = proyecto

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        try:
            datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD")
        self._fecha = valor

    @property
    def horas_trabajadas(self):
        return self._horas_trabajadas

    @horas_trabajadas.setter
    def horas_trabajadas(self, valor):
        if valor <= 0:
            raise ValueError("Las horas deben ser mayores a 0")
        self._horas_trabajadas = valor

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if not valor.strip():
            raise ValueError("Debe ingresar una descripción")
        self._descripcion = valor

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
