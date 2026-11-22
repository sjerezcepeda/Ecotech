import sqlite3
from pathlib import Path


class ConexionBD:
    @staticmethod
    def obtener_conexion():
        carpeta_proyecto = Path(__file__).resolve().parent
        ruta = carpeta_proyecto / "datos" / "ecotech.db"

        if not ruta.is_file():
            raise FileNotFoundError(
                "No se encontro datos/ecotech.db"
            )

        conexion = sqlite3.connect(ruta, timeout=5)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")

        return conexion