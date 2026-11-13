from datetime import datetime

class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio, id_proyecto=None):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ValueError("Debe ingresar un nombre")
        self._nombre = valor

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if not valor.strip():
            raise ValueError("Debe ingresar una descripción")
        self._descripcion = valor

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor):
        try:
            datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD")
        self._fecha_inicio = valor

    def __str__(self):
        return f"Proyecto [ID: {self.id_proyecto}] | {self.nombre} | {self.descripcion} | {self.fecha_inicio}"

