from views.utils import leer_numero, confirmar
from datetime import datetime

class ProyectoView:
    @staticmethod
    def mostrar_menu():
        print("\n--- GESTIÓN DE PROYECTOS ---")
        print("1.- Agregar proyecto")
        print("2.- Editar proyecto")
        print("3.- Eliminar proyecto")
        print("4.- Imprimir un proyecto")
        print("5.- Imprimir todos los proyectos")
        print("6.- Asignar empleado a proyecto")
        print("7.- Quitar empleado de proyecto")
        print("8.- Ver empleados asignados a un proyecto")
        print("0.- Volver")
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def leer_texto(mensaje, actual=None):
        while True:
            valor = input(mensaje).strip()

            if valor == "0":
                print("Operación cancelada")
                return None

            if not valor and actual is not None:
                return actual

            if valor:
                return valor

            print("Error: Este campo no puede estar vacío")

    @staticmethod
    def leer_fecha(mensaje, actual=None):
        while True:
            fecha = input(mensaje).strip()

            if fecha == "0":
                print("Operación cancelada")
                return None

            if not fecha and actual is not None:
                return actual

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                return fecha
            except ValueError:
                print("Error: Ingrese una fecha válida (AAAA-MM-DD)")

    @staticmethod
    def formulario_nuevo():
        print("\nEscriba 0 para cancelar")

        nombre = ProyectoView.leer_texto("Nombre: ")
        if nombre is None:
            return None

        descripcion = ProyectoView.leer_texto("Descripción: ")
        if descripcion is None:
            return None

        fecha_inicio = ProyectoView.leer_fecha(
            "Fecha de inicio (AAAA-MM-DD): "
        )
        if fecha_inicio is None:
            return None

        return {
            "nombre": nombre,
            "descripcion": descripcion,
            "fecha_inicio": fecha_inicio
        }

    @staticmethod
    def formulario_editar(obj):
        print("\nPresione Enter para mantener el dato actual")
        print("Escriba 0 para cancelar")

        nombre = ProyectoView.leer_texto(
            f"Nombre ({obj.nombre}): ", obj.nombre
        )
        if nombre is None:
            return None

        descripcion = ProyectoView.leer_texto(
            f"Descripción ({obj.descripcion}): ", obj.descripcion
        )
        if descripcion is None:
            return None

        fecha_inicio = ProyectoView.leer_fecha(
            f"Fecha de inicio ({obj.fecha_inicio}): ",
            obj.fecha_inicio
        )
        if fecha_inicio is None:
            return None

        return {
            "nombre": nombre,
            "descripcion": descripcion,
            "fecha_inicio": fecha_inicio
        }

    @staticmethod
    def solicitar_id():
        return leer_numero("Ingrese el ID: ")

    @staticmethod
    def mostrar_objeto(obj):
        print(obj)

    @staticmethod
    def mostrar_lista(objetos):
        if not objetos:
            print("No hay registros")
        for obj in objetos:
            print(obj)

    @staticmethod
    def confirmar_eliminacion():
        return confirmar("¿Desea eliminarlo?")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(mensaje)

