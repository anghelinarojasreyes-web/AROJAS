import hashlib

class Usuario:
    def __init__(self, nombre, correo, contrasena=None):
        self.nombre = nombre
        self.correo = correo
        self._contrasena = None

        if contrasena is not None:
            self.contrasena = contrasena

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ValueError("Debe ingresar un nombre")
        self._nombre = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor.strip():
            raise ValueError("Debe ingresar un correo")
        self._correo = valor

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        if not valor.strip():
            raise ValueError("Debe ingresar una contraseña")
        self._contrasena = hashlib.sha256(valor.encode()).hexdigest()

    def verificar_contrasena(self, valor):
        return self._contrasena == hashlib.sha256(valor.encode()).hexdigest()