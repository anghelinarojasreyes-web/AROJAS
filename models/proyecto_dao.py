from config.database import Database
from models.proyecto import Proyecto

class ProyectoDAO:
    @staticmethod
    def crear(proyecto):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES (?, ?, ?)",
                (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio)
            )
            conn.commit()
            proyecto.id_proyecto = cursor.lastrowid
            return True
        except Exception:
            conn.rollback()
            print("Error al crear proyecto")
            return False
        finally:
            conn.close()

    @staticmethod
    def convertir(fila):
        return Proyecto(
            fila["nombre"],
            fila["descripcion"],
            fila["fecha_inicio"],
            fila["id_proyecto"]
        )

    @staticmethod
    def obtener_todos():
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proyecto")
            return [ProyectoDAO.convertir(fila) for fila in cursor.fetchall()]
        except Exception:
            print("Error al obtener proyectos")
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(id_proyecto):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM proyecto WHERE id_proyecto = ?",
                (id_proyecto,)
            )
            fila = cursor.fetchone()
            return ProyectoDAO.convertir(fila) if fila else None
        except Exception:
            print("Error al buscar proyecto")
            return None
        finally:
            conn.close()

    @staticmethod
    def actualizar(proyecto):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE proyecto SET nombre=?, descripcion=?, fecha_inicio=? WHERE id_proyecto=?",
                (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.id_proyecto)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            print("Error al actualizar proyecto")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_proyecto):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM proyecto WHERE id_proyecto = ?",
                (id_proyecto,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            print("Error al eliminar proyecto")
            return False
        finally:
            conn.close()

    @staticmethod
    def asignar_empleado(id_empleado, id_proyecto):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (?, ?)",
                (id_empleado, id_proyecto)
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            print("Error al asignar empleado al proyecto")
            return False
        finally:
            conn.close()

    @staticmethod
    def quitar_empleado(id_empleado, id_proyecto):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM empleado_proyecto WHERE id_empleado=? AND id_proyecto=?",
                (id_empleado, id_proyecto)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            print("Error al quitar empleado del proyecto")
            return False
        finally:
            conn.close()

    @staticmethod
    def ver_empleados(id_proyecto):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id_empleado, e.nombre
                FROM empleado e
                INNER JOIN empleado_proyecto ep
                ON e.id_empleado = ep.id_empleado
                WHERE ep.id_proyecto = ?
            """, (id_proyecto,))
            return cursor.fetchall()
        except Exception:
            print("Error al consultar empleados del proyecto")
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_por_empleado(id_empleado):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.*
                FROM proyecto p
                INNER JOIN empleado_proyecto ep
                ON p.id_proyecto = ep.id_proyecto
                WHERE ep.id_empleado = ?
            """, (id_empleado,))
            return [ProyectoDAO.convertir(fila) for fila in cursor.fetchall()]
        except Exception:
            print("Error al consultar proyectos del empleado")
            return []
        finally:
            conn.close()
