from validaciones import (
    validar_texto,
    validar_id_opcional
)


class Departamento:
    def __init__(
        self,
        nombre,
        gerente_id=None,
        id=None
    ):
        self._id = id
        self.cambiar_nombre(nombre)

        self._gerente_id = validar_id_opcional(
            gerente_id,
            "ID del gerente"
        )

    @property
    def nombre(self):
        return self._nombre

    def cambiar_nombre(self, nombre):
        self._nombre = validar_texto(
            nombre,
            "Nombre del departamento"
        )

    def asignar_gerente(self, empleado_id):
        self._gerente_id = validar_id_opcional(
            empleado_id,
            "ID del gerente"
        )

    def datos_para_guardar(self):
        return (
            self._nombre,
            self._gerente_id
        )