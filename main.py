from config.database import Database
from controllers.main_controller import MainController
from models.administrador import Administrador
from models.administrador_dao import AdministradorDAO


def crear_primer_administrador():
    conn = Database().get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM administrador")
        cantidad = cursor.fetchone()[0]
    finally:
        conn.close()

    if cantidad > 0:
        return

    print("\n--- CONFIGURACIÓN INICIAL DE ECOTECH ---")
    print("No existe ningún administrador registrado.")
    print("Debe crear una cuenta para comenzar.")

    while True:
        nombre = input("Nombre: ").strip()

        if nombre:
            break

        print("Debe ingresar un nombre")

    while True:
        correo = input("Correo: ").strip()

        if "@" in correo and "." in correo.split("@")[-1] and " " not in correo:
            break

        print("Debe ingresar un correo válido")

    print("\nLa contraseña debe tener:")
    print("- Entre 8 y 20 caracteres")
    print("- Al menos una letra")
    print("- Al menos un número")

    while True:
        contrasena = input("Contraseña: ")

        try:
            administrador = Administrador(nombre, correo, contrasena)
            break
        except ValueError as e:
            print(f"Error: {e}")

    if AdministradorDAO.crear(administrador):
        print("Primer administrador registrado correctamente")
    else:
        print("No se pudo registrar el administrador")


if __name__ == "__main__":
    db = Database()
    db.init_db()

    conn = db.get_connection()
    print("Conexión a la base de datos exitosa")
    conn.close()

    crear_primer_administrador()

    MainController().ejecutar()
