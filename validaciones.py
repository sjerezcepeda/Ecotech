from datetime import date


def validar_texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(
            f"{campo} no puede estar vacío."
        )

    return valor.strip()


def validar_entero(valor, campo, minimo=1):
    if type(valor) is not int or valor < minimo:
        raise ValueError(
            f"{campo} debe ser un entero "
            f"mayor o igual a {minimo}."
        )

    return valor


def validar_id_opcional(valor, campo):
    if valor is None:
        return None

    return validar_entero(valor, campo)


def validar_fecha(valor):
    valor = validar_texto(valor, "Fecha")

    return date.fromisoformat(valor).isoformat()