from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO
from models.gerente_dao import GerenteDAO
from views.departamento_view import DepartamentoView


class DepartamentoController:
    def __init__(self):
        self.view = DepartamentoView()

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

                if buscar(id_obj) is None:
                    print("Error: No se encontró el registro")
                    continue

                return id_obj

            except ValueError:
                print("Error: Debe ingresar un número válido")

    def pedir_gerente(self, actual=None):
        while True:
            texto = input(
                "ID del gerente (0 sin gerente, C para cancelar): "
            ).strip()

            if texto.lower() == "c":
                print("Operación cancelada")
                return False, None

            if texto == "" and actual is not None:
                return True, actual

            try:
                id_gerente = int(texto)

                if id_gerente == 0:
                    return True, None

                if id_gerente < 0:
                    print("Error: El ID debe ser positivo")
                    continue

                if GerenteDAO.obtener_por_id(id_gerente) is None:
                    print("Error: El gerente no existe")
                    continue

                return True, id_gerente

            except ValueError:
                print("Error: Ingrese un ID numérico válido")

    def agregar(self):
        print("\n--- AGREGAR DEPARTAMENTO ---")
        print("Escriba 0 en el nombre para cancelar")

        while True:
            nombre = input("Nombre: ").strip()

            if nombre == "0":
                print("Operación cancelada")
                return

            if nombre:
                break

            print("Error: Debe ingresar un nombre")

        continuar, id_gerente = self.pedir_gerente()

        if not continuar:
            return

        try:
            obj = Departamento(nombre, id_gerente)

            if DepartamentoDAO.crear(obj):
                self.view.mostrar_mensaje("Agregado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo agregar")

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def editar(self):
        id_departamento = self.pedir_id(
            "ID del departamento",
            DepartamentoDAO.obtener_por_id
        )

        if id_departamento is None:
            return

        obj = DepartamentoDAO.obtener_por_id(id_departamento)

        print("\nPresione Enter para mantener el nombre actual")
        print("Escriba 0 para cancelar")

        while True:
            nombre = input(f"Nombre ({obj.nombre}): ").strip()

            if nombre == "0":
                print("Operación cancelada")
                return

            if nombre == "":
                nombre = obj.nombre

            if nombre:
                break

            print("Error: Debe ingresar un nombre")

        print("Presione Enter para mantener el gerente actual")

        continuar, id_gerente = self.pedir_gerente(obj.gerente)

        if not continuar:
            return

        try:
            obj.nombre = nombre
            obj.gerente = id_gerente

            if DepartamentoDAO.actualizar(obj):
                self.view.mostrar_mensaje("Actualizado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo actualizar")

        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error: {e}")

    def eliminar(self):
        id_departamento = self.pedir_id(
            "ID del departamento",
            DepartamentoDAO.obtener_por_id
        )

        if id_departamento is None:
            return

        if self.view.confirmar_eliminacion():
            if DepartamentoDAO.eliminar(id_departamento):
                self.view.mostrar_mensaje("Eliminado correctamente")
            else:
                self.view.mostrar_mensaje("No se pudo eliminar")
        else:
            self.view.mostrar_mensaje("Operación cancelada")

    def imprimir_uno(self):
        id_departamento = self.pedir_id(
            "ID del departamento",
            DepartamentoDAO.obtener_por_id
        )

        if id_departamento is None:
            return

        obj = DepartamentoDAO.obtener_por_id(id_departamento)
        self.view.mostrar_objeto(obj)

    def imprimir_todos(self):
        self.view.mostrar_lista(DepartamentoDAO.obtener_todos())

