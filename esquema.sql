PRAGMA foreign_keys = ON;

CREATE TABLE departamentos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    gerente_id INTEGER,
    FOREIGN KEY (gerente_id)
        REFERENCES empleados(id)
        ON DELETE RESTRICT
);

CREATE TABLE empleados (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT NOT NULL COLLATE NOCASE UNIQUE,
    fecha_inicio_contrato TEXT NOT NULL,
    salario INTEGER NOT NULL CHECK (salario >= 0),
    departamento_id INTEGER,
    FOREIGN KEY (departamento_id)
        REFERENCES departamentos(id)
        ON DELETE RESTRICT
);

CREATE TABLE proyectos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL
);

CREATE TABLE asignaciones_proyecto (
    empleado_id INTEGER NOT NULL,
    proyecto_id INTEGER NOT NULL,
    activa INTEGER NOT NULL DEFAULT 1
        CHECK (activa IN (0, 1)),
    PRIMARY KEY (empleado_id, proyecto_id),
    FOREIGN KEY (empleado_id)
        REFERENCES empleados(id)
        ON DELETE RESTRICT,
    FOREIGN KEY (proyecto_id)
        REFERENCES proyectos(id)
        ON DELETE RESTRICT
);

CREATE TABLE registros_tiempo (
    id INTEGER PRIMARY KEY,
    empleado_id INTEGER NOT NULL,
    proyecto_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    minutos INTEGER NOT NULL
        CHECK (minutos > 0 AND minutos <= 1440),
    descripcion TEXT NOT NULL,
    FOREIGN KEY (empleado_id, proyecto_id)
        REFERENCES asignaciones_proyecto(
            empleado_id,
            proyecto_id
        )
        ON DELETE RESTRICT
);