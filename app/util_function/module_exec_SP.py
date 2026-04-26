import pyodbc 
from os import path, getenv
from util_function.module_config import ConfigJson

def exec_SP_mssql(id_database: int, id_procedure: int, *args, **kwargs):
    """
    Ejecuta un stored procedure en SQL Server.
    
    :param id_database: Índice del database en config
    :param id_procedure: Índice del procedimiento en config
    :return: Boolean
    """
    # Extraer msg_boolean si se envía por retrocompatibilidad, 
    # para evitar enviarlo a la base de datos como un parámetro de SQL.
    kwargs.pop("msg_boolean", None)

    # 1. Configuración de base de datos
    file_database = ConfigJson().get_content_json_date(file_json='db')["database"][id_database]
    host = getenv(file_database['HOST'])
    name = getenv(file_database['NAME'])
    user = getenv(file_database['USER'])
    password = getenv(file_database['PASSWORD'])
    driver   = file_database['DRIVER']

    # 2. Set id procedure
    file_procedure = ConfigJson().get_content_json_date(file_json='store_procedure')["procedures"][id_procedure]
    name_procedure = file_procedure['name_procedure']
       
    connection_string = "DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (
        driver, host, name, user, password
    )
    
    con = pyodbc.connect(connection_string)
    cursor = con.cursor()

    print(f"### Ejecutando procedimiento almacenado: {name_procedure} ...")

    # Combinar parámetros posicionales y nombrados restantes (en el orden proporcionado)
    params = list(args) + list(kwargs.values())

    # Construir y ejecutar la consulta usando marcadores seguros '?'
    if params:
        placeholders = ", ".join(["?"] * len(params))
        sql = f"{name_procedure} {placeholders}"
        print(f"Parámetros usados: {params}")
        cursor.execute(sql, params)
    else:
        cursor.execute(name_procedure)
        print("Sin parámetros.")

    con.commit()
    print("✅ Ejecución completada correctamente")
        
