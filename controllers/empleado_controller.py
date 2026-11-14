from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from models.departamento_dao import DepartamentoDAO
from views.empleado_view import EmpleadoView


class EmpleadoController:
    def __init__(self):
        self.view = EmpleadoView()

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
                id_empleado = int(
                    input("ID del empleado (0 para cancelar): ")
                )

                if id_empleado == 0:
                    print("Operación cancelada")
                    return None

                if id_empleado < 0:
                    print("Error: El ID debe ser positivo")
                    continue

                empleado = EmpleadoDAO.obtener_por_id(id_empleado)

                if empleado is None:
                    print("Error: El empleado no existe")
                    continue

                return id_empleado

            except ValueError:
                print("Error: Debe ingresar un número válido")

    def pedir_departamento(self, id_departamento):
        while True:
            if id_departamento == 0:
                return None

            departamento = DepartamentoDAO.obtener_por_id(id_departamento)

            if departamento is not None:
                return departamento

            print("Error: El departamento no existe")

            while True:
                texto = input(
                    "ID departamento (0 sin departamento, C para cancelar): "
                ).strip()

                if texto.lower() == "c":
                    print("Operación cancelada")
                    return False

                try:
                    id_departamento = int(texto)

                    if id_departamento < 0:
                        print("Error: El ID debe ser positivo")
                        continue

                    break

                except ValueError:
                    print("Error: Debe ingresar un número válido")

    def agregar(self):
        try:
            datos = self.view.formulario_nuevo()

            departamento = self.pedir_departamento(
                datos["id_departamento"]
            )

            if departamento is False:
                return

            obj = Empleado(
                datos["nombre"],
                datos["correo"],
                datos["direccion"],
                datos["telefono"],
                datos["fecha_inicio"],
                datos["salario"],
                departamento
            )

            if EmpleadoDAO.crear(obj):
                self.view.mostrar_mensaje("Agregado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo agregar")

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def editar(self):
        id_empleado = self.pedir_id()

        if id_empleado is None:
            return

        obj = EmpleadoDAO.obtener_por_id(id_empleado)

        try:
            datos = self.view.formulario_editar(obj)

            departamento = self.pedir_departamento(
                datos["id_departamento"]
            )

            if departamento is False:
                return

            obj.nombre = datos["nombre"]
            obj.correo = datos["correo"]
            obj.direccion = datos["direccion"]
            obj.telefono = datos["telefono"]
            obj.fecha_inicio = datos["fecha_inicio"]
            obj.salario = datos["salario"]
            obj.departamento = departamento

            if EmpleadoDAO.actualizar(obj):
                self.view.mostrar_mensaje("Actualizado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo actualizar")

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def eliminar(self):
        id_empleado = self.pedir_id()

        if id_empleado is None:
            return

        if self.view.confirmar_eliminacion():
            if EmpleadoDAO.eliminar(id_empleado):
                self.view.mostrar_mensaje("Eliminado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo eliminar")
        else:
            self.view.mostrar_mensaje("Operación cancelada")

    def imprimir_uno(self):
        id_empleado = self.pedir_id()

        if id_empleado is None:
            return

        obj = EmpleadoDAO.obtener_por_id(id_empleado)
        self.view.mostrar_objeto(obj)

    def imprimir_todos(self):
        self.view.mostrar_lista(EmpleadoDAO.obtener_todos())
