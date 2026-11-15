from config.database import Database
from models.departamento import Departamento

class DepartamentoDAO:
    @staticmethod
    def crear(departamento):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO departamento (nombre, id_gerente) VALUES (?, ?)",
                (departamento.nombre, departamento.gerente)
            )
            conn.commit()
            departamento.id_departamento = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error al crear departamento: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def convertir(fila):
        return Departamento(
            fila["nombre"],
            fila["id_gerente"],
            fila["id_departamento"]
        )

    @staticmethod
    def obtener_todos():
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departamento")
            return [DepartamentoDAO.convertir(fila) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener departamentos: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(id_departamento):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM departamento WHERE id_departamento = ?",
                (id_departamento,)
            )
            fila = cursor.fetchone()
            return DepartamentoDAO.convertir(fila) if fila else None
        except Exception as e:
            print(f"Error al buscar departamento: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def actualizar(departamento):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE departamento SET nombre = ?, id_gerente = ? WHERE id_departamento = ?",
                (departamento.nombre, departamento.gerente, departamento.id_departamento)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error al actualizar departamento: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_departamento):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM departamento WHERE id_departamento = ?",
                (id_departamento,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error al eliminar departamento: {e}")
            return False
        finally:
            conn.close()
