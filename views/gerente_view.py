from views.utils import confirmar

class GerenteView:
    @staticmethod
    def mostrar_menu():
        print("\n--- GESTIÓN DE GERENTES ---")
        print("1.- Agregar gerente")
        print("2.- Editar gerente")
        print("3.- Eliminar gerente")
        print("4.- Imprimir un gerente")
        print("5.- Imprimir todos los gerentes")
        print("0.- Volver")

        while True:
            try:
                return int(input("Seleccione una opción: "))
            except ValueError:
                print("Error: Ingrese un número válido")

    @staticmethod
    def leer_dato(mensaje, actual=None):
        while True:
            dato = input(mensaje).strip()
            if dato.upper() == "C":
                print("Operación cancelada")
                return None
            if not dato and actual is not None:
                return actual
            if dato:
                return dato
            print("Error: Campo obligatorio")

    @staticmethod
    def formulario_nuevo():
        print("\n--- AGREGAR GERENTE ---")
        print("Escriba C para cancelar")

        nombre = GerenteView.leer_dato("Nombre: ")
        if nombre is None:
            return None

        correo = GerenteView.leer_dato("Correo: ")
        if correo is None:
            return None

        contrasena = GerenteView.leer_dato("Contraseña (8 a 20 caracteres): ")
        if contrasena is None:
            return None

        return {
            "nombre": nombre,
            "correo": correo,
            "contrasena": contrasena
        }

    @staticmethod
    def formulario_editar(obj):
        print("\nEnter para mantener, C para cancelar")

        nombre = GerenteView.leer_dato(
            f"Nombre ({obj.nombre}): ", obj.nombre
        )
        if nombre is None:
            return None

        correo = GerenteView.leer_dato(
            f"Correo ({obj.correo}): ", obj.correo
        )
        if correo is None:
            return None

        return {"nombre": nombre, "correo": correo}

    @staticmethod
    def solicitar_id():
        while True:
            try:
                numero = int(input("ID del gerente (0 para cancelar): "))
                if numero == 0:
                    print("Operación cancelada")
                    return None
                if numero > 0:
                    return numero
                print("Error: El ID debe ser positivo")
            except ValueError:
                print("Error: Ingrese un número válido")

    @staticmethod
    def mostrar_objeto(obj):
        print(obj)

    @staticmethod
    def mostrar_lista(objetos):
        if not objetos:
            print("No hay gerentes registrados")
        for obj in objetos:
            print(obj)

    @staticmethod
    def confirmar_eliminacion():
        return confirmar("¿Desea eliminarlo?")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(mensaje)
