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
        except Exception as e:
            conn.rollback()
            print(f"Error al crear gerente: {e}")
            return False
        finally:
            conn.close()

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
            if fila:
                gerente = Gerente(
                    fila["nombre"],
                    fila["correo"],
                    id_gerente=fila["id_gerente"]
                )
                gerente._contrasena = fila["contrasena"]
                return gerente
            return None
        except Exception as e:
            print(f"Error al buscar gerente: {e}")
            return None
        finally:
            conn.close()