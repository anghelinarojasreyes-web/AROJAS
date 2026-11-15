from views.utils import leer_numero


class MainView:
    @staticmethod
    def mostrar_menu():
        print("\n--- ECOTECH SOLUTIONS ---")
        print("1.- Iniciar sesión")
        print("0.- Salir")
        return leer_numero("Seleccione una opción: ")

