from repositorio_base import RepositorioBase


class ProyectoRepositorio(RepositorioBase):
    tabla = "proyectos"

    columnas = (
        "nombre",
        "descripcion",
        "fecha_inicio"
    )

    def validar_relaciones(
        self,
        conexion,
        datos,
        identificador=None
    ):
        if identificador is None:
            return

        primera_fecha = conexion.execute(
            "SELECT MIN(fecha) "
            "FROM registros_tiempo "
            "WHERE proyecto_id = ?",
            (identificador,)
        ).fetchone()[0]

        if (
            primera_fecha is not None
            and datos["fecha_inicio"] > primera_fecha
        ):
            raise ValueError(
                "El inicio del proyecto no puede "
                "ser posterior a horas "
                "que ya fueron registradas."
            )