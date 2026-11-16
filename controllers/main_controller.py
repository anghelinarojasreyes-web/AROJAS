import os
import time
from getpass import getpass
from views.main_view import MainView
from controllers.empleado_controller import EmpleadoController
from controllers.departamento_controller import DepartamentoController
from controllers.proyecto_controller import ProyectoController
from controllers.registro_tiempo_controller import RegistroTiempoController
from controllers.gerente_controller import GerenteController
from controllers.administrador_controller import AdministradorController
from controllers.clima_controller import ClimaController
from models.administrador_dao import AdministradorDAO
from models.gerente_dao import GerenteDAO
from models.departamento_dao import DepartamentoDAO
from models.proyecto_dao import ProyectoDAO
from models.empleado_dao import EmpleadoDAO
from models.registro_tiempo_dao import RegistroTiempoDAO

class MainController:
    def __init__(self):
        self.view = MainView()
        self.empleado_controller = EmpleadoController()
        self.departamento_controller = DepartamentoController()
        self.proyecto_controller = ProyectoController()
        self.registro_tiempo_controller = RegistroTiempoController()
        self.gerente_controller = GerenteController()
        self.administrador_controller = AdministradorController()
        self.clima_controller = ClimaController()
        self.intentos_por_correo = {}
        self.bloqueos_por_correo = {}

    def mostrar_bienvenida(self, usuario):
        print(f"\nBienvenido, {usuario.nombre}")
        print(f"Rol: {usuario.mostrar_rol()}")

    def leer_contrasena(self):
        if os.name != "nt":
            return getpass("Contraseña (0 para volver): ")

        import msvcrt
        print("Contraseña (0 para volver): ", end="", flush=True)
        caracteres = []

        while True:
            tecla = msvcrt.getwch()

            if tecla == "\r":
                print()
                return "".join(caracteres)
            elif tecla == "\x03":
                raise KeyboardInterrupt
            elif tecla == "\b":
                if caracteres:
                    caracteres.pop()
                    print("\b \b", end="", flush=True)
            elif tecla in ("\x00", "\xe0"):
                msvcrt.getwch()
            elif tecla.isprintable():
                caracteres.append(tecla)
                print("*", end="", flush=True)

    def iniciar_sesion(self):
        while True:
            print("\n--- INICIO DE SESIÓN ---")
            correo = input("Correo (0 para volver): ").strip()

            if correo == "0":
                return

            administrador = AdministradorDAO.obtener_por_correo(correo)
            gerente = GerenteDAO.obtener_por_correo(correo)
            empleado = EmpleadoDAO.obtener_por_correo(correo)

            correo_clave = correo.lower()
            restante = self.bloqueos_por_correo.get(correo_clave, 0) - time.monotonic()

            if restante > 0:
                print(f"Cuenta bloqueada. Espere {int(restante) + 1} segundos")
                continue

            if correo_clave in self.bloqueos_por_correo:
                del self.bloqueos_por_correo[correo_clave]
                self.intentos_por_correo[correo_clave] = 0

            contrasena = self.leer_contrasena()

            if contrasena == "0":
                return

            if administrador and administrador.verificar_contrasena(contrasena):
                self.intentos_por_correo.pop(correo_clave, None)
                self.mostrar_bienvenida(administrador)
                self.menu_administrador(administrador)
                return

            if gerente and gerente.verificar_contrasena(contrasena):
                self.intentos_por_correo.pop(correo_clave, None)
                self.mostrar_bienvenida(gerente)
                self.menu_gerente(gerente)
                return

            if empleado and empleado.verificar_contrasena(contrasena):
                self.intentos_por_correo.pop(correo_clave, None)
                self.mostrar_bienvenida(empleado)
                self.menu_empleado(empleado)
                return

            intentos = self.intentos_por_correo.get(correo_clave, 0) + 1
            self.intentos_por_correo[correo_clave] = intentos

            print("Correo o contraseña incorrecta")

            if intentos >= 3:
                self.bloqueos_por_correo[correo_clave] = time.monotonic() + 30
                print("Se alcanzó el máximo de 3 intentos")
                print("Esta cuenta quedó bloqueada por 30 segundos")
            else:
                print(f"Intentos restantes: {3 - intentos}")

    def menu_administrador(self, administrador):
        while True:
            print("\n--- PANEL DE ADMINISTRADOR ---")
            print(f"Administrador: {administrador.nombre}")
            print("1.- Gestión de Empleados")
            print("2.- Gestión de Departamentos")
            print("3.- Gestión de Proyectos")
            print("4.- Gestión de Registros de Tiempo")
            print("5.- Gestión de Gerentes")
            print("6.- Gestión de Administradores")
            print("7.- Consultar clima")
            print("0.- Cerrar sesión")

            try:
                opcion = int(input("Seleccione una opción: "))
            except ValueError:
                print("Ingrese un número válido")
                continue

            if opcion == 1:
                self.empleado_controller.ejecutar(administrador)
            elif opcion == 2:
                self.departamento_controller.ejecutar(administrador)
            elif opcion == 3:
                self.proyecto_controller.ejecutar(administrador)
            elif opcion == 4:
                self.registro_tiempo_controller.ejecutar()
            elif opcion == 5:
                self.gerente_controller.ejecutar(administrador)
            elif opcion == 6:
                self.administrador_controller.ejecutar(administrador)
            elif opcion == 7:
                self.clima_controller.consultar()
            elif opcion == 0:
                print("Sesión cerrada")
                break
            else:
                print("Opción no válida")

    def menu_gerente(self, gerente):
        while True:
            print("\n--- PANEL DE GERENTE ---")
            print(f"Gerente: {gerente.nombre}")
            print("1.- Consultar datos personales")
            print("2.- Consultar departamentos asignados")
            print("3.- Consultar empleados")
            print("4.- Editar empleado")
            print("5.- Consultar proyectos")
            print("6.- Consultar registros de tiempo")
            print("7.- Consultar clima")
            print("0.- Cerrar sesión")

            try:
                opcion = int(input("Seleccione una opción: "))
            except ValueError:
                print("Ingrese un número válido")
                continue

            if opcion == 1:
                print(f"\nNombre: {gerente.nombre}")
                print(f"Correo: {gerente.correo}")
                print(f"ID: {gerente.id_gerente}")
                print("\nDepartamentos que dirige:")

                encontrado = False

                for departamento in DepartamentoDAO.obtener_todos():
                    if departamento.gerente == gerente.id_gerente:
                        print(departamento.nombre)
                        encontrado = True

                if not encontrado:
                    print("No tiene departamentos asignados")

            elif opcion == 2:
                encontrado = False

                for departamento in DepartamentoDAO.obtener_todos():
                    if departamento.gerente == gerente.id_gerente:
                        print(departamento)
                        encontrado = True

                if not encontrado:
                    print("No tiene departamentos asignados")

            elif opcion == 3:
                encontrado = False

                for empleado in EmpleadoDAO.obtener_todos():
                    if gerente.puede_editar_empleado(empleado):
                        print(empleado)
                        encontrado = True

                if not encontrado:
                    print("No hay empleados en sus departamentos")

            elif opcion == 4:
                self.empleado_controller.editar(gerente)

            elif opcion == 5:
                proyectos_vistos = set()

                for empleado in EmpleadoDAO.obtener_todos():
                    if gerente.puede_editar_empleado(empleado):
                        proyectos = ProyectoDAO.obtener_por_empleado(
                            empleado.id_empleado
                        )

                        for proyecto in proyectos:
                            if proyecto.id_proyecto not in proyectos_vistos:
                                print(proyecto)
                                proyectos_vistos.add(proyecto.id_proyecto)

                if not proyectos_vistos:
                    print("No hay proyectos asignados")

            elif opcion == 6:
                encontrado = False

                for empleado in EmpleadoDAO.obtener_todos():
                    if gerente.puede_editar_empleado(empleado):
                        registros = RegistroTiempoDAO.obtener_por_empleado(
                            empleado.id_empleado
                        )

                        for registro in registros:
                            print(registro)
                            encontrado = True

                if not encontrado:
                    print("No hay registros de tiempo")

            elif opcion == 7:
                self.clima_controller.consultar()

            elif opcion == 0:
                print("Sesión cerrada")
                break

            else:
                print("Opción no válida")

    def menu_empleado(self, empleado):
        while True:
            print("\n--- PANEL DE EMPLEADO ---")
            print(f"Empleado: {empleado.nombre}")
            print("1.- Consultar datos personales")
            print("2.- Consultar departamento")
            print("3.- Consultar compañeros")
            print("4.- Consultar gerente")
            print("5.- Consultar proyectos")
            print("6.- Consultar registros de tiempo")
            print("7.- Registrar horas trabajadas")
            print("8.- Consultar clima")
            print("0.- Cerrar sesión")

            try:
                opcion = int(input("Seleccione una opción: "))
            except ValueError:
                print("Ingrese un número válido")
                continue

            if opcion == 1:
                print(empleado)

            elif opcion == 2:
                if empleado.departamento:
                    print(empleado.departamento)
                else:
                    print("No tiene departamento asignado")

            elif opcion == 3:
                if empleado.departamento:
                    encontrados = False

                    for companero in EmpleadoDAO.obtener_todos():
                        if (
                            companero.departamento
                            and companero.id_empleado != empleado.id_empleado
                        ):
                            if (
                                companero.departamento.id_departamento
                                == empleado.departamento.id_departamento
                            ):
                                print(
                                    f"{companero.nombre} | {companero.correo}"
                                )
                                encontrados = True

                    if not encontrados:
                        print("No hay compañeros registrados")
                else:
                    print("No tiene departamento asignado")

            elif opcion == 4:
                if empleado.departamento and empleado.departamento.gerente:
                    gerente = GerenteDAO.obtener_por_id(
                        empleado.departamento.gerente
                    )

                    if gerente:
                        print(
                            f"Nombre: {gerente.nombre} | "
                            f"Correo: {gerente.correo}"
                        )
                    else:
                        print("No se encontró al gerente")
                else:
                    print("No tiene gerente asignado")

            elif opcion == 5:
                proyectos = ProyectoDAO.obtener_por_empleado(
                    empleado.id_empleado
                )

                if proyectos:
                    for proyecto in proyectos:
                        print(proyecto)
                else:
                    print("No tiene proyectos asignados")

            elif opcion == 6:
                registros = RegistroTiempoDAO.obtener_por_empleado(
                    empleado.id_empleado
                )

                if registros:
                    for registro in registros:
                        print(registro)
                else:
                    print("No tiene registros de tiempo")

            elif opcion == 7:
                self.registro_tiempo_controller.registrar_horas(empleado)

            elif opcion == 8:
                self.clima_controller.consultar()

            elif opcion == 0:
                print("Sesión cerrada")
                break

            else:
                print("Opción no válida")

    def ejecutar(self):
        while True:
            opcion = self.view.mostrar_menu()

            if opcion == 1:
                self.iniciar_sesion()
            elif opcion == 0:
                print("Hasta luego")
                break
            else:
                print("Opción no válida")
