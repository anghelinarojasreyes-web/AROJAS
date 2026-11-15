from views.utils import leer_numero, confirmar

class DepartamentoView:
    @staticmethod
    def mostrar_menu():
        print("\n--- GESTIÓN DE DEPARTAMENTOS ---")
        print("1.- Agregar departamento")
        print("2.- Editar departamento")
        print("3.- Eliminar departamento")
        print("4.- Imprimir un departamento")
        print("5.- Imprimir todos los departamentos")
        print("6.- Asignar empleado a departamento")
        print("7.- Quitar empleado de departamento")
        print("8.- Ver empleados de un departamento")
        print("0.- Volver")
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def leer_dato(mensaje, actual=None):
        while True:
            dato = input(mensaje).strip()
            if dato.upper() == "C":
                print("Operación cancelada")
                return False
            if not dato and actual is not None:
                return actual
            if dato:
                return dato
            print("Error: Campo obligatorio")

    @staticmethod
    def leer_gerente(mensaje, actual=None):
        while True:
            dato = input(mensaje).strip()
            if dato.upper() == "C":
                print("Operación cancelada")
                return False
            if not dato and actual is not None:
                return actual or None
            if dato.isdigit():
                return int(dato) or None
            print("Error: Ingrese un ID válido")

    @staticmethod
    def formulario_nuevo():
        print("\nEscriba C para cancelar")
        nombre = DepartamentoView.leer_dato("Nombre: ")
        if nombre is False:
            return None
        gerente = DepartamentoView.leer_gerente("ID del gerente (0 si no tiene): ")
        if gerente is False:
            return None
        return {"nombre": nombre, "gerente": gerente}

    @staticmethod
    def formulario_editar(obj):
        print("\nEnter para mantener, C para cancelar")
        nombre = DepartamentoView.leer_dato(f"Nombre ({obj.nombre}): ", obj.nombre)
        if nombre is False:
            return None
        gerente = DepartamentoView.leer_gerente(
            f"ID del gerente ({obj.gerente or 'Sin asignar'}): ",
            obj.gerente if obj.gerente is not None else 0
        )
        if gerente is False:
            return None
        return {"nombre": nombre, "gerente": gerente}

    @staticmethod
    def solicitar_id():
        while True:
            dato = input("ID del departamento (0 para cancelar): ").strip()
            if dato.upper() == "C" or dato == "0":
                print("Operación cancelada")
                return None
            if dato.isdigit() and int(dato) > 0:
                return int(dato)
            print("Error: Ingrese un ID válido")

    @staticmethod
    def solicitar_id_empleado():
        while True:
            dato = input("ID del empleado (0 para cancelar): ").strip()
            if dato.upper() == "C" or dato == "0":
                print("Operación cancelada")
                return None
            if dato.isdigit() and int(dato) > 0:
                return int(dato)
            print("Error: Ingrese un ID válido")

    @staticmethod
    def mostrar_objeto(obj):
        print(obj)

    @staticmethod
    def mostrar_lista(objetos):
        if not objetos:
            print("No hay registros")
            return
        for obj in objetos:
            print(obj)

    @staticmethod
    def mostrar_empleados(empleados):
        if not empleados:
            print("No hay empleados registrados")
            return
        for empleado in empleados:
            print(f"ID: {empleado.id_empleado} | Nombre: {empleado.nombre} | Correo: {empleado.correo}")

    @staticmethod
    def confirmar_eliminacion():
        return confirmar("¿Desea eliminarlo?")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(mensaje)

    @staticmethod
    def mostrar_titulo(titulo):
        print(f"\n--- {titulo} ---")
