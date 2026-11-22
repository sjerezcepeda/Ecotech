from conexion import ConexionBD
from validaciones import validar_entero


class AsignacionRepositorio:
    def asignar(
        self,
        empleado_id,
        proyecto_id
    ):
        validar_entero(
            empleado_id,
            "ID del empleado"
        )

        validar_entero(
            proyecto_id,
            "ID del proyecto"
        )

        conexion = ConexionBD.obtener_conexion()

        try:
            conexion.execute("BEGIN IMMEDIATE")

            empleado = conexion.execute(
                "SELECT id FROM empleados "
                "WHERE id = ?",
                (empleado_id,)
            ).fetchone()

            proyecto = conexion.execute(
                "SELECT id FROM proyectos "
                "WHERE id = ?",
                (proyecto_id,)
            ).fetchone()

            if empleado is None:
                raise ValueError(
                    "El empleado no existe."
                )

            if proyecto is None:
                raise ValueError(
                    "El proyecto no existe."
                )

            asignacion = conexion.execute(
                """
                SELECT activa
                FROM asignaciones_proyecto
                WHERE empleado_id = ?
                  AND proyecto_id = ?
                """,
                (empleado_id, proyecto_id)
            ).fetchone()

            if asignacion is None:
                conexion.execute(
                    """
                    INSERT INTO asignaciones_proyecto (
                        empleado_id,
                        proyecto_id,
                        activa
                    )
                    VALUES (?, ?, 1)
                    """,
                    (empleado_id, proyecto_id)
                )

            elif asignacion["activa"] == 1:
                raise ValueError(
                    "El empleado ya está asignado "
                    "a ese proyecto."
                )

            else:
                conexion.execute(
                    """
                    UPDATE asignaciones_proyecto
                    SET activa = 1
                    WHERE empleado_id = ?
                      AND proyecto_id = ?
                    """,
                    (empleado_id, proyecto_id)
                )

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()

    def desasignar(
        self,
        empleado_id,
        proyecto_id
    ):
        validar_entero(
            empleado_id,
            "ID del empleado"
        )

        validar_entero(
            proyecto_id,
            "ID del proyecto"
        )

        conexion = ConexionBD.obtener_conexion()

        try:
            cursor = conexion.execute(
                """
                UPDATE asignaciones_proyecto
                SET activa = 0
                WHERE empleado_id = ?
                  AND proyecto_id = ?
                  AND activa = 1
                """,
                (empleado_id, proyecto_id)
            )

            conexion.commit()

            return cursor.rowcount == 1

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()

    def listar(self):
        conexion = ConexionBD.obtener_conexion()

        try:
            return conexion.execute(
                """
                SELECT
                    a.empleado_id,
                    e.nombre AS empleado,
                    a.proyecto_id,
                    p.nombre AS proyecto,
                    a.activa
                FROM asignaciones_proyecto AS a
                JOIN empleados AS e
                    ON e.id = a.empleado_id
                JOIN proyectos AS p
                    ON p.id = a.proyecto_id
                ORDER BY
                    a.empleado_id,
                    a.proyecto_id
                """
            ).fetchall()

        finally:
            conexion.close()