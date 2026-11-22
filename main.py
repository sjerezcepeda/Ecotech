import sqlite3

from empleado import Empleado
from departamento import Departamento
from proyecto import Proyecto
from registro_tiempo import RegistroTiempo

from empleado_repositorio import (
    EmpleadoRepositorio
)

from departamento_repositorio import (
    DepartamentoRepositorio
)

from proyecto_repositorio import (
    ProyectoRepositorio
)

from registro_tiempo_repositorio import (
    RegistroTiempoRepositorio
)

from asignacion_repositorio import (
    AsignacionRepositorio
)

from informes import ServicioInformes


CONFIGURACIONES = {
    "1": {
        "titulo": "EMPLEADOS",
        "modelo": Empleado,
        "repositorio": EmpleadoRepositorio,
        "campos": [
            ("Nombre", "texto"),
            ("Dirección", "texto"),
            ("Teléfono", "texto"),
            ("Correo", "texto"),
            (
                "Inicio de contrato AAAA-MM-DD",
                "texto"
            ),
            (
                "Salario entero, sin puntos",
                "numero"
            ),
            (
                "ID departamento "
                "(vacío si no tiene)",
                "opcional"
            )
        ]
    },

    "2": {
        "titulo": "DEPARTAMENTOS",
        "modelo": Departamento,
        "repositorio": DepartamentoRepositorio,
        "campos": [
            ("Nombre", "texto"),
            (
                "ID gerente "
                "(vacío si aún no tiene)",
                "opcional"
            )
        ]
    },

    "3": {
        "titulo": "PROYECTOS",
        "modelo": Proyecto,
        "repositorio": ProyectoRepositorio,
        "campos": [
            ("Nombre", "texto"),
            ("Descripción", "texto"),
            (
                "Fecha de inicio AAAA-MM-DD",
                "texto"
            )
        ]
    },

    "4": {
        "titulo": "REGISTROS DE TIEMPO",
        "modelo": RegistroTiempo,
        "repositorio": RegistroTiempoRepositorio,
        "campos": [
            ("ID empleado", "numero"),
            ("ID proyecto", "numero"),
            ("Fecha AAAA-MM-DD", "texto"),
            ("Minutos enteros", "numero"),
            ("Descripción de tarea", "texto")
        ]
    }
}


def pedir_numero(mensaje, minimo=0):
    while True:
        try:
            valor = int(input(mensaje))

            if valor < minimo:
                print(
                    "El valor debe ser mayor "
                    f"o igual a {minimo}."
                )
                continue

            return valor

        except ValueError:
            print(
                "Debes escribir un número entero."
            )


def pedir_objeto(configuracion):
    valores = []

    for etiqueta, tipo in configuracion["campos"]:
        if tipo == "numero":
            valor = pedir_numero(
                etiqueta + ": "
            )

        elif tipo == "opcional":
            entrada = input(
                etiqueta + ": "
            ).strip()

            if entrada == "":
                valor = None
            else:
                valor = int(entrada)

        else:
            valor = input(
                etiqueta + ": "
            )

        valores.append(valor)

    clase = configuracion["modelo"]

    return clase(*valores)


def mostrar_fila(fila):
    partes = []

    for columna in fila.keys():
        partes.append(
            f"{columna}: {fila[columna]}"
        )

    print(" | ".join(partes))


def mostrar_filas(filas):
    if not filas:
        print("No hay resultados.")
        return

    for fila in filas:
        mostrar_fila(fila)


def ejecutar_controlado(accion):
    try:
        accion()

    except ValueError as error:
        print(
            "Revisa los datos:",
            error
        )

    except FileNotFoundError:
        print(
            "No se encontró datos/ecotech.db. "
            "Revisa la ubicación de la base."
        )

    except sqlite3.IntegrityError:
        print(
            "Operación rechazada: puede haber "
            "un dato repetido o registros "
            "relacionados que deben conservarse."
        )

    except sqlite3.OperationalError:
        print(
            "No se pudo completar la operación "
            "en SQLite. Revisa tablas, columnas "
            "y posibles bloqueos de la base."
        )

    except sqlite3.DatabaseError:
        print(
            "La base presentó un error. "
            "Conserva una copia y revisa "
            "el archivo."
        )

    except ModuleNotFoundError:
        print(
            "Falta una biblioteca de informes. "
            "Instala reportlab y openpyxl "
            "en el Python que estás utilizando."
        )

    except OSError:
        print(
            "No se pudo acceder al archivo. "
            "Revisa permisos y cierra el informe "
            "si está abierto."
        )


def menu_crud(configuracion):
    repositorio = (
        configuracion["repositorio"]()
    )

    while True:
        print(
            "\n===== "
            + configuracion["titulo"]
            + " ====="
        )

        print("1. Crear")
        print("2. Listar")
        print("3. Buscar por ID")
        print("4. Actualizar")
        print("5. Eliminar")
        print("0. Volver")

        opcion = input(
            "Selecciona una opción: "
        ).strip()

        if opcion == "0":
            return

        def accion():
            if opcion == "1":
                objeto = pedir_objeto(
                    configuracion
                )

                nuevo_id = repositorio.crear(
                    objeto
                )

                print(
                    "Registro creado con ID:",
                    nuevo_id
                )

            elif opcion == "2":
                mostrar_filas(
                    repositorio.listar()
                )

            elif opcion in ("3", "4", "5"):
                identificador = pedir_numero(
                    "ID del registro: ",
                    minimo=1
                )

                fila = repositorio.buscar(
                    identificador
                )

                if fila is None:
                    print(
                        "No se encontró el registro."
                    )
                    return

                mostrar_fila(fila)

                if opcion == "4":
                    print(
                        "\nVuelve a escribir TODOS "
                        "los datos del registro."
                    )

                    print(
                        "En campos opcionales, "
                        "vacío significa "
                        "sin asignación."
                    )

                    objeto = pedir_objeto(
                        configuracion
                    )

                    actualizado = (
                        repositorio.actualizar(
                            identificador,
                            objeto
                        )
                    )

                    if actualizado:
                        print(
                            "Registro actualizado."
                        )
                    else:
                        print(
                            "No se actualizó."
                        )

                elif opcion == "5":
                    confirmacion = input(
                        "Escribe ELIMINAR "
                        "para confirmar: "
                    )

                    if confirmacion != "ELIMINAR":
                        print(
                            "Eliminación cancelada."
                        )
                        return

                    eliminado = (
                        repositorio.eliminar(
                            identificador
                        )
                    )

                    if eliminado:
                        print(
                            "Registro eliminado."
                        )
                    else:
                        print(
                            "No se eliminó."
                        )

            else:
                print(
                    "La opción no existe."
                )

        ejecutar_controlado(accion)


def gestionar_asignacion(asignar):
    repositorio = AsignacionRepositorio()

    empleado_id = pedir_numero(
        "ID empleado: ",
        minimo=1
    )

    proyecto_id = pedir_numero(
        "ID proyecto: ",
        minimo=1
    )

    if asignar:
        repositorio.asignar(
            empleado_id,
            proyecto_id
        )

        print(
            "Asignación creada o reactivada."
        )

    else:
        actualizado = (
            repositorio.desasignar(
                empleado_id,
                proyecto_id
            )
        )

        if actualizado:
            print(
                "Empleado desasignado. "
                "El historial se conserva."
            )
        else:
            print(
                "No existe esa asignación activa."
            )


def generar_informe():
    print("1. PDF")
    print("2. Excel")

    opcion = input(
        "Formato: "
    ).strip()

    if opcion == "1":
        formato = "pdf"

    elif opcion == "2":
        formato = "xlsx"

    else:
        raise ValueError(
            "Formato no válido."
        )

    ruta = ServicioInformes().generar(
        formato
    )

    print(
        "Informe generado:",
        ruta
    )


def revisar_departamentos():
    filas = (
        DepartamentoRepositorio().listar()
    )

    pendientes = [
        fila
        for fila in filas
        if fila["gerente_id"] is None
    ]

    if pendientes:
        print(
            "Departamentos pendientes "
            "de completar gerente:"
        )

        mostrar_filas(pendientes)

    else:
        print(
            "No hay departamentos "
            "sin gerente."
        )


def main():
    print(
        "EcoTech - núcleo académico Unidad 2"
    )

    print(
        "Utiliza solamente datos ficticios."
    )

    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Empleados")
        print("2. Departamentos")
        print("3. Proyectos")
        print("4. Registros de tiempo")
        print("5. Asignar o reactivar proyecto")
        print("6. Desasignar proyecto")
        print("7. Ver asignaciones")
        print("8. Generar informe")
        print("9. Revisar departamentos sin gerente")
        print("0. Salir")

        opcion = input(
            "Selecciona una opción: "
        ).strip()

        if opcion == "0":
            print(
                "Programa finalizado."
            )
            return

        if opcion in CONFIGURACIONES:
            ejecutar_controlado(
                lambda: menu_crud(
                    CONFIGURACIONES[opcion]
                )
            )

        elif opcion == "5":
            ejecutar_controlado(
                lambda: gestionar_asignacion(True)
            )

        elif opcion == "6":
            ejecutar_controlado(
                lambda: gestionar_asignacion(False)
            )

        elif opcion == "7":
            ejecutar_controlado(
                lambda: mostrar_filas(
                    AsignacionRepositorio().listar()
                )
            )

        elif opcion == "8":
            ejecutar_controlado(
                generar_informe
            )

        elif opcion == "9":
            ejecutar_controlado(
                revisar_departamentos
            )

        else:
            print(
                "La opción no existe."
            )


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, EOFError):
        print(
            "\nSalida solicitada."
        )