from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from models.departamento_dao import DepartamentoDAO
from views.empleado_view import EmpleadoView

class EmpleadoController:
    def __init__(self):
        self.view = EmpleadoView()

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

    def pedir_id(self, gerente=None):
        while True:
            try:
                id_empleado = int(input("ID del empleado (0 para cancelar): "))
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
                if gerente and not gerente.puede_editar_empleado(empleado):
                    print("No tiene permiso para editar este empleado")
                    return None
                return id_empleado
            except ValueError:
                print("Error: Debe ingresar un número válido")

    def pedir_departamento(self, id_departamento):
        while True:
            if id_departamento == 0:
                return None
            if id_departamento > 0:
                departamento = DepartamentoDAO.obtener_por_id(id_departamento)
                if departamento is not None:
                    return departamento
                print("Error: El departamento no existe")
            else:
                print("Error: El ID debe ser positivo")
            texto = input("ID departamento (0 sin departamento, C cancelar): ").strip()
            if texto.upper() == "C":
                print("Operación cancelada")
                return False
            try:
                id_departamento = int(texto)
            except ValueError:
                print("Error: Debe ingresar un número válido")
                id_departamento = -1

    def agregar(self, administrador):
        try:
            datos = self.view.formulario_nuevo()
            if datos is None:
                return
            departamento = self.pedir_departamento(datos["id_departamento"])
            if departamento is False:
                return
            obj = Empleado(
                datos["nombre"], datos["correo"], datos["direccion"],
                datos["telefono"], datos["fecha_inicio"], datos["salario"],
                departamento, contrasena=datos["contrasena"]
            )
            if administrador.registrar_empleado(obj):
                self.view.mostrar_mensaje("Agregado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo agregar")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def editar(self, gerente=None):
        id_empleado = self.pedir_id(gerente)
        if id_empleado is None:
            return
        obj = EmpleadoDAO.obtener_por_id(id_empleado)
        if obj is None:
            self.view.mostrar_mensaje("El empleado no existe")
            return
        try:
            datos = self.view.formulario_editar(obj, gerente)
            if datos is None:
                return
            if gerente:
                if not gerente.puede_editar_empleado(obj):
                    self.view.mostrar_mensaje("No tiene permiso para editar este empleado")
                    return
                departamento = obj.departamento
            else:
                departamento = self.pedir_departamento(datos["id_departamento"])
                if departamento is False:
                    return
            empleado_actualizado = Empleado(
                datos["nombre"], datos["correo"], datos["direccion"],
                datos["telefono"], datos["fecha_inicio"], datos["salario"],
                departamento, id_empleado, None
            )
            if EmpleadoDAO.actualizar(empleado_actualizado):
                self.view.mostrar_mensaje("Actualizado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo actualizar")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def eliminar(self, administrador):
        id_empleado = self.pedir_id()
        if id_empleado is None:
            return
        if self.view.confirmar_eliminacion():
            if administrador.eliminar_empleado(id_empleado):
                self.view.mostrar_mensaje("Eliminado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo eliminar")
        else:
            self.view.mostrar_mensaje("Operación cancelada")

    def imprimir_uno(self):
        id_empleado = self.pedir_id()
        if id_empleado is not None:
            empleado = EmpleadoDAO.obtener_por_id(id_empleado)
            if empleado is not None:
                self.view.mostrar_objeto(empleado)

    def imprimir_todos(self):
        self.view.mostrar_lista(EmpleadoDAO.obtener_todos())
