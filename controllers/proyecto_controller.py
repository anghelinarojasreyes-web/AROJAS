from models.proyecto import Proyecto
from models.proyecto_dao import ProyectoDAO
from views.proyecto_view import ProyectoView
from models.empleado_dao import EmpleadoDAO


class ProyectoController:
    def __init__(self):
        self.view = ProyectoView()

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
            elif opcion == 6:
                self.asignar_empleado()
            elif opcion == 7:
                self.quitar_empleado()
            elif opcion == 8:
                self.ver_empleados()
            elif opcion == 0:
                break
            else:
                self.view.mostrar_mensaje("Opción no válida")

    def pedir_id(self, mensaje, buscar):
        while True:
            try:
                id_obj = int(input(f"{mensaje} (0 para cancelar): "))

                if id_obj == 0:
                    print("Operación cancelada")
                    return None

                if id_obj < 0:
                    print("Error: El ID debe ser positivo")
                    continue

                objeto = buscar(id_obj)

                if objeto is None:
                    print("Error: No se encontró el registro")
                    continue

                return id_obj

            except ValueError:
                print("Error: Debe ingresar un número válido")

    def agregar(self):
        try:
            datos = self.view.formulario_nuevo()

            if datos is None:
                return

            obj = Proyecto(
                datos["nombre"],
                datos["descripcion"],
                datos["fecha_inicio"]
            )

            if ProyectoDAO.crear(obj):
                self.view.mostrar_mensaje("Agregado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo agregar")

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def editar(self):
        id_proyecto = self.pedir_id(
            "ID del proyecto",
            ProyectoDAO.obtener_por_id
        )

        if id_proyecto is None:
            return

        obj = ProyectoDAO.obtener_por_id(id_proyecto)

        try:
            datos = self.view.formulario_editar(obj)

            if datos is None:
                return

            obj.nombre = datos["nombre"]
            obj.descripcion = datos["descripcion"]
            obj.fecha_inicio = datos["fecha_inicio"]

            if ProyectoDAO.actualizar(obj):
                self.view.mostrar_mensaje("Actualizado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo actualizar")

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def eliminar(self):
        id_proyecto = self.pedir_id(
            "ID del proyecto",
            ProyectoDAO.obtener_por_id
        )

        if id_proyecto is None:
            return

        if self.view.confirmar_eliminacion():
            if ProyectoDAO.eliminar(id_proyecto):
                self.view.mostrar_mensaje("Eliminado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo eliminar")
        else:
            self.view.mostrar_mensaje("Operación cancelada")

    def imprimir_uno(self):
        id_proyecto = self.pedir_id(
            "ID del proyecto",
            ProyectoDAO.obtener_por_id
        )

        if id_proyecto is None:
            return

        obj = ProyectoDAO.obtener_por_id(id_proyecto)
        self.view.mostrar_objeto(obj)

    def imprimir_todos(self):
        self.view.mostrar_lista(ProyectoDAO.obtener_todos())

    def asignar_empleado(self):
        id_empleado = self.pedir_id(
            "ID del empleado",
            EmpleadoDAO.obtener_por_id
        )

        if id_empleado is None:
            return

        id_proyecto = self.pedir_id(
            "ID del proyecto",
            ProyectoDAO.obtener_por_id
        )

        if id_proyecto is None:
            return

        if ProyectoDAO.asignar_empleado(id_empleado, id_proyecto):
            self.view.mostrar_mensaje("Empleado asignado correctamente")
        else:
            self.view.mostrar_mensaje(
                "No se pudo asignar. Puede que ya esté asignado"
            )

    def quitar_empleado(self):
        id_proyecto = self.pedir_id(
            "ID del proyecto",
            ProyectoDAO.obtener_por_id
        )

        if id_proyecto is None:
            return

        while True:
            empleados = ProyectoDAO.ver_empleados(id_proyecto)

            if not empleados:
                self.view.mostrar_mensaje(
                    "No hay empleados asignados a este proyecto"
                )
                return

            print("\nEmpleados asignados:")
            for empleado in empleados:
                print(
                    f"ID: {empleado['id_empleado']} - "
                    f"Nombre: {empleado['nombre']}"
                )

            try:
                id_empleado = int(
                    input("ID del empleado a quitar (0 para cancelar): ")
                )

                if id_empleado == 0:
                    print("Operación cancelada")
                    return

                if not any(
                    empleado["id_empleado"] == id_empleado
                    for empleado in empleados
                ):
                    print("Error: Ese empleado no está asignado")
                    continue

                if ProyectoDAO.quitar_empleado(
                    id_empleado, id_proyecto
                ):
                    self.view.mostrar_mensaje(
                        "Empleado quitado correctamente"
                    )
                else:
                    self.view.mostrar_mensaje(
                        "No se pudo quitar al empleado"
                    )

                return

            except ValueError:
                print("Error: Debe ingresar un número válido")

    def ver_empleados(self):
        id_proyecto = self.pedir_id(
            "ID del proyecto",
            ProyectoDAO.obtener_por_id
        )

        if id_proyecto is None:
            return

        empleados = ProyectoDAO.ver_empleados(id_proyecto)

        if empleados:
            for empleado in empleados:
                print(
                    f"ID: {empleado['id_empleado']} - "
                    f"Nombre: {empleado['nombre']}"
                )
        else:
            self.view.mostrar_mensaje("No hay empleados asignados")
