
from util_function.module_list_files import list_files_by_pattern
from util_function.module_read_files import read_file_auto
from util_function.module_move_files import move_files
from util_function.module_insert import insert_mssql
from util_function.module_exec_SP import exec_SP_mssql
from util_function.module_delete import delete_by_date
from util_function.module_logger_wfm import ETLLogger
import pandas as pd

# Parametros Iniciales para Logger
logger = ETLLogger(
    cliente="IBERIA",
    servicio="VUELOS INTERNACIONALES"
)

def execute_step(step_number, step_function, *args, **kwargs):
    """Ejecuta un paso del ETL con manejo automático de errores"""
    try:
        result = step_function(*args, **kwargs)
        logger.log_ok(step_number)
        return result
    except Exception as e:
        logger.log_error(step_number, e)
        return None

def reporte_logueos():
    logger.reset()
    logger.set_reporte("Corte de indicadores")
    
    try:
        # PASO 1: LISTAR Y VALIDAR ARCHIVOS
        patron = '*Iberia*.csv'
        listfiles = list_files_by_pattern(id_path_files=0, patron=patron)
        if not listfiles:
            return False  
        
        lista_df = []

        for file in listfiles:
            df = execute_step(2, read_file_auto, id_path_files=0, name_file=file, read_kwargs={"sep":';'})
            if df is None: return False

            lista_df.append(df)

            move_result = execute_step(6, move_files, id_path_files=0, name_file=file)
            if move_result is None: return False

        df_final = pd.concat(lista_df, ignore_index=True)
        df_final['Interval Start'] = pd.to_datetime(df_final['Interval Start'], format='mixed', errors='coerce')
        df_final['Interval End'] = pd.to_datetime(df_final['Interval End'], format='mixed', errors='coerce')

        fechas_procesadas = (df_final['Interval Start'].min(), df_final['Interval Start'].max())

        delete = execute_step(4, delete_by_date, dates=fechas_procesadas, id_database=0, id_table=3)
        if delete is None: return False

        insert = execute_step(5, insert_mssql, data=df_final, id_database=0, id_table=3)
        if insert is None: return False        

        logger.log_range_date(fechas_procesadas)        
        execute_step(7, exec_SP_mssql, msg_boolean=True, id_database=0, id_procedure=1)

        logger.log_final_success()
        return True
        
    except Exception as e:
        logger.log_error(8, e)
        return False
    
reporte_logueos()

