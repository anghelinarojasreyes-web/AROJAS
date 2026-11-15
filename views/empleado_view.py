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
            if valor.upper() == "C":
                raise ValueError("Operación cancelada")
            if not valor and actual is not None:
                return actual
            if valor:
                return valor
            print("Error: Campo obligatorio")

    @staticmethod
    def leer_correo(mensaje, actual=None):
        while True:
            correo = EmpleadoView.leer_texto(mensaje, actual)
            if "@" in correo and "." in correo.split("@")[-1] and " " not in correo:
                return correo
            print("Error: Correo inválido")

    @staticmethod
    def leer_telefono(mensaje, actual=None):
        while True:
            telefono = EmpleadoView.leer_texto(mensaje, actual)
            if telefono.isdigit() and len(telefono) == 9:
                return telefono
            print("Error: Debe tener 9 dígitos")

    @staticmethod
    def leer_fecha(mensaje, actual=None):
        while True:
            fecha = EmpleadoView.leer_texto(mensaje, actual)
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                return fecha
            except ValueError:
                print("Error: Fecha inválida (AAAA-MM-DD)")

    @staticmethod
    def leer_salario(mensaje, actual=None):
        while True:
            valor = EmpleadoView.leer_texto(mensaje, str(actual) if actual is not None else None)
            try:
                salario = float(valor)
                if salario >= 0:
                    return salario
            except ValueError:
                pass
            print("Error: Salario inválido")

    @staticmethod
    def leer_departamento(mensaje, actual=None):
        while True:
            valor = EmpleadoView.leer_texto(mensaje, str(actual) if actual is not None else None)
            if valor.isdigit():
                return int(valor)
            print("Error: ID inválido")

    @staticmethod
    def leer_contrasena():
        while True:
            clave = EmpleadoView.leer_texto("Contraseña (8 a 20 caracteres): ")
            if 8 <= len(clave) <= 20 and any(c.isalpha() for c in clave) and any(c.isdigit() for c in clave):
                return clave
            print("Error: Debe tener una letra y un número")

    @staticmethod
    def formulario_nuevo():
        print("\nEscriba C para cancelar")
        try:
            return {
                "nombre": EmpleadoView.leer_texto("Nombre: "),
                "correo": EmpleadoView.leer_correo("Correo: "),
                "direccion": EmpleadoView.leer_texto("Dirección: "),
                "telefono": EmpleadoView.leer_telefono("Teléfono: "),
                "fecha_inicio": EmpleadoView.leer_fecha("Fecha inicio (AAAA-MM-DD): "),
                "salario": EmpleadoView.leer_salario("Salario: "),
                "id_departamento": EmpleadoView.leer_departamento("ID departamento (0 sin departamento): "),
                "contrasena": EmpleadoView.leer_contrasena()
            }
        except ValueError as e:
            if str(e) == "Operación cancelada":
                print(e)
                return None
            raise

    @staticmethod
    def formulario_editar(obj, gerente=None):
        print("\nEnter para mantener, C para cancelar")
        try:
            datos = {
                "nombre": EmpleadoView.leer_texto(f"Nombre ({obj.nombre}): ", obj.nombre),
                "correo": EmpleadoView.leer_correo(f"Correo ({obj.correo}): ", obj.correo),
                "direccion": EmpleadoView.leer_texto(f"Dirección ({obj.direccion}): ", obj.direccion),
                "telefono": EmpleadoView.leer_telefono(f"Teléfono ({obj.telefono}): ", obj.telefono),
                "fecha_inicio": EmpleadoView.leer_fecha(f"Fecha inicio ({obj.fecha_inicio}): ", obj.fecha_inicio),
                "salario": EmpleadoView.leer_salario(f"Salario ({obj.salario}): ", obj.salario)
            }
            id_actual = obj.departamento.id_departamento if obj.departamento else 0
            datos["id_departamento"] = id_actual if gerente else EmpleadoView.leer_departamento(
                f"ID departamento ({id_actual}): ", id_actual
            )
            return datos
        except ValueError as e:
            if str(e) == "Operación cancelada":
                print(e)
                return None
            raise

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
