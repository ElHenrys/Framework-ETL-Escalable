from os import listdir
from os.path import isfile
from os import path, getenv
from util_function.module_config import ConfigJson
# from util_function.module_logger_wfm import ETLLogger
import fnmatch


def list_files(id_path_files, logger=None):
    """
    PATH_ORIGIN: ruta origen del archivo
    TYPE_FILE: extension del archivo
    return: Lista
    """
    try:
        # 1. Set path files
        files = ConfigJson().get_content_json_date(file_json='path_files')["files"][id_path_files]
        print(files)
        PATH_ORIGIN = files['PATH_ORIGIN']
        TYPE_FILE = files['TYPE_FILE']
        
        # 2. Asegurar que la ruta termine con separador
        if not PATH_ORIGIN.endswith('/'):
            PATH_ORIGIN += '/'
        
        # 3. Si TYPE_FILE está vacío, listar todos los archivos
        if TYPE_FILE == "":
            return [obj for obj in listdir(PATH_ORIGIN) if isfile(PATH_ORIGIN + obj)]
        else:
            return [obj for obj in listdir(PATH_ORIGIN) if isfile(PATH_ORIGIN + obj) and obj.endswith(TYPE_FILE)]
    
    except Exception as e:
        error_msg = f"Error al validar archivos: {e}"
        print(f"❌ ERROR: {error_msg}")
        
        if logger:
            logger.log_error(1, Exception(error_msg))
            
        return [], False


def list_files_by_pattern(id_path_files: int, patron: str, logger=None):
    """
    Lista archivos en un directorio y los filtra mediante un patrón (ej. '*bookstore*.parquet').
    
    Args:
        id_path_files (int): ID del directorio en path_files.json
        patron (str): Patrón de búsqueda (ej: '*bookstore*.parquet')
        logger (ETLLogger, optional): Logger para registrar errores
        
    Returns:
        list: Lista de archivos encontrados que coinciden con el patrón
    """
    try:
        # 1. Set path files
        files = ConfigJson().get_content_json_date(file_json='path_files')["files"][id_path_files]
        PATH_ORIGIN = files['PATH_ORIGIN']
        
        # 2. Asegurar que la ruta termine con separador
        if not PATH_ORIGIN.endswith('/'):
            PATH_ORIGIN += '/'
        
        # 3. Listar todos los archivos y aplicar el filtro por patrón
        all_files = [obj for obj in listdir(PATH_ORIGIN) if isfile(PATH_ORIGIN + obj)]
        matched_files = fnmatch.filter(all_files, patron)
        
        return matched_files
    
    except Exception as e:
        error_msg = f"Error al listar archivos con patrón '{patron}': {e}"
        print(f"❌ ERROR: {error_msg}")
        
        if logger:
            logger.log_error(1, Exception(error_msg))
            
        return []
                      

def list_files_with_validation(id_path_files, required_files, logger=None):
    """
    Lista archivos y valida que todos los archivos requeridos estén presentes.
    Registra automáticamente errores si faltan archivos.
    
    Args:
        id_path_files (int): ID del directorio en path_files.json
        required_files (list): Lista de archivos requeridos
        logger (ETLLogger, optional): Logger para registrar errores
        
    Returns:
        tuple: (archivos_encontrados, validacion_exitosa)
    """
    try:
        # Listar archivos disponibles
        available_files = list_files(id_path_files)
        
        # Validar que todos los archivos requeridos estén presentes
        missing_files = [file for file in required_files if file not in available_files]
        
        if missing_files:
            alert_msg = f"Archivos faltantes: {missing_files}. Archivos requeridos: {required_files}, Archivos encontrados: {available_files}"
            print(f"ALERTA: {alert_msg}")
            
            # Registrar alerta en el logger si está disponible
            if logger:
                logger.log_alert(1, alert_msg)
            
            return available_files, False
        
        return available_files, True
        
    except Exception as e:
        error_msg = f"Error al validar archivos: {e}"
        print(f"❌ ERROR: {error_msg}")
        
        if logger:
            logger.log_error(1, Exception(error_msg))
            
        return [], False
                      