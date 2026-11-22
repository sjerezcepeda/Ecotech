from repositorio_base import RepositorioBase


class DepartamentoRepositorio(RepositorioBase):
    tabla = "departamentos"

    columnas = (
        "nombre",
        "gerente_id"
    )

    def validar_relaciones(
        self,
        conexion,
        datos,
        identificador=None
    ):
        gerente_id = datos["gerente_id"]

        if gerente_id is None:
            return

        empleado = conexion.execute(
            "SELECT departamento_id "
            "FROM empleados WHERE id = ?",
            (gerente_id,)
        ).fetchone()

        if empleado is None:
            raise ValueError(
                "El empleado indicado como "
                "gerente no existe."
            )

        if (
            identificador is None
            or empleado["departamento_id"]
            != identificador
        ):
            raise ValueError(
                "El gerente debe pertenecer "
                "al mismo departamento. "
                "Crea primero el departamento "
                "sin gerente y complétalo después."
            )