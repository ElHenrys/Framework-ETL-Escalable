from os import path, getenv
import pyodbc
from util_function.module_config import ConfigJson


def delete_by_date(dates: tuple, id_database: int, id_table: int):
    """
    msg_boolean
    :param dates:
    :param id_table:
    :param msg_boolean:
    :param id_database:
    :return: Boolean
    """
    
    date_start_segment  =dates[0]
    date_end_segment    =dates[1]

    # 1. Set id database
    file_database = ConfigJson().get_content_json_date(file_json='db')["database"][id_database]
    
    host = getenv(file_database['HOST'])
    name = getenv(file_database['NAME'])
    user = getenv(file_database['USER'])
    password = getenv(file_database['PASSWORD'])
    driver = file_database['DRIVER']

    # 2. Set table
    file_table = ConfigJson().get_content_json_date(file_json='table')["table"][id_table]
    schema = file_table['SCHEMA']
    table_name = file_table['TABLE_NAME']
    delete_by = file_table['DELETE_BY']

    query_delete = "DELETE %s.%s WHERE %s >= convert(datetime2,?) AND %s <= convert(datetime2,?)" % (schema,
                                                                table_name,
                                                                delete_by,
                                                                delete_by)
    connection_string = "DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (driver,
                                                                                host,
                                                                                name,
                                                                                user,
                                                                                password)

    con = pyodbc.connect(connection_string)
    cursor = con.cursor()
    print(f"INFO: Process Delete start {schema}.{table_name} -- {str(date_start_segment)} {str(date_end_segment)}")
    with cursor.execute(query_delete, (date_start_segment, date_end_segment)):
        print("INFO: Process Delete completed")
    con.close()

    return True



def truncate(id_database: int, id_table: int):
    """
    msg_boolean
    :param dates:
    :param id_table:
    :param msg_boolean:
    :param id_database:
    :return: Boolean
    """

    # 1. Set id database
    file_database = ConfigJson().get_content_json_date(file_json='db')["database"][id_database]
    host = getenv(file_database['HOST'])
    name = getenv(file_database['NAME'])
    user = getenv(file_database['USER'])
    password = getenv(file_database['PASSWORD'])
    driver = file_database['DRIVER']

    # 2. Set table
    file_table = ConfigJson().get_content_json_date(file_json='table')["table"][id_table]
    schema = file_table['SCHEMA']
    table_name = file_table['TABLE_NAME']

    query_delete = "TRUNCATE TABLE %s.%s" % (schema,
                                                table_name)

    connection_string = "DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (driver,
                                                                                host,
                                                                                name,
                                                                                user,
                                                                                password)

    con = pyodbc.connect(connection_string)
    cursor = con.cursor()
    print("INFO: Process Truncate start " + schema + '.' + table_name )
    with cursor.execute(query_delete):
        print("INFO: Process Truncate completed")
        
    return True



def delete_by_filename(id_database: int, id_table: int, filename: str):

    """
    msg_boolean
    :param dates:
    :param id_table:
    :param msg_boolean:
    :param id_database:
    :return: Boolean
    """

    # 1. Set id database
    file_database = ConfigJson().get_content_json_date(file_json='db')["database"][id_database]
    host = getenv(file_database['HOST'])
    name = getenv(file_database['NAME'])
    user = getenv(file_database['USER'])
    password = getenv(file_database['PASSWORD'])
    driver = file_database['DRIVER']

    # 2. Set table
    file_table = ConfigJson().get_content_json_date(file_json='table')["table"][id_table]
    schema = file_table['SCHEMA']
    table_name = file_table['TABLE_NAME']
    delete_by = file_table['DELETE_BY']


    query_delete = "DELETE FROM %s.%s WHERE %s = ?" % (schema,
                                                                table_name,
                                                                delete_by)

    connection_string = "DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (driver,
                                                                                host,
                                                                                name,
                                                                                user,
                                                                                password)

    con = pyodbc.connect(connection_string)
    cursor = con.cursor()
    print("INFO: Process Delete start " + schema + '.' + table_name +' -- ' + filename)
    cursor.execute(query_delete, (filename))
    con.commit()
    print("INFO: Process Delete completed")
    con.close()

    return True

    


def delete_all(id_database: int, id_table: int):
    """
    msg_boolean
    :param id_table:
    :param msg_boolean:
    :param id_database:
    :return: Boolean
    """
  
    # 1. Set id database
    file_database = ConfigJson().get_content_json_date(file_json='db')["database"][id_database]
    host = getenv(file_database['HOST'])
    name = getenv(file_database['NAME'])
    user = getenv(file_database['USER'])
    password = getenv(file_database['PASSWORD'])
    driver = file_database['DRIVER']

    # 2. Set table
    file_table = ConfigJson().get_content_json_date(file_json='table')["table"][id_table]
    schema = file_table['SCHEMA']
    table_name = file_table['TABLE_NAME']


    query_delete = "DELETE FROM %s.%s" % (schema,
                                                                table_name)
    connection_string = "DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (driver,
                                                                                host,
                                                                                name,
                                                                                user,
                                                                                password)

    con = pyodbc.connect(connection_string)
    cursor = con.cursor()
    print(f"INFO: Process Delete start {schema}.{table_name} ")
    with cursor.execute(query_delete):
        print("INFO: Process Delete completed")
    con.close()

    return True

