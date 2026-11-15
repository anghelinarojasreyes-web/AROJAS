from config.database import Database
from models.registro_tiempo import RegistroTiempo
from models.empleado import Empleado
from models.proyecto import Proyecto
from models.departamento import Departamento

class RegistroTiempoDAO:
    @staticmethod
    def crear(registro):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO registro_tiempo
                (fecha, horas_trabajadas, descripcion, id_empleado, id_proyecto)
                VALUES (?, ?, ?, ?, ?)
            """, (registro.fecha, registro.horas_trabajadas,
                  registro.descripcion, registro.empleado.id_empleado,
                  registro.proyecto.id_proyecto))
            conn.commit()
            registro.id_registro = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error al crear registro: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def convertir(fila):
        departamento = None
        if fila["id_departamento"] is not None:
            departamento = Departamento(
                fila["departamento_nombre"],
                fila["id_gerente"],
                fila["id_departamento"]
            )
        empleado = Empleado(
            fila["empleado_nombre"],
            fila["correo"],
            fila["direccion"],
            fila["telefono"],
            fila["empleado_fecha_inicio"],
            fila["salario"],
            departamento,
            fila["id_empleado"]
        )
        empleado._contrasena = fila["contrasena"]
        proyecto = Proyecto(
            fila["proyecto_nombre"],
            fila["proyecto_descripcion"],
            fila["proyecto_fecha_inicio"],
            fila["id_proyecto"]
        )
        return RegistroTiempo(
            fila["fecha"],
            fila["horas_trabajadas"],
            fila["descripcion"],
            empleado,
            proyecto,
            fila["id_registro"]
        )

    @staticmethod
    def obtener_todos():
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(RegistroTiempoDAO.consulta_registros())
            return [RegistroTiempoDAO.convertir(fila) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener registros: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def consulta_registros():
        return """
            SELECT r.id_registro, r.fecha, r.horas_trabajadas, r.descripcion,
                   e.id_empleado, e.nombre AS empleado_nombre, e.correo,
                   e.direccion, e.telefono, e.fecha_inicio AS empleado_fecha_inicio,
                   e.salario, e.contrasena, e.id_departamento,
                   d.nombre AS departamento_nombre, d.id_gerente,
                   p.id_proyecto, p.nombre AS proyecto_nombre,
                   p.descripcion AS proyecto_descripcion,
                   p.fecha_inicio AS proyecto_fecha_inicio
            FROM registro_tiempo r
            JOIN empleado e ON r.id_empleado = e.id_empleado
            LEFT JOIN departamento d ON e.id_departamento = d.id_departamento
            JOIN proyecto p ON r.id_proyecto = p.id_proyecto
        """

    @staticmethod
    def obtener_por_id(id_registro):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                RegistroTiempoDAO.consulta_registros() + " WHERE r.id_registro = ?",
                (id_registro,)
            )
            fila = cursor.fetchone()
            return RegistroTiempoDAO.convertir(fila) if fila else None
        except Exception as e:
            print(f"Error al buscar registro: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def actualizar(registro):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE registro_tiempo
                SET fecha=?, horas_trabajadas=?, descripcion=?,
                    id_empleado=?, id_proyecto=?
                WHERE id_registro=?
            """, (registro.fecha, registro.horas_trabajadas,
                  registro.descripcion, registro.empleado.id_empleado,
                  registro.proyecto.id_proyecto, registro.id_registro))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error al actualizar registro: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_registro):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM registro_tiempo WHERE id_registro = ?",
                (id_registro,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error al eliminar registro: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_por_empleado(id_empleado):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                RegistroTiempoDAO.consulta_registros() + " WHERE e.id_empleado = ?",
                (id_empleado,)
            )
            return [RegistroTiempoDAO.convertir(fila) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error al consultar registros: {e}")
            return []
        finally:
            conn.close()
