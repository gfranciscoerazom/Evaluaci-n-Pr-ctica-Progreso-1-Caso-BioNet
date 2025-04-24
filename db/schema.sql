-- Script de creación de tablas y triggers para BioNet (PostgreSQL)

CREATE TABLE IF NOT EXISTS resultados_examenes (
    id SERIAL PRIMARY KEY,
    laboratorio_id TEXT NOT NULL,
    paciente_id TEXT NOT NULL,
    tipo_examen TEXT NOT NULL,
    resultado TEXT NOT NULL,
    fecha_examen DATE NOT NULL,
    UNIQUE(laboratorio_id, paciente_id, tipo_examen, fecha_examen)
);

CREATE TABLE IF NOT EXISTS log_cambios_resultados (
    id SERIAL PRIMARY KEY,
    operacion TEXT NOT NULL,
    paciente_id TEXT NOT NULL,
    tipo_examen TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Función para loguear inserts y updates
CREATE OR REPLACE FUNCTION log_resultados_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_cambios_resultados (operacion, paciente_id, tipo_examen)
    VALUES (TG_OP, NEW.paciente_id, NEW.tipo_examen);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para loguear inserts
DROP TRIGGER IF EXISTS log_resultados_insert ON resultados_examenes;
CREATE TRIGGER log_resultados_insert
AFTER INSERT ON resultados_examenes
FOR EACH ROW EXECUTE FUNCTION log_resultados_func();

-- Trigger para loguear updates
DROP TRIGGER IF EXISTS log_resultados_update ON resultados_examenes;
CREATE TRIGGER log_resultados_update
AFTER UPDATE ON resultados_examenes
FOR EACH ROW EXECUTE FUNCTION log_resultados_func();
