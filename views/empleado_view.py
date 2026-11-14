from views.utils import leer_numero, confirmar
from datetime import datetime

class EmpleadoView:
    @staticmethod
    def mostrar_menu():
        print("\n--- GESTIÓN DE EMPLEADOS ---")
        print("1.- Agregar empleado")
        print("2.- Editar empleado")
        print("3.- Eliminar empleado")
        print("4.- Imprimir un empleado")
        print("5.- Imprimir todos los empleados")
        print("0.- Volver")
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def leer_texto(mensaje, actual=None):
        while True:
            valor = input(mensaje).strip()

            if not valor and actual is not None:
                return actual

            if valor:
                return valor

            print("Error: Este campo no puede estar vacío")

    @staticmethod
    def leer_correo(mensaje, actual=None):
        while True:
            correo = input(mensaje).strip()

            if not correo and actual is not None:
                return actual

            if "@" in correo and "." in correo.split("@")[-1] and " " not in correo:
                return correo

            print("Error: Ingrese un correo válido")

    @staticmethod
    def leer_telefono(mensaje, actual=None):
        while True:
            telefono = input(mensaje).strip()

            if not telefono and actual is not None:
                return actual

            if telefono.isdigit() and len(telefono) == 9:
                return telefono

            print("Error: El teléfono debe tener 9 dígitos numéricos")

    @staticmethod
    def leer_fecha(mensaje, actual=None):
        while True:
            fecha = input(mensaje).strip()

            if not fecha and actual is not None:
                return actual

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                return fecha
            except ValueError:
                print("Error: Ingrese una fecha válida (AAAA-MM-DD)")

    @staticmethod
    def leer_salario(mensaje, actual=None):
        while True:
            valor = input(mensaje).strip()

            if not valor and actual is not None:
                return actual

            try:
                salario = float(valor)

                if salario >= 0:
                    return salario

                print("Error: El salario no puede ser negativo")

            except ValueError:
                print("Error: Ingrese un salario numérico")

    @staticmethod
    def leer_departamento(mensaje, actual=None):
        while True:
            valor = input(mensaje).strip()

            if not valor and actual is not None:
                return actual

            try:
                numero = int(valor)

                if numero >= 0:
                    return numero

                print("Error: El ID no puede ser negativo")

            except ValueError:
                print("Error: Ingrese un número válido")

    @staticmethod
    def formulario_nuevo():
        nombre = EmpleadoView.leer_texto("Nombre: ")
        correo = EmpleadoView.leer_correo("Correo: ")
        direccion = EmpleadoView.leer_texto("Dirección: ")
        telefono = EmpleadoView.leer_telefono("Teléfono (9 dígitos): ")
        fecha_inicio = EmpleadoView.leer_fecha("Fecha de inicio (AAAA-MM-DD): ")
        salario = EmpleadoView.leer_salario("Salario: ")
        id_depto = EmpleadoView.leer_departamento(
            "ID departamento (0 si no tiene): "
        )

        return {
            "nombre": nombre,
            "correo": correo,
            "direccion": direccion,
            "telefono": telefono,
            "fecha_inicio": fecha_inicio,
            "salario": salario,
            "id_departamento": id_depto
        }

    @staticmethod
    def formulario_editar(obj):
        nombre = EmpleadoView.leer_texto(
            f"Nombre ({obj.nombre}): ", obj.nombre
        )
        correo = EmpleadoView.leer_correo(
            f"Correo ({obj.correo}): ", obj.correo
        )
        direccion = EmpleadoView.leer_texto(
            f"Dirección ({obj.direccion}): ", obj.direccion
        )
        telefono = EmpleadoView.leer_telefono(
            f"Teléfono ({obj.telefono}): ", obj.telefono
        )
        fecha_inicio = EmpleadoView.leer_fecha(
            f"Fecha de inicio ({obj.fecha_inicio}): ", obj.fecha_inicio
        )
        salario = EmpleadoView.leer_salario(
            f"Salario ({obj.salario}): ", obj.salario
        )

        id_actual = obj.departamento.id_departamento if obj.departamento else 0
        id_departamento = EmpleadoView.leer_departamento(
            f"ID departamento ({id_actual}): ", id_actual
        )

        return {
            "nombre": nombre,
            "correo": correo,
            "direccion": direccion,
            "telefono": telefono,
            "fecha_inicio": fecha_inicio,
            "salario": salario,
            "id_departamento": id_departamento
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

