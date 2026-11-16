from config.database import Database
from models.gerente import Gerente

class GerenteDAO:
    @staticmethod
    def crear(gerente):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gerente (nombre, correo, contrasena) VALUES (?, ?, ?)",
                (gerente.nombre, gerente.correo, gerente.contrasena)
            )
            conn.commit()
            gerente.id_gerente = cursor.lastrowid
            return True
        except Exception:
            conn.rollback()
            print("Error al crear gerente")
            return False
        finally:
            conn.close()

    @staticmethod
    def convertir(fila):
        gerente = Gerente(
            fila["nombre"],
            fila["correo"],
            id_gerente=fila["id_gerente"]
        )
        gerente._contrasena = fila["contrasena"]
        return gerente

    @staticmethod
    def obtener_por_id(id_gerente):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gerente WHERE id_gerente = ?",
                (id_gerente,)
            )
            fila = cursor.fetchone()
            return GerenteDAO.convertir(fila) if fila else None
        except Exception:
            print("Error al buscar gerente")
            return None
        finally:
            conn.close()

    @staticmethod
    def obtener_por_correo(correo):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gerente WHERE correo = ?",
                (correo,)
            )
            fila = cursor.fetchone()
            return GerenteDAO.convertir(fila) if fila else None
        except Exception:
            print("Error al buscar gerente por correo")
            return None
        finally:
            conn.close()

    @staticmethod
    def obtener_todos():
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gerente")
            return [GerenteDAO.convertir(fila) for fila in cursor.fetchall()]
        except Exception:
            print("Error al obtener gerentes")
            return []
        finally:
            conn.close()

    @staticmethod
    def actualizar(gerente):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE gerente SET nombre = ?, correo = ? WHERE id_gerente = ?",
                (gerente.nombre, gerente.correo, gerente.id_gerente)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            print("Error al actualizar gerente")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_gerente):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM gerente WHERE id_gerente = ?",
                (id_gerente,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            print("Error al eliminar gerente")
            return False
        finally:
            conn.close()
