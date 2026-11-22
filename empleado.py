from datetime import date


class Empleado:
    def __init__(
        self,
        nombre,
        direccion,
        telefono,
        correo,
        fecha_inicio_contrato,
        salario,
        departamento_id=None,
        id=None
    ):
        self._id = id
        self._nombre = self.validar_texto(nombre, "Nombre")
        self._direccion = self.validar_texto(
            direccion, "Dirección"
        )
        self._telefono = self.validar_texto(
            telefono, "Teléfono"
        )

        self.cambiar_correo(correo)
        self.actualizar_salario(salario)

        self._fecha_inicio_contrato = date.fromisoformat(
            fecha_inicio_contrato
        ).isoformat()

        if departamento_id is not None:
            if type(departamento_id) is not int:
                raise ValueError(
                    "El ID del departamento debe ser entero."
                )

            if departamento_id <= 0:
                raise ValueError(
                    "El ID del departamento debe ser positivo."
                )

        self._departamento_id = departamento_id

    @staticmethod
    def validar_texto(valor, campo):
        if not isinstance(valor, str):
            raise ValueError(f"{campo} debe ser texto.")

        valor = valor.strip()

        if valor == "":
            raise ValueError(f"{campo} no puede estar vacío.")

        return valor

    @property
    def nombre(self):
        return self._nombre

    @property
    def salario(self):
        return self._salario

    def cambiar_correo(self, correo):
        correo = self.validar_texto(
            correo, "Correo"
        ).lower()

        if correo.count("@") != 1:
            raise ValueError("El correo debe tener una @.")

        usuario, dominio = correo.split("@")

        if (
            not usuario
            or "." not in dominio
            or dominio.startswith(".")
            or dominio.endswith(".")
            or any(letra.isspace() for letra in correo)
        ):
            raise ValueError("El correo no tiene formato válido.")

        self._correo = correo

    def actualizar_salario(self, salario):
        if type(salario) is not int:
            raise ValueError(
                "El salario debe ser un número entero."
            )

        if salario < 0:
            raise ValueError(
                "El salario no puede ser negativo."
            )

        self._salario = salario

    def datos_para_guardar(self):
        return (
            self._nombre,
            self._direccion,
            self._telefono,
            self._correo,
            self._fecha_inicio_contrato,
            self._salario,
            self._departamento_id
        )