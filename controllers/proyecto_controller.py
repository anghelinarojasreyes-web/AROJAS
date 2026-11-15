from models.proyecto import Proyecto
from models.proyecto_dao import ProyectoDAO
from models.empleado_dao import EmpleadoDAO
from views.proyecto_view import ProyectoView

class ProyectoController:
    def __init__(self):
        self.view = ProyectoView()

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
                numero = int(input(f"{mensaje} (0 para cancelar): "))
                if numero == 0:
                    print("Operación cancelada")
                    return None
                if numero > 0 and buscar(numero) is not None:
                    return numero
                print("Error: No se encontró el registro")
            except ValueError:
                print("Error: Ingrese un número válido")

    def agregar(self, administrador):
        try:
            datos = self.view.formulario_nuevo()
            if datos is None:
                return
            obj = Proyecto(datos["nombre"], datos["descripcion"], datos["fecha_inicio"])
            if administrador.registrar_proyecto(obj):
                print("Agregado correctamente")
            else:
                print("No se pudo agregar")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")

    def editar(self):
        id_proyecto = self.pedir_id("ID del proyecto", ProyectoDAO.obtener_por_id)
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
                print("Actualizado correctamente")
            else:
                print("No se pudo actualizar")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")

    def eliminar(self, administrador):
        id_proyecto = self.pedir_id("ID del proyecto", ProyectoDAO.obtener_por_id)
        if id_proyecto is None:
            return

        if self.view.confirmar_eliminacion():
            if administrador.eliminar_proyecto(id_proyecto):
                print("Eliminado correctamente")
            else:
                print("No se pudo eliminar")
        else:
            print("Operación cancelada")

    def imprimir_uno(self):
        id_proyecto = self.pedir_id("ID del proyecto", ProyectoDAO.obtener_por_id)
        if id_proyecto is not None:
            self.view.mostrar_objeto(ProyectoDAO.obtener_por_id(id_proyecto))

    def imprimir_todos(self):
        self.view.mostrar_lista(ProyectoDAO.obtener_todos())

    def asignar_empleado(self):
        id_empleado = self.pedir_id("ID del empleado", EmpleadoDAO.obtener_por_id)
        if id_empleado is None:
            return

        id_proyecto = self.pedir_id("ID del proyecto", ProyectoDAO.obtener_por_id)
        if id_proyecto is None:
            return

        if ProyectoDAO.asignar_empleado(id_empleado, id_proyecto):
            print("Empleado asignado correctamente")
        else:
            print("No se pudo asignar. Puede que ya esté asignado")

    def quitar_empleado(self):
        id_proyecto = self.pedir_id("ID del proyecto", ProyectoDAO.obtener_por_id)
        if id_proyecto is None:
            return

        empleados = ProyectoDAO.ver_empleados(id_proyecto)
        if not empleados:
            print("No hay empleados asignados")
            return

        print("\nEmpleados asignados:")
        for empleado in empleados:
            print(f"ID: {empleado['id_empleado']} - Nombre: {empleado['nombre']}")

        while True:
            try:
                id_empleado = int(input("ID del empleado a quitar (0 para cancelar): "))
                if id_empleado == 0:
                    print("Operación cancelada")
                    return
                if not any(e["id_empleado"] == id_empleado for e in empleados):
                    print("Error: Ese empleado no está asignado")
                    continue
                if ProyectoDAO.quitar_empleado(id_empleado, id_proyecto):
                    print("Empleado quitado correctamente")
                else:
                    print("No se pudo quitar al empleado")
                return
            except ValueError:
                print("Error: Ingrese un número válido")

    def ver_empleados(self):
        id_proyecto = self.pedir_id("ID del proyecto", ProyectoDAO.obtener_por_id)
        if id_proyecto is None:
            return

        empleados = ProyectoDAO.ver_empleados(id_proyecto)
        if empleados:
            for empleado in empleados:
                print(f"ID: {empleado['id_empleado']} - Nombre: {empleado['nombre']}")
        else:
            print("No hay empleados asignados")
