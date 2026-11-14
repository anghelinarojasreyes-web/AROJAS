from models.registro_tiempo import RegistroTiempo
from models.registro_tiempo_dao import RegistroTiempoDAO
from models.empleado_dao import EmpleadoDAO
from models.proyecto_dao import ProyectoDAO
from views.registro_tiempo_view import RegistroTiempoView


class RegistroTiempoController:
    def __init__(self):
        self.view = RegistroTiempoView()

    def ejecutar(self):
        while True:
            opcion = self.view.mostrar_menu()

            if opcion == 1:
                self.agregar()
            elif opcion == 2:
                self.editar()
            elif opcion == 3:
                self.eliminar()
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
            try:
                id_registro = int(
                    input("ID del registro (0 para cancelar): ")
                )

                if id_registro == 0:
                    self.view.mostrar_mensaje("Operación cancelada")
                    return None

                if id_registro < 0:
                    self.view.mostrar_mensaje(
                        "Error: El ID debe ser positivo"
                    )
                    continue

                registro = RegistroTiempoDAO.obtener_por_id(id_registro)

                if registro is None:
                    self.view.mostrar_mensaje(
                        "Error: El registro no existe"
                    )
                    continue

                return id_registro

            except ValueError:
                self.view.mostrar_mensaje(
                    "Error: Ingrese un número válido"
                )

    def agregar(self):
        try:
            datos = self.view.formulario_nuevo()

            if datos is None:
                self.view.mostrar_mensaje("Operación cancelada")
                return

            empleado = EmpleadoDAO.obtener_por_id(
                datos["id_empleado"]
            )
            proyecto = ProyectoDAO.obtener_por_id(
                datos["id_proyecto"]
            )

            if empleado is None or proyecto is None:
                self.view.mostrar_mensaje(
                    "Error: Empleado o proyecto no encontrado"
                )
                return

            obj = RegistroTiempo(
                datos["fecha"],
                datos["horas"],
                datos["descripcion"],
                empleado,
                proyecto
            )

            if RegistroTiempoDAO.crear(obj):
                self.view.mostrar_mensaje("Agregado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo agregar")

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def editar(self):
        id_registro = self.pedir_id()

        if id_registro is None:
            return

        obj = RegistroTiempoDAO.obtener_por_id(id_registro)

        try:
            datos = self.view.formulario_editar(obj)

            if datos is None:
                self.view.mostrar_mensaje("Operación cancelada")
                return

            empleado = EmpleadoDAO.obtener_por_id(
                datos["id_empleado"]
            )
            proyecto = ProyectoDAO.obtener_por_id(
                datos["id_proyecto"]
            )

            if empleado is None or proyecto is None:
                self.view.mostrar_mensaje(
                    "Error: Empleado o proyecto no encontrado"
                )
                return

            obj.fecha = datos["fecha"]
            obj.horas_trabajadas = datos["horas"]
            obj.descripcion = datos["descripcion"]
            obj.empleado = empleado
            obj.proyecto = proyecto

            if RegistroTiempoDAO.actualizar(obj):
                self.view.mostrar_mensaje("Actualizado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo actualizar")

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def eliminar(self):
        id_registro = self.pedir_id()

        if id_registro is None:
            return

        if self.view.confirmar_eliminacion():
            if RegistroTiempoDAO.eliminar(id_registro):
                self.view.mostrar_mensaje("Eliminado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo eliminar")
        else:
            self.view.mostrar_mensaje("Operación cancelada")

    def imprimir_uno(self):
        id_registro = self.pedir_id()

        if id_registro is None:
            return

        obj = RegistroTiempoDAO.obtener_por_id(id_registro)

        if obj:
            self.view.mostrar_objeto(obj)
        else:
            self.view.mostrar_mensaje("No encontrado")

    def imprimir_todos(self):
        self.view.mostrar_lista(
            RegistroTiempoDAO.obtener_todos()
        )

