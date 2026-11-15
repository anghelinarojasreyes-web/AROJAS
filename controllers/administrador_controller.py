from models.administrador import Administrador
from models.administrador_dao import AdministradorDAO
from views.administrador_view import AdministradorView

class AdministradorController:
    def __init__(self):
        self.view = AdministradorView()

    def ejecutar(self, administrador_actual):
        while True:
            opcion = self.view.mostrar_menu()

            if opcion == 1:
                self.agregar(administrador_actual)
            elif opcion == 2:
                self.editar()
            elif opcion == 3:
                self.eliminar(administrador_actual)
            elif opcion == 4:
                self.imprimir_uno()
            elif opcion == 5:
                self.imprimir_todos()
            elif opcion == 0:
                break
            else:
                self.view.mostrar_mensaje("Opción no válida")

    def pedir_id(self):
        while True:
            numero = self.view.solicitar_id()

            if numero is None:
                return None

            if AdministradorDAO.obtener_por_id(numero):
                return numero

            self.view.mostrar_mensaje("Error: El administrador no existe")

    def validar_correo(self, correo, id_actual=None):
        partes = correo.split("@")

        if (
            len(partes) != 2
            or not partes[0]
            or "." not in partes[1]
            or " " in correo
        ):
            self.view.mostrar_mensaje("Error: Correo inválido")
            return False

        existente = AdministradorDAO.obtener_por_correo(correo)

        if existente and existente.id_administrador != id_actual:
            self.view.mostrar_mensaje("Error: Correo ya registrado")
            return False

        return True

    def agregar(self, administrador_actual):
        datos = self.view.formulario_nuevo()

        if datos is None:
            return

        if not self.validar_correo(datos["correo"]):
            return

        try:
            administrador = Administrador(
                datos["nombre"],
                datos["correo"],
                datos["contrasena"]
            )

            if administrador_actual.registrar_administrador(administrador):
                self.view.mostrar_mensaje(
                    "Administrador registrado correctamente"
                )
            else:
                self.view.mostrar_mensaje(
                    "No se pudo registrar el administrador"
                )

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def editar(self):
        numero = self.pedir_id()

        if numero is None:
            return

        administrador = AdministradorDAO.obtener_por_id(numero)
        datos = self.view.formulario_editar(administrador)

        if datos is None:
            return

        if not self.validar_correo(datos["correo"], numero):
            return

        administrador.nombre = datos["nombre"]
        administrador.correo = datos["correo"]

        if AdministradorDAO.actualizar(administrador):
            self.view.mostrar_mensaje("Actualizado correctamente")
        else:
            self.view.mostrar_mensaje("No se pudo actualizar")

    def eliminar(self, administrador_actual):
        numero = self.pedir_id()

        if numero is None:
            return

        if numero == administrador_actual.id_administrador:
            self.view.mostrar_mensaje(
                "No puede eliminar su propia cuenta"
            )
            return

        administradores = AdministradorDAO.obtener_todos()

        if len(administradores) <= 1:
            self.view.mostrar_mensaje(
                "No puede eliminar al último administrador"
            )
            return

        if self.view.confirmar_eliminacion():
            if AdministradorDAO.eliminar(numero):
                self.view.mostrar_mensaje("Eliminado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo eliminar")
        else:
            self.view.mostrar_mensaje("Operación cancelada")

    def imprimir_uno(self):
        numero = self.pedir_id()

        if numero is not None:
            administrador = AdministradorDAO.obtener_por_id(numero)
            self.view.mostrar_objeto(administrador)

    def imprimir_todos(self):
        administradores = AdministradorDAO.obtener_todos()
        self.view.mostrar_lista(administradores)
