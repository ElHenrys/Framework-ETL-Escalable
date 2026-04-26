import os
import pyodbc
import traceback
import json
import inspect
from datetime import datetime
from root_dir import get_root_dir

class ETLLogger:
    def __init__(self, cliente: str, servicio: str):
        # Cargar configuración desde log_db.json
        self._load_config()
        
        self.cliente = cliente
        self.servicio = servicio
        
        # Detectar automáticamente el archivo Python que se está ejecutando
        caller_frame = inspect.currentframe().f_back
        caller_file = caller_frame.f_code.co_filename
        self.proceso = os.path.basename(caller_file).replace('.py', '')
        
        # Extraer automáticamente el nombre de la carpeta del proyecto como ETL
        project_path = os.path.dirname(os.path.dirname(caller_file))
        self.etl = os.path.basename(project_path)
        
        # Diccionario de pasos estándar
        self.pasos = {
            1: "Listar Archivos",
            2: "Leer Archivos",
            3: "Validar Datos",
            4: "Borrar Datos Previos",
            5: "Insertar Datos",
            6: "Mover Archivos",
            7: "Ejercutar Stored Procedure",
            8: "Fin de Ejecución"
        }

        # Variable para el nombre del reporte
        self.reporte = None
        
        # Variables para el nuevo sistema de logging
        self.fecha_inicio = None
        self.ultimo_paso_exitoso = 0
        self.ultimo_error = None
        self.detalle_error = None
        self.star_date = None  #Fecha inicio de la data cargada por GTR
        self.end_date= None #Fecha fin de la data cargada por GTR
    
    def _load_config(self):
        """Cargar configuración de base de datos desde log_db.json"""
        root_dir = get_root_dir()
        config_path = os.path.join(root_dir, 'config', 'log_db.json')
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        db_config = config['database'][0]
        self.connection_string = f"DRIVER={{{db_config['DRIVER']}}};SERVER={os.getenv(db_config['HOST'])};DATABASE={os.getenv(db_config['NAME'])};UID={os.getenv(db_config['USER'])};PWD={os.getenv(db_config['PASSWORD'])}"   

    def log_range_date(self, range_date: tuple):
        """Recibe las fechas que carga GTR"""
        self.star_date = range_date[0]
        self.end_date = range_date[1]

    def set_reporte(self, reporte: str):
        """Definir el nombre del reporte e iniciar el cronómetro"""
        self.reporte = reporte
        self.fecha_inicio = datetime.now()

    def log_ok(self, paso_id: int):
        """Registrar paso exitoso"""
        self.ultimo_paso_exitoso = paso_id

    def log_error(self, paso_id: int, exception: Exception):
        """Registrar error en paso específico"""
        self.ultimo_error = paso_id
        detalle = f"{type(exception).__name__}: {str(exception)}\n{traceback.format_exc()}"
        if len(detalle) > 2000:
            start = 1500
            end = 400
            detalle = (
                detalle[:start]
                + "\n\n---RECORTADO POR LONGITUD---\n\n"
                + detalle[-end:]
            )
        self.detalle_error = detalle[:2000]
        self._insert_final_log()
    
    def log_alert(self, paso_id: int, message: str):
        """Registrar alerta en paso específico"""
        self.ultimo_error = paso_id
        self.detalle_error = message
        self._insert_alert_log()

    def log_final_success(self):
        """Registrar finalización exitosa del proceso"""
        self.ultimo_paso_exitoso = 8
        self._insert_final_log()

    def _insert_final_log(self):
        """Insertar log final con toda la información del proceso"""
        # Determinar el paso final y status
        if self.ultimo_error:
            paso_final = self.ultimo_error
            status = "ERROR"
            detalle = self.detalle_error
        else:
            paso_final = self.ultimo_paso_exitoso
            status = "OK"
            detalle = "Proceso completado exitosamente"
            
        self._insert_log_record(paso_final, status, detalle)
    
    def _insert_alert_log(self):
        """Insertar log de alerta con status ALERTA"""
        paso_final = self.ultimo_error
        status = "ALERTA"
        detalle = self.detalle_error
        
        self._insert_log_record(paso_final, status, detalle)

    def _insert_log_record(self, paso_final: int, status: str, detalle: str):
        """Método unificado para insertar registros en la tabla de logs."""
        fecha_fin = datetime.now()
        tmo_segundos = int((fecha_fin - self.fecha_inicio).total_seconds()) if self.fecha_inicio else 0
        
        paso_name = self.pasos.get(paso_final, f"Paso {paso_final} (no definido)")

        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO [logs].[stg_logs_etls] (
                inicio_proceso
                ,fin_proceso
                ,duracion
                ,fecha_cargada_inicio
                ,fecha_cargada_fin
                ,cliente
                ,servicio
                ,etl
                ,proceso
                ,reporte
                ,paso_id
                ,paso_name
                ,paso_stattus
                ,detalle
                       )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.fecha_inicio,
            fecha_fin,
            tmo_segundos,
            self.star_date,
            self.end_date,
            self.cliente,
            self.servicio,
            self.etl,
            self.proceso,
            self.reporte,
            str(paso_final),
            paso_name,
            status,
            detalle
        ))

        conn.commit()
        cursor.close()
        conn.close()

    def reset(self):      
        self.reporte = None
        self.fecha_inicio = None
        self.ultimo_paso_exitoso = 0
        self.ultimo_error = None
        self.detalle_error = None
        self.star_date = None  
        self.end_date= None