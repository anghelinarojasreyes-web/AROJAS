class Departamento:
    def __init__(self, nombre, gerente=None, id_departamento=None):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente = gerente

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ValueError("Debe ingresar el nombre del departamento")
        self._nombre = valor

    @property
    def gerente(self):
        return self._gerente

    def obtener_gerente(self):
        if self._gerente is None:
            return None

        from models.gerente_dao import GerenteDAO
        return GerenteDAO.obtener_por_id(self._gerente)

    @gerente.setter
    def gerente(self, valor):
        self._gerente = valor

    def __str__(self):
        return f"Departamento [ID: {self.id_departamento}] | Nombre: {self.nombre} | Gerente: {self.gerente or 'Sin asignar'}"
