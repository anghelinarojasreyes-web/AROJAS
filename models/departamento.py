class Departamento:
    def __init__(self, nombre, gerente=None, id_departamento=None):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente = gerente

    @property
    def id_departamento(self):
        return self._id_departamento

    @id_departamento.setter
    def id_departamento(self, valor):
        if valor is not None and (not isinstance(valor, int) or valor <= 0):
            raise ValueError("ID de departamento inválido")
        self._id_departamento = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Debe ingresar el nombre del departamento")
        self._nombre = valor.strip()

    @property
    def gerente(self):
        return self._gerente

    @gerente.setter
    def gerente(self, valor):
        if valor is not None and (not isinstance(valor, int) or valor <= 0):
            raise ValueError("ID de gerente inválido")
        self._gerente = valor

    def obtener_gerente(self):
        if self.gerente is None:
            return None
        from models.gerente_dao import GerenteDAO
        return GerenteDAO.obtener_por_id(self.gerente)

    def __str__(self):
        return f"Departamento [ID: {self.id_departamento}] | Nombre: {self.nombre} | Gerente: {self.gerente or 'Sin asignar'}"
