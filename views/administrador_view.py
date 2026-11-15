class AdministradorView:
    @staticmethod
    def mostrar_menu():
        print("\n--- GESTIÓN DE ADMINISTRADORES ---")
        print("1.- Registrar administrador")
        print("2.- Editar administrador")
        print("3.- Eliminar administrador")
        print("4.- Buscar administrador")
        print("5.- Mostrar todos los administradores")
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
        print("\n--- REGISTRAR ADMINISTRADOR ---")
        print("Escriba C para cancelar")

        nombre = AdministradorView.leer_dato("Nombre: ")
        if nombre is None:
            return None

        correo = AdministradorView.leer_dato("Correo: ")
        if correo is None:
            return None

        contrasena = AdministradorView.leer_dato(
            "Contraseña (8 a 20 caracteres): "
        )
        if contrasena is None:
            return None

        return {
            "nombre": nombre,
            "correo": correo,
            "contrasena": contrasena
        }

    @staticmethod
    def formulario_editar(administrador):
        print("\n--- EDITAR ADMINISTRADOR ---")
        print("Enter para mantener, C para cancelar")

        nombre = AdministradorView.leer_dato(
            f"Nombre ({administrador.nombre}): ",
            administrador.nombre
        )
        if nombre is None:
            return None

        correo = AdministradorView.leer_dato(
            f"Correo ({administrador.correo}): ",
            administrador.correo
        )
        if correo is None:
            return None

        return {"nombre": nombre, "correo": correo}

    @staticmethod
    def solicitar_id():
        while True:
            try:
                numero = int(input("ID del administrador (0 para cancelar): "))

                if numero == 0:
                    print("Operación cancelada")
                    return None

                if numero > 0:
                    return numero

                print("Error: El ID debe ser positivo")

            except ValueError:
                print("Error: Ingrese un número válido")

    @staticmethod
    def mostrar_objeto(administrador):
        print(f"ID: {administrador.id_administrador}")
        print(f"Nombre: {administrador.nombre}")
        print(f"Correo: {administrador.correo}")

    @staticmethod
    def mostrar_lista(administradores):
        if not administradores:
            print("No hay administradores registrados")
            return

        for administrador in administradores:
            print(
                f"ID: {administrador.id_administrador} | "
                f"Nombre: {administrador.nombre} | "
                f"Correo: {administrador.correo}"
            )

    @staticmethod
    def confirmar_eliminacion():
        respuesta = input("¿Desea eliminarlo? (S/N): ").strip().upper()
        return respuesta == "S"

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(mensaje)
