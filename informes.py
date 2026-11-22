from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

from conexion import ConexionBD


class ExportadorInforme(ABC):
    @abstractmethod
    def exportar(self, secciones, ruta):
        pass


class ExportadorExcel(ExportadorInforme):
    def exportar(self, secciones, ruta):
        from openpyxl import Workbook
        from openpyxl.cell.cell import (
            ILLEGAL_CHARACTERS_RE
        )

        libro = Workbook()
        libro.remove(libro.active)

        for nombre, contenido in secciones.items():
            columnas, filas = contenido

            hoja = libro.create_sheet(
                nombre[:31]
            )

            for fila in [columnas] + filas:
                valores = []

                for valor in fila:
                    if isinstance(valor, str):
                        valor = (
                            ILLEGAL_CHARACTERS_RE.sub(
                                "",
                                valor
                            )
                        )

                    valores.append(valor)

                hoja.append(valores)

                for celda in hoja[hoja.max_row]:
                    if isinstance(
                        celda.value,
                        str
                    ):
                        celda.data_type = "s"

        libro.save(ruta)


class ExportadorPDF(ExportadorInforme):
    def exportar(self, secciones, ruta):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import (
            A4,
            landscape
        )
        from reportlab.lib.styles import (
            getSampleStyleSheet
        )
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Table,
            TableStyle,
            PageBreak,
            Spacer
        )

        estilos = getSampleStyleSheet()
        estilo_celda = estilos["BodyText"]
        estilo_celda.fontSize = 8
        estilo_celda.leading = 10

        elementos = []

        for nombre, contenido in secciones.items():
            columnas, filas = contenido

            if elementos:
                elementos.append(PageBreak())

            elementos.append(
                Paragraph(
                    "EcoTech: " + nombre,
                    estilos["Heading1"]
                )
            )

            elementos.append(Spacer(1, 12))

            datos = [columnas] + filas
            celdas = []

            for fila in datos:
                fila_pdf = []

                for valor in fila:
                    texto = (
                        "Sin asignar"
                        if valor is None
                        else str(valor)
                    )

                    fila_pdf.append(
                        Paragraph(
                            escape(texto),
                            estilo_celda
                        )
                    )

                celdas.append(fila_pdf)

            ancho = 750 / len(columnas)

            tabla = Table(
                celdas,
                repeatRows=1,
                colWidths=[
                    ancho
                    for _ in columnas
                ]
            )

            tabla.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    )
                ])
            )

            elementos.append(tabla)

        documento = SimpleDocTemplate(
            str(ruta),
            pagesize=landscape(A4),
            leftMargin=35,
            rightMargin=35
        )

        documento.build(elementos)


class ServicioInformes:
    def obtener_datos(self):
        consultas = {
            "Empleados": """
                SELECT
                    e.id,
                    e.nombre,
                    e.correo,
                    e.salario,
                    d.nombre AS departamento
                FROM empleados AS e
                LEFT JOIN departamentos AS d
                    ON d.id = e.departamento_id
                ORDER BY e.id
            """,

            "Departamentos": """
                SELECT
                    d.id,
                    d.nombre,
                    e.nombre AS gerente
                FROM departamentos AS d
                LEFT JOIN empleados AS e
                    ON e.id = d.gerente_id
                ORDER BY d.id
            """,

            "Proyectos": """
                SELECT
                    id,
                    nombre,
                    descripcion,
                    fecha_inicio
                FROM proyectos
                ORDER BY id
            """,

            "Tiempo": """
                SELECT
                    r.id,
                    e.nombre AS empleado,
                    p.nombre AS proyecto,
                    r.fecha,
                    r.minutos,
                    r.descripcion
                FROM registros_tiempo AS r
                JOIN empleados AS e
                    ON e.id = r.empleado_id
                JOIN proyectos AS p
                    ON p.id = r.proyecto_id
                ORDER BY r.fecha, r.id
            """
        }

        conexion = ConexionBD.obtener_conexion()

        try:
            secciones = {}

            for nombre, consulta in consultas.items():
                cursor = conexion.execute(
                    consulta
                )

                columnas = [
                    columna[0]
                    for columna
                    in cursor.description
                ]

                filas = [
                    list(fila)
                    for fila
                    in cursor.fetchall()
                ]

                secciones[nombre] = (
                    columnas,
                    filas
                )

            return secciones

        finally:
            conexion.close()

    def generar(self, formato):
        if formato == "pdf":
            exportador = ExportadorPDF()

        elif formato == "xlsx":
            exportador = ExportadorExcel()

        else:
            raise ValueError(
                "Formato no permitido."
            )

        carpeta = (
            Path(__file__).resolve().parent
            / "reportes"
        )

        carpeta.mkdir(exist_ok=True)

        nombre = datetime.now().strftime(
            "informe_%Y%m%d_%H%M%S_%f"
        )

        ruta = carpeta / (
            nombre + "." + formato
        )

        secciones = self.obtener_datos()

        exportador.exportar(
            secciones,
            ruta
        )

        return ruta