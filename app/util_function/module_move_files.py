# -*- coding: utf-8 -*-

from os import path, getenv
from util_function.module_config import ConfigJson
import shutil

def move_files(id_path_files:int, name_file:str):
    """
    PATH_ORIGIN : ruta origen donde se encuentra alojado el archivo
    PATH_DESTINATION : ruta destino a donde se moverá el archivo
    name_file : nombre del archivo (este valor proviende del modulo lis files)
    return: Boolean
    """

    # 1. Set files
    files = ConfigJson().get_content_json_date(file_json='path_files')["files"][id_path_files]
    PATH_ORIGIN      = files['PATH_ORIGIN']
    PATH_DESTINATION = files['PATH_DESTINATION']
    TYPE_FILE        = files['TYPE_FILE']
    
    # 2. Crear carpeta de destino si no existe
    import os
    if not os.path.exists(PATH_DESTINATION):
        os.makedirs(PATH_DESTINATION)
        print(f'INFO: Carpeta creada: {PATH_DESTINATION}')
    
    # 2. Verificar si el archivo existe antes de mover
    # Asegurar que las rutas tengan el separador correcto
    if not PATH_ORIGIN.endswith('/'):
        PATH_ORIGIN += '/'
    if not PATH_DESTINATION.endswith('/'):
        PATH_DESTINATION += '/'
        
    source_file = PATH_ORIGIN + name_file
    destination_file = PATH_DESTINATION + name_file
    
    if not path.exists(source_file):
        print(f"WARNING: El archivo {source_file} no existe, posiblemente ya fue procesado")
        return True
    
    # 3. File moved to process
    shutil.move(source_file, destination_file)
    print('INFO: File moved to process')
        
    return True
        
    
def move_files_custom(id_path_files:int, name_file:str, prefijo: str):
    """
    PATH_ORIGIN : ruta origen donde se encuentra alojado el archivo
    PATH_DESTINATION : ruta destino a donde se moverá el archivo
    name_file : nombre del archivo (este valor proviende del modulo lis files)
    return: Boolean
    """

    # 1. Set files
    files = ConfigJson().get_content_json_date(file_json='path_files')["files"][id_path_files]
    PATH_ORIGIN      = files['PATH_ORIGIN']
    PATH_DESTINATION = files['PATH_DESTINATION']
    TYPE_FILE        = files['TYPE_FILE']
    
    # 2. File moved to process
    print(PATH_DESTINATION + str(prefijo) + name_file)
    shutil.move(PATH_ORIGIN + name_file , PATH_DESTINATION + str(prefijo) + name_file )
    
    print('INFO: File moved to process')
        
