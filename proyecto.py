from validaciones import (
    validar_texto,
    validar_fecha
)


class Proyecto:
    def __init__(
        self,
        nombre,
        descripcion,
        fecha_inicio,
        id=None
    ):
        self._id = id

        self.editar(
            nombre,
            descripcion,
            fecha_inicio
        )

    def editar(
        self,
        nombre,
        descripcion,
        fecha_inicio
    ):
        nombre_validado = validar_texto(
            nombre,
            "Nombre del proyecto"
        )

        descripcion_validada = validar_texto(
            descripcion,
            "Descripción"
        )

        fecha_validada = validar_fecha(
            fecha_inicio
        )

        self._nombre = nombre_validado
        self._descripcion = descripcion_validada
        self._fecha_inicio = fecha_validada

    def datos_para_guardar(self):
        return (
            self._nombre,
            self._descripcion,
            self._fecha_inicio
        )