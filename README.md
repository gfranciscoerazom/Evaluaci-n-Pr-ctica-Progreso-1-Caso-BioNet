# Proyecto Integración BioNet

## Estructura del Proyecto

- **db/schema.sql**  
  Contiene el script SQL para crear las tablas y triggers necesarios en la base de datos PostgreSQL, incluyendo la tabla principal de resultados y la tabla de logs de cambios.

- **docs/informe_bionet.pdf**  
  Documento de análisis y diseño. Incluye la identificación de problemas, justificación de patrones, estructura de carpetas, diagramas de flujo y esquema de base de datos (en mermaid).

- **input-labs/**  
  Carpeta donde se depositan los archivos `.csv` generados por los laboratorios para ser procesados por el sistema.

- **processed/**  
  Carpeta donde se mueven los archivos `.csv` que han sido procesados exitosamente.

- **error/**  
  Carpeta donde se mueven los archivos `.csv` que presentan errores de formato o duplicidad.

- **scripts/main.py**  
  Script principal que implementa la lógica de integración: monitorea la carpeta de entrada, valida y procesa los archivos, inserta los datos en la base de datos y gestiona el movimiento de archivos.

## Resumen del Proyecto

Este proyecto resuelve la integración de resultados de exámenes clínicos de laboratorios distribuidos, centralizando la información en una base de datos PostgreSQL. Utiliza un script automatizado para recolectar, validar y consolidar los archivos `.csv` generados por los laboratorios, asegurando la unicidad de los datos y registrando todas las operaciones relevantes para auditoría. La solución está diseñada para ser robusta ante errores de formato, duplicados y problemas de concurrencia, facilitando la gestión centralizada y la trazabilidad de los resultados clínicos en BioNet.
