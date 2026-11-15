from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO
from models.gerente_dao import GerenteDAO
from models.empleado_dao import EmpleadoDAO
from views.departamento_view import DepartamentoView

class DepartamentoController:
    def __init__(self):
        self.view = DepartamentoView()

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

    def pedir_id(self):
        while True:
            numero = self.view.solicitar_id()
            if numero is None:
                return None
            if DepartamentoDAO.obtener_por_id(numero):
                return numero
            self.view.mostrar_mensaje("Error: Departamento no encontrado")

    def pedir_empleado(self):
        while True:
            numero = self.view.solicitar_id_empleado()
            if numero is None:
                return None
            empleado = EmpleadoDAO.obtener_por_id(numero)
            if empleado:
                return empleado
            self.view.mostrar_mensaje("Error: Empleado no encontrado")

    def validar_gerente(self, id_gerente):
        if id_gerente is not None and GerenteDAO.obtener_por_id(id_gerente) is None:
            self.view.mostrar_mensaje("Error: El gerente no existe")
            return False
        return True

    def agregar(self, administrador):
        datos = self.view.formulario_nuevo()
        if datos is None:
            return
        if not self.validar_gerente(datos["gerente"]):
            return
        try:
            obj = Departamento(datos["nombre"], datos["gerente"])
            if administrador.registrar_departamento(obj):
                self.view.mostrar_mensaje("Agregado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo agregar")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def editar(self):
        id_departamento = self.pedir_id()
        if id_departamento is None:
            return
        obj = DepartamentoDAO.obtener_por_id(id_departamento)
        datos = self.view.formulario_editar(obj)
        if datos is None:
            return
        if not self.validar_gerente(datos["gerente"]):
            return
        try:
            obj.nombre = datos["nombre"]
            obj.gerente = datos["gerente"]
            if DepartamentoDAO.actualizar(obj):
                self.view.mostrar_mensaje("Actualizado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo actualizar")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def eliminar(self, administrador):
        id_departamento = self.pedir_id()
        if id_departamento is None:
            return
        for empleado in EmpleadoDAO.obtener_todos():
            if empleado.departamento and empleado.departamento.id_departamento == id_departamento:
                self.view.mostrar_mensaje("No puede eliminar un departamento con empleados asignados")
                return
        if self.view.confirmar_eliminacion():
            if administrador.eliminar_departamento(id_departamento):
                self.view.mostrar_mensaje("Eliminado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo eliminar")
        else:
            self.view.mostrar_mensaje("Operación cancelada")

    def imprimir_uno(self):
        id_departamento = self.pedir_id()
        if id_departamento is not None:
            self.view.mostrar_objeto(DepartamentoDAO.obtener_por_id(id_departamento))

    def imprimir_todos(self):
        self.view.mostrar_lista(DepartamentoDAO.obtener_todos())

    def asignar_empleado(self):
        self.view.mostrar_titulo("ASIGNAR EMPLEADO A DEPARTAMENTO")
        self.view.mostrar_lista(DepartamentoDAO.obtener_todos())
        id_departamento = self.pedir_id()
        if id_departamento is None:
            return
        departamento = DepartamentoDAO.obtener_por_id(id_departamento)
        self.view.mostrar_empleados(EmpleadoDAO.obtener_todos())
        empleado = self.pedir_empleado()
        if empleado is None:
            return
        if empleado.departamento and empleado.departamento.id_departamento == id_departamento:
            self.view.mostrar_mensaje("El empleado ya pertenece a este departamento")
            return
        empleado.departamento = departamento
        if EmpleadoDAO.actualizar(empleado):
            self.view.mostrar_mensaje("Empleado asignado correctamente")
        else:
            self.view.mostrar_mensaje("No se pudo asignar el empleado")

    def quitar_empleado(self):
        self.view.mostrar_titulo("QUITAR EMPLEADO DE DEPARTAMENTO")
        self.view.mostrar_empleados(EmpleadoDAO.obtener_todos())
        empleado = self.pedir_empleado()
        if empleado is None:
            return
        if empleado.departamento is None:
            self.view.mostrar_mensaje("El empleado no tiene departamento asignado")
            return
        empleado.departamento = None
        if EmpleadoDAO.actualizar(empleado):
            self.view.mostrar_mensaje("Empleado quitado correctamente")
        else:
            self.view.mostrar_mensaje("No se pudo quitar el empleado")

    def ver_empleados(self):
        self.view.mostrar_titulo("EMPLEADOS DE UN DEPARTAMENTO")
        self.view.mostrar_lista(DepartamentoDAO.obtener_todos())
        id_departamento = self.pedir_id()
        if id_departamento is None:
            return
        empleados = []
        for empleado in EmpleadoDAO.obtener_todos():
            if empleado.departamento and empleado.departamento.id_departamento == id_departamento:
                empleados.append(empleado)
        self.view.mostrar_empleados(empleados)
