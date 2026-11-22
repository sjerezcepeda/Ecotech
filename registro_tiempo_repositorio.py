from repositorio_base import RepositorioBase
from servicio_registros import ServicioRegistros


class RegistroTiempoRepositorio(
    RepositorioBase
):
    tabla = "registros_tiempo"

    columnas = (
        "empleado_id",
        "proyecto_id",
        "fecha",
        "minutos",
        "descripcion"
    )

    def validar_relaciones(
        self,
        conexion,
        datos,
        identificador=None
    ):
        ServicioRegistros.validar(
            conexion,
            datos,
            identificador
        )