
from util_function.module_list_files import list_files_with_validation
from util_function.module_read_files import read_file_auto
from util_function.module_move_files import move_files
from util_function.module_insert import insert_mssql
from util_function.module_exec_SP import exec_SP_mssql
from util_function.module_delete import delete_by_date
from util_function.module_logger_wfm import ETLLogger
import pandas as pd

# Parametros Iniciales para Logger
logger = ETLLogger(
    cliente="ENTEL",
    servicio="ATECIÓN AL CLIENTE"
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

def corte_Genesys():
    logger.reset()
    logger.set_reporte("Corte Genesys")
    
    files = [
        'Entel_Chile_IN_TMO.csv',
        'Entel_Chile_IN_Agentes.csv',
        'Entel_Chile_IN_Trafico.csv'
        ]
    try:
        # PASO 1: LISTAR Y VALIDAR ARCHIVOS
        listfiles, validation_success = list_files_with_validation(0, files, logger)
        if not validation_success:
            return False  

        for i in range(len(files)):
            df = execute_step(2, read_file_auto, id_path_files=0, name_file=files[i])
            if df is None: return False

            df['Inicio del intervalo'] = pd.to_datetime(df['Inicio del intervalo'], format='mixed', errors='coerce')
            df['Fin del intervalo'] = pd.to_datetime(df['Fin del intervalo'], format='mixed', errors='coerce')
            fechas_procesadas = (df['Inicio del intervalo'].min(), df['Inicio del intervalo'].max())

            delete = execute_step(4, delete_by_date, dates=fechas_procesadas,id_database=0, id_table=i)
            if delete is None: return False

            insert = execute_step(5, insert_mssql, data=df, id_database=0, id_table=i)
            if insert is None: return False        

            move_result = execute_step(6, move_files, id_path_files=0, name_file=files[i])
            if move_result is None: return False
        logger.log_range_date(fechas_procesadas)        
        # execute_step(7, exec_SP_mssql, id_database=0, id_procedure=0)
        # execute_step(7, exec_SP_mssql, msg_boolean=True, id_database=0, id_procedure=1, date_param1=fechas_procesadas[0], date_param2=fechas_procesadas[1])

        logger.log_final_success()
        return True
        
    except Exception as e:
        logger.log_error(8, e)
        return False
    
corte_Genesys()
