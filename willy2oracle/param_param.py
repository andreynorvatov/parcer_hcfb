import cx_Oracle

lap_db_credentials = {
    'db_user_name': 'strmon',
    'db_pwd': 'strmon_15',
    'db_name_for_L1': 'DBSTRES1.HOMECREDIT.RU/LAP85.HOMECREDIT.RU',
    'db_name_for_L2': "os-1440.HOMECREDIT.RU/LAP95.HOMECREDIT.RU"
}

env = 'L1'

"Настроечные параметры для cx_Oracle"
lib_dir = r'C:\\Oracle Instant Client\\instantclient_21_3'
cx_Oracle.init_oracle_client(lib_dir)

"Подключение к БД в зависимости от тестового окружения"
db_connection = cx_Oracle.connect(
    user=lap_db_credentials['db_user_name'],
    password=lap_db_credentials['db_pwd'],
    dsn=lap_db_credentials['db_name_for_L1' if env ==
                            'L1' else 'db_name_for_L2'],
    encoding='UTF-8'
)

"Инициализация курсора"
cursor = db_connection.cursor()
"Текст SQL запроса в БД"
sql_query_text = f"select * from DBA_SCHEDULER_JOBS where enabled = 'TRUE'"

"Исполнение курсор"
cursor.execute(sql_query_text)


sql_query_result = cursor.fetchall()
print(sql_query_result)
    
db_connection.commit()

