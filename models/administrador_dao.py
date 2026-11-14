from config.database import Database
from models.administrador import Administrador

class AdministradorDAO:
    @staticmethod
    def crear(administrador):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO administrador (nombre, correo, contrasena) VALUES (?, ?, ?)",
                (administrador.nombre, administrador.correo, administrador.contrasena)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error al registrar administrador: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_por_correo(correo):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM administrador WHERE correo = ?",
                (correo,)
            )
            fila = cursor.fetchone()

            if fila:
                administrador = Administrador.__new__(Administrador)
                administrador._nombre = fila["nombre"]
                administrador._correo = fila["correo"]
                administrador._contrasena = fila["contrasena"]
                return administrador

            return None

        except Exception as e:
            print(f"Error al buscar administrador: {e}")
            return None
        finally:
            conn.close()
