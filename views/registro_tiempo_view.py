
from views.utils import leer_numero, confirmar
from datetime import datetime
from models.empleado_dao import EmpleadoDAO
from models.proyecto_dao import ProyectoDAO


class RegistroTiempoView:
    @staticmethod
    def mostrar_menu():
        print("\n--- REGISTROS DE TIEMPO ---")
        print("1.- Agregar registro")
        print("2.- Editar registro")
        print("3.- Eliminar registro")
        print("4.- Imprimir un registro")
        print("5.- Imprimir todos los registros")
        print("0.- Volver")
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def leer_fecha(mensaje, actual=None):
        while True:
            fecha = input(mensaje).strip()

            if fecha == "0":
                return None

            if fecha == "" and actual is not None:
                return actual

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                return fecha
            except ValueError:
                print("Error: Ingrese una fecha válida (AAAA-MM-DD)")

    @staticmethod
    def leer_horas(mensaje, actual=None):
        while True:
            texto = input(mensaje).strip()

            if texto == "0":
                return None

            if texto == "" and actual is not None:
                return actual

            try:
                horas = float(texto)

                if horas > 0:
                    return horas

                print("Error: Las horas deben ser mayores a 0")

            except ValueError:
                print("Error: Ingrese un número válido")

    @staticmethod
    def leer_texto(mensaje, actual=None):
        while True:
            texto = input(mensaje).strip()

            if texto == "0":
                return None

            if texto == "" and actual is not None:
                return actual

            if texto:
                return texto

            print("Error: Este campo no puede estar vacío")

    @staticmethod
    def leer_id(mensaje, buscar, actual=None):
        while True:
            texto = input(mensaje).strip()

            if texto == "0":
                return None

            if texto == "" and actual is not None:
                return actual

            try:
                id_obj = int(texto)

                if id_obj < 0:
                    print("Error: El ID debe ser positivo")
                    continue

                if buscar(id_obj) is None:
                    print("Error: El registro no existe")
                    continue

                return id_obj

            except ValueError:
                print("Error: Ingrese un ID numérico válido")

    @staticmethod
    def formulario_nuevo():
        print("\nEscriba 0 para cancelar")

        fecha = RegistroTiempoView.leer_fecha(
            "Fecha (AAAA-MM-DD): "
        )
        if fecha is None:
            return None

        horas = RegistroTiempoView.leer_horas(
            "Horas trabajadas: "
        )
        if horas is None:
            return None

        descripcion = RegistroTiempoView.leer_texto(
            "Descripción: "
        )
        if descripcion is None:
            return None

        id_empleado = RegistroTiempoView.leer_id(
            "ID del empleado: ",
            EmpleadoDAO.obtener_por_id
        )
        if id_empleado is None:
            return None

        id_proyecto = RegistroTiempoView.leer_id(
            "ID del proyecto: ",
            ProyectoDAO.obtener_por_id
        )
        if id_proyecto is None:
            return None

        return {
            "fecha": fecha,
            "horas": horas,
            "descripcion": descripcion,
            "id_empleado": id_empleado,
            "id_proyecto": id_proyecto
        }

    @staticmethod
    def formulario_editar(obj):
        print("\nPresione Enter para mantener el dato actual")
        print("Escriba 0 para cancelar")

        fecha = RegistroTiempoView.leer_fecha(
            f"Fecha ({obj.fecha}): ", obj.fecha
        )
        if fecha is None:
            return None

        horas = RegistroTiempoView.leer_horas(
            f"Horas ({obj.horas_trabajadas}): ",
            obj.horas_trabajadas
        )
        if horas is None:
            return None

        descripcion = RegistroTiempoView.leer_texto(
            f"Descripción ({obj.descripcion}): ",
            obj.descripcion
        )
        if descripcion is None:
            return None

        id_empleado = RegistroTiempoView.leer_id(
            f"ID del empleado ({obj.empleado.id_empleado}): ",
            EmpleadoDAO.obtener_por_id,
            obj.empleado.id_empleado
        )
        if id_empleado is None:
            return None

        id_proyecto = RegistroTiempoView.leer_id(
            f"ID del proyecto ({obj.proyecto.id_proyecto}): ",
            ProyectoDAO.obtener_por_id,
            obj.proyecto.id_proyecto
        )
        if id_proyecto is None:
            return None

        return {
            "fecha": fecha,
            "horas": horas,
            "descripcion": descripcion,
            "id_empleado": id_empleado,
            "id_proyecto": id_proyecto
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