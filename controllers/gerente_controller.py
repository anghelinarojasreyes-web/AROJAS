from models.gerente import Gerente
from models.gerente_dao import GerenteDAO

class GerenteController:
    def ejecutar(self):
        while True:
            print("\n--- GESTIÓN DE GERENTES ---")
            print("1.- Registrar gerente")
            print("2.- Buscar gerente")
            print("0.- Volver")

            try:
                opcion = int(input("Seleccione una opción: "))

                if opcion == 1:
                    self.agregar()
                elif opcion == 2:
                    self.buscar()
                elif opcion == 0:
                    break
                else:
                    print("Opción no válida")
            except ValueError:
                print("Debe ingresar un número")

    def agregar(self):
        try:
            nombre = input("Nombre: ")
            correo = input("Correo: ")

            print("\nLa contraseña debe cumplir estos requisitos:")
            print("- Entre 8 y 20 caracteres")
            print("- Al menos una letra")
            print("- Al menos un número")

            contrasena = input("Contraseña: ")

            gerente = Gerente(nombre, correo, contrasena)

            if GerenteDAO.crear(gerente):
                print(f"Gerente registrado con ID: {gerente.id_gerente}")
            else:
                print("No se pudo registrar el gerente")

        except ValueError as e:
            print(f"Error: {e}")

    def buscar(self):
        try:
            id_gerente = int(input("ID del gerente: "))
            gerente = GerenteDAO.obtener_por_id(id_gerente)

            if gerente:
                print(gerente)
            else:
                print("Gerente no encontrado")

        except ValueError:
            print("Debe ingresar un ID válido")
