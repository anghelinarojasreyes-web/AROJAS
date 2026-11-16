from config.database import Database
from models.administrador import Administrador

class AdministradorDAO:
    @staticmethod
    def convertir_administrador(fila):
        administrador = Administrador.__new__(Administrador)
        administrador._nombre = fila["nombre"]
        administrador._correo = fila["correo"]
        administrador._contrasena = fila["contrasena"]
        administrador.id_administrador = fila["id_administrador"]
        return administrador

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
            administrador.id_administrador = cursor.lastrowid
            return True
        except Exception:
            conn.rollback()
            print("Error al registrar administrador")
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(id_administrador):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM administrador WHERE id_administrador = ?",
                (id_administrador,)
            )
            fila = cursor.fetchone()
            return AdministradorDAO.convertir_administrador(fila) if fila else None
        except Exception:
            print("Error al buscar administrador")
            return None
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
            return AdministradorDAO.convertir_administrador(fila) if fila else None
        except Exception:
            print("Error al buscar administrador")
            return None
        finally:
            conn.close()

    @staticmethod
    def obtener_todos():
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM administrador")
            return [AdministradorDAO.convertir_administrador(fila) for fila in cursor.fetchall()]
        except Exception:
            print("Error al listar administradores")
            return []
        finally:
            conn.close()

    @staticmethod
    def actualizar(administrador):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE administrador SET nombre = ?, correo = ? WHERE id_administrador = ?",
                (administrador.nombre, administrador.correo, administrador.id_administrador)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            print("Error al actualizar administrador")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_administrador):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM administrador")
            cantidad = cursor.fetchone()[0]
            if cantidad <= 1:
                return False
            cursor.execute(
                "DELETE FROM administrador WHERE id_administrador = ?",
                (id_administrador,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            print("Error al eliminar administrador")
            return False
        finally:
            conn.close()
