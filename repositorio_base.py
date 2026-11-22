from conexion import ConexionBD


class RepositorioBase:
    TABLAS_PERMITIDAS = {
        "empleados",
        "departamentos",
        "proyectos",
        "registros_tiempo"
    }

    tabla = ""
    columnas = ()

    def __init__(self):
        if self.tabla not in self.TABLAS_PERMITIDAS:
            raise ValueError(
                "Tabla no permitida."
            )

    def listar(self):
        conexion = ConexionBD.obtener_conexion()

        try:
            consulta = (
                f"SELECT * FROM {self.tabla} "
                "ORDER BY id"
            )

            return conexion.execute(
                consulta
            ).fetchall()

        finally:
            conexion.close()

    def buscar(self, identificador):
        conexion = ConexionBD.obtener_conexion()

        try:
            consulta = (
                f"SELECT * FROM {self.tabla} "
                "WHERE id = ?"
            )

            return conexion.execute(
                consulta,
                (identificador,)
            ).fetchone()

        finally:
            conexion.close()

    def validar_relaciones(
        self,
        conexion,
        datos,
        identificador=None
    ):
        pass

    def crear(self, objeto):
        conexion = ConexionBD.obtener_conexion()

        try:
            conexion.execute("BEGIN IMMEDIATE")

            valores = objeto.datos_para_guardar()

            datos = dict(
                zip(self.columnas, valores)
            )

            self.validar_relaciones(
                conexion,
                datos
            )

            nombres = ", ".join(self.columnas)

            marcas = ", ".join(
                "?" for _ in self.columnas
            )

            consulta = (
                f"INSERT INTO {self.tabla} "
                f"({nombres}) VALUES ({marcas})"
            )

            cursor = conexion.execute(
                consulta,
                valores
            )

            conexion.commit()

            return cursor.lastrowid

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()

    def actualizar(
        self,
        identificador,
        objeto
    ):
        conexion = ConexionBD.obtener_conexion()

        try:
            conexion.execute("BEGIN IMMEDIATE")

            existente = conexion.execute(
                f"SELECT id FROM {self.tabla} "
                "WHERE id = ?",
                (identificador,)
            ).fetchone()

            if existente is None:
                return False

            valores = objeto.datos_para_guardar()

            datos = dict(
                zip(self.columnas, valores)
            )

            self.validar_relaciones(
                conexion,
                datos,
                identificador
            )

            cambios = ", ".join(
                f"{columna} = ?"
                for columna in self.columnas
            )

            consulta = (
                f"UPDATE {self.tabla} "
                f"SET {cambios} WHERE id = ?"
            )

            conexion.execute(
                consulta,
                valores + (identificador,)
            )

            conexion.commit()

            return True

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()

    def eliminar(self, identificador):
        conexion = ConexionBD.obtener_conexion()

        try:
            cursor = conexion.execute(
                f"DELETE FROM {self.tabla} "
                "WHERE id = ?",
                (identificador,)
            )

            conexion.commit()

            return cursor.rowcount == 1

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()