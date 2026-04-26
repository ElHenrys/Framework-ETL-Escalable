from util_function.module_config import ConfigJson
from sqlalchemy import create_engine
from os import path, getenv
from pandas import DataFrame



def insert_mssql(data: DataFrame, id_database: int, id_table: int, fast_exec: bool=True):
    """
    :param id_table:
    :param data:
    :param msg_boolean:
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

    string_connect_engine = "mssql+pyodbc://%s:%s@%s:1433/%s?driver=%s" % (user,
                                                                           password,
                                                                           host,
                                                                           name,
                                                                           driver)

    engine = create_engine(string_connect_engine, pool_size=0,fast_executemany=fast_exec ,max_overflow=-1)

    print("INFO: Process of insert start ..." + schema + '.' + table_name )
    data.to_sql(table_name, engine, schema=schema, if_exists='append', chunksize=5000, index=False)
    print("✅ INFO: Process of insert completed")
    return True
