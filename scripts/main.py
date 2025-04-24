import os
import time
import shutil
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

INPUT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../input-labs'))
PROCESSED_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../processed'))
ERROR_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../error'))

# Connection string para PostgreSQL en Aiven (usa sslmode=require)
DB_URL = "postgresql+psycopg2://avnadmin:AVNS_4YaeS2XokteNx9v6OxX@pg-83e0710-proyecto-capstone.f.aivencloud.com:12526/defaultdb?sslmode=require"

REQUIRED_FIELDS = ['laboratorio_id', 'paciente_id',
                   'tipo_examen', 'resultado', 'fecha_examen']

# Verifica que el archivo no esté siendo escrito (tamaño estable durante 3 segundos)


def is_file_complete(filepath):
    size1 = os.path.getsize(filepath)
    time.sleep(3)
    size2 = os.path.getsize(filepath)
    return size1 == size2


def process_csv(file_path, engine):
    try:
        df = pd.read_csv(file_path, dtype=str, encoding='utf-8')
        if not all(field in df.columns for field in REQUIRED_FIELDS):
            return False  # Formato inválido

        if df[REQUIRED_FIELDS].isnull().any().any() or (df[REQUIRED_FIELDS] == '').any().any():
            return False  # Formato inválido

        with engine.begin() as conn:
            for _, row in df.iterrows():
                try:
                    conn.execute(
                        text("""
                            INSERT INTO resultados_examenes (laboratorio_id, paciente_id, tipo_examen, resultado, fecha_examen)
                            VALUES (:laboratorio_id, :paciente_id, :tipo_examen, :resultado, :fecha_examen)
                        """),
                        {
                            'laboratorio_id': row['laboratorio_id'],
                            'paciente_id': row['paciente_id'],
                            'tipo_examen': row['tipo_examen'],
                            'resultado': row['resultado'],
                            'fecha_examen': row['fecha_examen']
                        }
                    )
                except IntegrityError:
                    return False  # Duplicado
        return True
    except Exception:
        return False


def main():
    # El usuario debe crear la base y las tablas ejecutando schema.sql en PostgreSQL previamente
    try:
        engine = create_engine(DB_URL, connect_args={
                               "options": "-c client_encoding=utf8"})
        # Probar conexión
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        import traceback
        print(f"Error conectando a la base de datos: {e}")
        traceback.print_exc()
        return

    print('Monitorizando carpeta de entrada... (Ctrl+C para salir)')
    while True:
        for filename in os.listdir(INPUT_DIR):
            if not filename.lower().endswith('.csv'):
                continue
            file_path = os.path.join(INPUT_DIR, filename)
            if not is_file_complete(file_path):
                continue
            print(f'Procesando: {filename}')
            success = process_csv(file_path, engine)
            if success:
                shutil.move(file_path, os.path.join(PROCESSED_DIR, filename))
                print(f'Archivo procesado correctamente: {filename}')
            else:
                shutil.move(file_path, os.path.join(ERROR_DIR, filename))
                print(f'Archivo con error: {filename}')
        time.sleep(5)


if __name__ == '__main__':
    main()
