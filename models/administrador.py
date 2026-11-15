from models.usuario import Usuario
from models.empleado_dao import EmpleadoDAO
from models.departamento_dao import DepartamentoDAO
from models.proyecto_dao import ProyectoDAO

class Administrador(Usuario):
    def __init__(self, nombre, correo, contrasena):
        super().__init__(nombre, correo, contrasena)

    def mostrar_rol(self):
        return "Administrador"

    def registrar_administrador(self, administrador):
        from models.administrador_dao import AdministradorDAO
        return AdministradorDAO.crear(administrador)

    def eliminar_administrador(self, id_administrador):
        from models.administrador_dao import AdministradorDAO
        return AdministradorDAO.eliminar(id_administrador)

    def registrar_empleado(self, empleado):
        return EmpleadoDAO.crear(empleado)

    def eliminar_empleado(self, id_empleado):
        return EmpleadoDAO.eliminar(id_empleado)

    def registrar_departamento(self, departamento):
        return DepartamentoDAO.crear(departamento)

    def eliminar_departamento(self, id_departamento):
        return DepartamentoDAO.eliminar(id_departamento)

    def registrar_proyecto(self, proyecto):
        return ProyectoDAO.crear(proyecto)

    def eliminar_proyecto(self, id_proyecto):
        return ProyectoDAO.eliminar(id_proyecto)

    def registrar_gerente(self, gerente):
        from models.gerente_dao import GerenteDAO
        return GerenteDAO.crear(gerente)

    def eliminar_gerente(self, id_gerente):
        from models.gerente_dao import GerenteDAO
        return GerenteDAO.eliminar(id_gerente)
