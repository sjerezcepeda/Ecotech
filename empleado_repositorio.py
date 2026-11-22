from repositorio_base import RepositorioBase


class EmpleadoRepositorio(RepositorioBase):
    tabla = "empleados"

    columnas = (
        "nombre",
        "direccion",
        "telefono",
        "correo",
        "fecha_inicio_contrato",
        "salario",
        "departamento_id"
    )

    def validar_relaciones(
        self,
        conexion,
        datos,
        identificador=None
    ):
        departamento_id = datos["departamento_id"]

        if departamento_id is not None:
            departamento = conexion.execute(
                "SELECT id FROM departamentos "
                "WHERE id = ?",
                (departamento_id,)
            ).fetchone()

            if departamento is None:
                raise ValueError(
                    "El departamento no existe."
                )

        if identificador is None:
            return

        gerencias = conexion.execute(
            "SELECT id FROM departamentos "
            "WHERE gerente_id = ?",
            (identificador,)
        ).fetchall()

        for departamento in gerencias:
            if departamento["id"] != departamento_id:
                raise ValueError(
                    "Este empleado es gerente. "
                    "Primero retíralo o reemplázalo "
                    "en el departamento que dirige."
                )

        primera_fecha = conexion.execute(
            "SELECT MIN(fecha) "
            "FROM registros_tiempo "
            "WHERE empleado_id = ?",
            (identificador,)
        ).fetchone()[0]

        if (
            primera_fecha is not None
            and datos["fecha_inicio_contrato"]
            > primera_fecha
        ):
            raise ValueError(
                "El contrato no puede comenzar "
                "después de horas ya registradas."
            )