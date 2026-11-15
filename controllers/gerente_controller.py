from models.gerente import Gerente
from models.gerente_dao import GerenteDAO
from models.departamento_dao import DepartamentoDAO
from views.gerente_view import GerenteView

class GerenteController:
    def __init__(self):
        self.view = GerenteView()

    def ejecutar(self, administrador):
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 1:
                self.agregar(administrador)
            elif opcion == 2:
                self.editar()
            elif opcion == 3:
                self.eliminar(administrador)
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
            if GerenteDAO.obtener_por_id(numero):
                return numero
            self.view.mostrar_mensaje("Error: El gerente no existe")

    def validar_correo(self, correo, id_actual=None):
        if "@" not in correo or "." not in correo.split("@")[-1] or " " in correo:
            self.view.mostrar_mensaje("Error: Correo inválido")
            return False

        existente = GerenteDAO.obtener_por_correo(correo)
        if existente and existente.id_gerente != id_actual:
            self.view.mostrar_mensaje("Error: Correo ya registrado")
            return False
        return True

    def agregar(self, administrador):
        datos = self.view.formulario_nuevo()
        if datos is None:
            return
        if not self.validar_correo(datos["correo"]):
            return

        try:
            gerente = Gerente(
                datos["nombre"], datos["correo"], datos["contrasena"]
            )
            if administrador.registrar_gerente(gerente):
                self.view.mostrar_mensaje("Agregado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo agregar")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def editar(self):
        numero = self.pedir_id()
        if numero is None:
            return

        gerente = GerenteDAO.obtener_por_id(numero)
        datos = self.view.formulario_editar(gerente)
        if datos is None:
            return
        if not self.validar_correo(datos["correo"], numero):
            return

        try:
            gerente.nombre = datos["nombre"]
            gerente.correo = datos["correo"]

            if GerenteDAO.actualizar(gerente):
                self.view.mostrar_mensaje("Actualizado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo actualizar")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def eliminar(self, administrador):
        numero = self.pedir_id()
        if numero is None:
            return

        for departamento in DepartamentoDAO.obtener_todos():
            if departamento.gerente == numero:
                self.view.mostrar_mensaje(
                    "No puede eliminar un gerente con departamentos asignados"
                )
                return

        if self.view.confirmar_eliminacion():
            if administrador.eliminar_gerente(numero):
                self.view.mostrar_mensaje("Eliminado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo eliminar")
        else:
            self.view.mostrar_mensaje("Operación cancelada")

    def imprimir_uno(self):
        numero = self.pedir_id()
        if numero is not None:
            self.view.mostrar_objeto(GerenteDAO.obtener_por_id(numero))

    def imprimir_todos(self):
        self.view.mostrar_lista(GerenteDAO.obtener_todos())
