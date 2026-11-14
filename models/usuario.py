import hashlib
import os
import hmac

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
        if not valor.strip() or "@" not in valor:
            raise ValueError("Debe ingresar un correo válido")
        self._correo = valor

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        if len(valor) < 8 or len(valor) > 20:
            raise ValueError("La contraseña debe tener entre 8 y 20 caracteres")

        if not any(letra.isalpha() for letra in valor):
            raise ValueError("La contraseña debe tener al menos una letra")

        if not any(numero.isdigit() for numero in valor):
            raise ValueError("La contraseña debe tener al menos un número")

        sal = os.urandom(16)
        hash_contrasena = hashlib.pbkdf2_hmac(
            "sha256",
            valor.encode(),
            sal,
            200000
        )

        self._contrasena = sal.hex() + ":" + hash_contrasena.hex()

    def verificar_contrasena(self, valor):
        if self._contrasena is None:
            return False

        if ":" not in self._contrasena:
            hash_antiguo = hashlib.sha256(valor.encode()).hexdigest()
            return hmac.compare_digest(self._contrasena, hash_antiguo)

        try:
            sal_hex, hash_guardado = self._contrasena.split(":")
            sal = bytes.fromhex(sal_hex)

            hash_ingresado = hashlib.pbkdf2_hmac(
                "sha256",
                valor.encode(),
                sal,
                200000
            )

            return hmac.compare_digest(
                hash_ingresado,
                bytes.fromhex(hash_guardado)
            )

        except ValueError:
            return False
