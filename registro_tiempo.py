from validaciones import (
    validar_entero,
    validar_texto,
    validar_fecha
)


class RegistroTiempo:
    def __init__(
        self,
        empleado_id,
        proyecto_id,
        fecha,
        minutos,
        descripcion,
        id=None
    ):
        self._id = id

        self._empleado_id = validar_entero(
            empleado_id,
            "ID del empleado"
        )

        self._proyecto_id = validar_entero(
            proyecto_id,
            "ID del proyecto"
        )

        self._fecha = validar_fecha(fecha)

        self._minutos = validar_entero(
            minutos,
            "Minutos"
        )

        if self._minutos > 1440:
            raise ValueError(
                "Un registro no puede superar "
                "1440 minutos."
            )

        self._descripcion = validar_texto(
            descripcion,
            "Descripción de la tarea"
        )

    def obtener_horas(self):
        return self._minutos / 60

    def datos_para_guardar(self):
        return (
            self._empleado_id,
            self._proyecto_id,
            self._fecha,
            self._minutos,
            self._descripcion
        )