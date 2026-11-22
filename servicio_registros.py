class ServicioRegistros:
    @staticmethod
    def validar(
        conexion,
        datos,
        identificador=None
    ):
        empleado = conexion.execute(
            """
            SELECT fecha_inicio_contrato
            FROM empleados
            WHERE id = ?
            """,
            (datos["empleado_id"],)
        ).fetchone()

        proyecto = conexion.execute(
            """
            SELECT fecha_inicio
            FROM proyectos
            WHERE id = ?
            """,
            (datos["proyecto_id"],)
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
            (
                datos["empleado_id"],
                datos["proyecto_id"]
            )
        ).fetchone()

        if (
            asignacion is None
            or asignacion["activa"] != 1
        ):
            raise ValueError(
                "El empleado necesita una "
                "asignación activa al proyecto."
            )

        if (
            datos["fecha"]
            < empleado["fecha_inicio_contrato"]
        ):
            raise ValueError(
                "La fecha no puede ser anterior "
                "al inicio del contrato."
            )

        if (
            datos["fecha"]
            < proyecto["fecha_inicio"]
        ):
            raise ValueError(
                "La fecha no puede ser anterior "
                "al inicio del proyecto."
            )

        id_excluido = (
            identificador
            if identificador is not None
            else -1
        )

        resultado = conexion.execute(
            """
            SELECT COALESCE(SUM(minutos), 0)
            FROM registros_tiempo
            WHERE empleado_id = ?
              AND fecha = ?
              AND id <> ?
            """,
            (
                datos["empleado_id"],
                datos["fecha"],
                id_excluido
            )
        ).fetchone()

        minutos_actuales = resultado[0]

        if (
            minutos_actuales
            + datos["minutos"]
            > 1440
        ):
            raise ValueError(
                "El total diario del empleado "
                "superaría las 24 horas."
            )