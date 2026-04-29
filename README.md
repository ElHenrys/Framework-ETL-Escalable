# Framework ETL Escalable

Este proyecto es un framework estandarizado y modular construido en Python para automatizar procesos ETL (Extracción, Transformación y Carga) orientados a bases de datos Microsoft SQL Server. 

El sistema facilita la lectura de archivos planos (CSV, Excel, Parquet, HTML), su limpieza/procesamiento mediante Pandas, la carga en bases de datos y el movimiento de los archivos procesados, todo orquestado bajo un sistema de auditoría (logs) automatizado.

---

## 🚀 Características Principales

- **Lectura Automática:** Capacidad de inferir el método de lectura correcto según la extensión del archivo (`module_read_files.py`).
- **Gestión de Archivos:** Listado de archivos por directorios, validaciones dinámicas y uso de patrones de comodín (`module_list_files.py`), así como el movimiento automático tras su proceso (`module_move_files.py`).
- **Logging Integrado:** Registro detallado de tiempos de ejecución, estados (`OK`, `ERROR`, `ALERTA`) y pasos ejecutados directamente en base de datos (`module_logger_wfm.py`).
- **Configuración Centralizada:** Uso de archivos JSON para evitar "hardcodear" credenciales, rutas, tablas y procedimientos almacenados.
- **Manejo de Base de Datos:** Módulos abstractos para inserciones, eliminaciones parametrizadas por fecha/archivo y ejecución de Stored Procedures de forma segura.

---

## 📂 Estructura del Proyecto

```text
Framework-ETL-Escalable/
├── app/
│   ├── util_function/       # Módulos core de la aplicación
│   │   ├── module_read_files.py
│   │   ├── module_list_files.py
│   │   ├── module_insert.py
│   │   ├── module_delete.py
│   │   ├── module_exec_SP.py
│   │   ├── module_move_files.py
│   │   └── module_logger_wfm.py
│   ├── Entel_genesys.py     # Script ETL ejemplo 1
│   └── Iberia_genesys.py    # Script ETL ejemplo 2
├── config/                  # Archivos de configuración
│   ├── db.json              # Credenciales y conexiones DB
│   ├── log_db.json          # Configuración de base de datos de logs
│   ├── path_files.json      # Rutas de origen y destino de archivos
│   ├── store_procedure.json # Definición de procedimientos almacenados
│   └── table.json           # Metadatos de tablas destino y llaves de borrado
└── README.md
```

---

## ⚙️ Configuración (Carpeta `config/`)

Antes de ejecutar cualquier proceso, debes asegurarte de que los archivos JSON estén correctamente configurados. Los índices (ID) configurados en estos JSON son los que se consumirán en los scripts ETL de Python.

* **`db.json`**: Define conexiones (Host, Usuario, Password, Driver). Se recomienda usar variables de entorno.
* **`table.json`**: Define el esquema, tabla de destino y el campo usado para lógicas de borrado (Ej. `DELETE_BY`).
* **`path_files.json`**: Define las rutas físicas donde se alojan originalmente los archivos y el directorio de destino una vez son procesados.
* **`store_procedure.json`**: Define la sintaxis base para llamar a los procedimientos (Ej: `EXEC [esquema].[nombre_sp]`).

---

## 💻 Ejemplo de Uso

Todo script ETL nuevo debe instanciar el Logger principal y utilizar el envoltorio `execute_step` para garantizar la captura de errores o éxitos en la base de datos de auditoría.

```python
from util_function.module_list_files import list_files_by_pattern
from util_function.module_read_files import read_file_auto
from util_function.module_logger_wfm import ETLLogger

# 1. Iniciar Logger
logger = ETLLogger(cliente="MI_CLIENTE", servicio="MI_SERVICIO")

def execute_step(step_number, step_function, *args, **kwargs):
    """Wrapper para trazabilidad"""
    try:
        result = step_function(*args, **kwargs)
        logger.log_ok(step_number)
        return result
    except Exception as e:
        logger.log_error(step_number, e)
        return None

def mi_proceso_etl():
    logger.reset()
    logger.set_reporte("Nombre de mi Proceso")
    
    # 2. Listar archivos
    archivos = list_files_by_pattern(id_path_files=0, patron='*datos*.csv', logger=logger)
    
    # 3. Leer archivo y procesar
    for archivo in archivos:
        df = execute_step(2, read_file_auto, id_path_files=0, name_file=archivo)
        if df is not None:
            # Lógicas de limpieza e inserción aquí...
            pass
            
    logger.log_final_success()
```

## 🛠️ Requisitos e Instalación
pip freeze > requirements.txt 
