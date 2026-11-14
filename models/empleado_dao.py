from config.database import Database
from models.empleado import Empleado
from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO

class EmpleadoDAO:
    @staticmethod
    def crear(empleado):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            id_depto = empleado.departamento.id_departamento if empleado.departamento else None
            cursor.execute("""INSERT INTO empleado (nombre, correo, direccion, telefono, fecha_inicio, salario, id_departamento)
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (empleado.nombre, empleado.correo, empleado.direccion, empleado.telefono, empleado.fecha_inicio, empleado.salario, id_depto))
            conn.commit()
            empleado.id_empleado = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error al crear empleado: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def convertir(fila):
        departamento = DepartamentoDAO.obtener_por_id(fila['id_departamento']) if fila['id_departamento'] else None
        return Empleado(fila['nombre'], fila['correo'], fila['direccion'], fila['telefono'], fila['fecha_inicio'], fila['salario'], departamento, fila['id_empleado'])

    @staticmethod
    def obtener_todos():
        conn = Database().get_connection()
        empleados = []

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    e.*,
                    d.nombre AS nombre_departamento,
                    d.id_gerente
                FROM empleado e
                LEFT JOIN departamento d
                    ON e.id_departamento = d.id_departamento
            """)

            for fila in cursor.fetchall():
                departamento = None

                if fila["nombre_departamento"] is not None:
                    departamento = Departamento(
                        fila["nombre_departamento"],
                        fila["id_gerente"],
                        fila["id_departamento"]
                    )

                empleado = Empleado(
                    fila["nombre"],
                    fila["correo"],
                    fila["direccion"],
                    fila["telefono"],
                    fila["fecha_inicio"],
                    fila["salario"],
                    departamento,
                    fila["id_empleado"]
                )

                empleados.append(empleado)

        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return []

        finally:
            conn.close()

        return empleados

    @staticmethod
    def obtener_por_id(id_empleado):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM empleado WHERE id_empleado = ?", (id_empleado,))
            fila = cursor.fetchone()
            return EmpleadoDAO.convertir(fila) if fila else None
        except Exception as e:
            print(f"Error al buscar empleado: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def actualizar(empleado):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            id_depto = empleado.departamento.id_departamento if empleado.departamento else None
            cursor.execute("""UPDATE empleado SET nombre=?, correo=?, direccion=?, telefono=?, fecha_inicio=?, salario=?, id_departamento=? WHERE id_empleado=?""",
                (empleado.nombre, empleado.correo, empleado.direccion, empleado.telefono, empleado.fecha_inicio, empleado.salario, id_depto, empleado.id_empleado))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error al actualizar empleado: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_empleado):
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM empleado WHERE id_empleado = ?", (id_empleado,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error al eliminar empleado: {e}")
            return False
        finally:
            conn.close()
