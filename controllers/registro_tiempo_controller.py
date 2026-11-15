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
                numero = int(input("ID del registro (0 para cancelar): "))
                if numero == 0:
                    print("Operación cancelada")
                    return None
                if numero > 0 and RegistroTiempoDAO.obtener_por_id(numero):
                    return numero
                print("Error: El registro no existe")
            except ValueError:
                print("Error: Ingrese un número válido")

    def agregar(self):
        try:
            datos = self.view.formulario_nuevo()
            if datos is None:
                return

            empleado = EmpleadoDAO.obtener_por_id(datos["id_empleado"])
            proyecto = ProyectoDAO.obtener_por_id(datos["id_proyecto"])

            if empleado is None or proyecto is None:
                print("Error: Empleado o proyecto no encontrado")
                return

            obj = RegistroTiempo(
                datos["fecha"], datos["horas"], datos["descripcion"],
                empleado, proyecto
            )

            if RegistroTiempoDAO.crear(obj):
                print("Agregado correctamente")
            else:
                print("No se pudo agregar")

        except (ValueError, TypeError) as e:
            print(f"Error: {e}")

    def registrar_horas(self, empleado):
        proyectos = ProyectoDAO.obtener_por_empleado(empleado.id_empleado)

        if not proyectos:
            print("No tiene proyectos asignados")
            return

        print("\n--- REGISTRAR HORAS TRABAJADAS ---")
        print("Proyectos asignados:")
        for proyecto in proyectos:
            print(proyecto)

        while True:
            texto = input("ID del proyecto (C para cancelar): ").strip()

            if texto.upper() == "C":
                print("Operación cancelada")
                return

            try:
                id_proyecto = int(texto)
                proyecto = None

                for p in proyectos:
                    if p.id_proyecto == id_proyecto:
                        proyecto = p
                        break

                if proyecto is not None:
                    break

                print("Error: El proyecto no está asignado a usted")

            except ValueError:
                print("Error: Ingrese un ID válido")

        print("Escriba C para cancelar")

        fecha = self.view.leer_fecha("Fecha (AAAA-MM-DD): ")
        if fecha is None:
            return

        horas = self.view.leer_horas("Horas trabajadas: ")
        if horas is None:
            return

        descripcion = self.view.leer_texto("Descripción: ")
        if descripcion is None:
            return

        try:
            registro = RegistroTiempo(
                fecha, horas, descripcion, empleado, proyecto
            )

            if RegistroTiempoDAO.crear(registro):
                print("Horas registradas correctamente")
            else:
                print("No se pudieron registrar las horas")

        except (ValueError, TypeError) as e:
            print(f"Error: {e}")

    def editar(self):
        id_registro = self.pedir_id()
        if id_registro is None:
            return

        obj = RegistroTiempoDAO.obtener_por_id(id_registro)

        try:
            datos = self.view.formulario_editar(obj)
            if datos is None:
                return

            empleado = EmpleadoDAO.obtener_por_id(datos["id_empleado"])
            proyecto = ProyectoDAO.obtener_por_id(datos["id_proyecto"])

            if empleado is None or proyecto is None:
                print("Error: Empleado o proyecto no encontrado")
                return

            obj.fecha = datos["fecha"]
            obj.horas_trabajadas = datos["horas"]
            obj.descripcion = datos["descripcion"]
            obj.empleado = empleado
            obj.proyecto = proyecto

            if RegistroTiempoDAO.actualizar(obj):
                print("Actualizado correctamente")
            else:
                print("No se pudo actualizar")

        except (ValueError, TypeError) as e:
            print(f"Error: {e}")

    def eliminar(self):
        id_registro = self.pedir_id()
        if id_registro is None:
            return

        if self.view.confirmar_eliminacion():
            if RegistroTiempoDAO.eliminar(id_registro):
                print("Eliminado correctamente")
            else:
                print("No se pudo eliminar")
        else:
            print("Operación cancelada")

    def imprimir_uno(self):
        id_registro = self.pedir_id()
        if id_registro is not None:
            self.view.mostrar_objeto(
                RegistroTiempoDAO.obtener_por_id(id_registro)
            )

    def imprimir_todos(self):
        self.view.mostrar_lista(RegistroTiempoDAO.obtener_todos())
