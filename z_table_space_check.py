import cx_Oracle
import os

sql_query_text = 'select NAME from v$database' 

sql_query_text =""" 
SELECT 
tablespace_name,
SUM(CASE WHEN AUTOEXTENSIBLE='YES' THEN round(MAXBYTES/1024/1024, 0) ELSE 0 END) AS "AVAILABLE_EXTENSIBLE",
SUM(CASE WHEN AUTOEXTENSIBLE='YES' AND MAXBYTES=0 THEN 1 ELSE 0 END) AS "Сheck" --проверка, если авторасширение есть, но объем=0
FROM dba_data_files
group by tablespace_name
ORDER BY tablespace_name
"""


db_credentials_L1 = {
    'CIF85': 'DBSTRES1.HOMECREDIT.RU/CIF85.HOMECREDIT.RU',
    'DTS85': 'os-4797.homecredit.ru/DTS85',
    'LAP85': 'DBSTRES1.HOMECREDIT.RU/LAP85.HOMECREDIT.RU',
    'SCAN85': 'os-4797.homecredit.ru/SCAN85',
    'HOMER85': 'os-5347.homecredit.ru:1521/HOMER85_RAC.HOMECREDIT.RU',
}


db_credentials_L2 = {
    'CIF95': 'os-1440/CIF95.HOMECREDIT.RU',
    'DTS95': 'OS-0708.HOMECREDIT.RU/DTS95',
    'LAP95': 'os-1440.HOMECREDIT.RU/LAP95.HOMECREDIT.RU',
    'SCAN95': 'os-0708.homecredit.ru/SCAN95',
    'HOMER95': 'DBSTRES1.HOMECREDIT.RU/HOMER95.HOMECREDIT.RU'
}

db_user_name = 'strmon'
db_user_pwd = 'strmon_15'

result_dict = {}

def db_query(db_credentials: dict, db_user_name: str, db_user_pwd: str, sql_query_text: str, result_dict: dict) -> dict:
    """
    Для заброса запроса по всем БД
    """
    "Настроечные параметры для cx_Oracle"
    lib_dir = r'C:\\Oracle Instant Client\\instantclient_21_3'
    cx_Oracle.init_oracle_client(lib_dir)

    for db_name in db_credentials.keys():
        "Подключение к БД в зависимости от тестового окружения"
        db_connection = cx_Oracle.connect(
            user=db_user_name,
            password=db_user_pwd,
            dsn=db_credentials[db_name],
            encoding='UTF-8'
        )

        "Инициализация курсора"
        cursor = db_connection.cursor()

        "Исполнение курсора"
        cursor.execute(sql_query_text)

        """
        Запись результата работы запроса в переменную sql_query_result: list, sql_query_result[0]: tuple.
        Ожидаемая структура данных: [(153, 'PK_NK_WLCM'), (229, 'RK_APPR'), (220, 'RK_WLCM')]
        """
        sql_query_result = cursor.fetchall()

        # print(sql_query_result)

        result_dict[db_name]=sql_query_result



    """
    Перебор всх значений из sql_query_result и добавление в словарь sms_count_dict,
    если ключа нет, выводится сообщение "Новая СМС, название: sms_name, количество: sms_count" и 
    происходит добавление в словарь sms_count_dict
    """
    # for sms_data in sql_query_result:
    #     sms_count_dict[sms_data[1]] = sms_data[0]

    #     if sms_data[1] not in sms_count_dict:
    #         print(
    #             f'Новая СМС, название: {sms_data[1]}, количество: {sms_data[0]}')

    return result_dict


# print(db_query(db_credentials_L2, db_user_name, db_user_pwd, sql_query_text, result_dict))


# l = [('LARGE_DATA', 321536, 0), ('LARGE_IDX', 224768, 0), ('MIDDLE_DATA', 873779, 0), ('MIDDLE_IDX', 163835, 0), ('MVLOGS', 32000, 0), ('SMALL_DATA', 262138, 0), ('SMALL_IDX', 259838, 0), ('SYSAUX', 97536, 0), ('SYSTEM', 32000, 0), ('TBS_AUDIT', 32000, 0), ('TOOLS', 32000, 0), ('UNDOTBS1', 32768, 0), ('UNDOTBS2',
# 32000, 0), ('USERS', 32000, 0)]

# li = ['CIF', 'LAP', 'SCAN']

# r = {}

# for i in li:
#     r[i]=2

# print(r)

r = {'CIF95': [('LARGE_DATA', 321536, 0), ('LARGE_IDX', 224768, 0), ('MIDDLE_DATA', 873779, 0), ('MIDDLE_IDX', 163835, 0), ('MVLOGS', 32000, 0), ('SMALL_DATA', 262138, 0), ('SMALL_IDX', 259838, 0), ('SYSAUX', 97536, 0), ('SYSTEM', 32000, 0), ('TBS_AUDIT', 32000, 0), ('TOOLS', 32000, 0), ('UNDOTBS1', 32768, 0), ('UNDOTBS2', 32000, 0), ('USERS', 32000, 0)], 'DTS95': [('AUDIT_DATA', 30720, 0), ('LARGE_DATA', 98301, 0), ('LARGE_IDX', 114684, 0), ('MIDDLE_DATA', 26624, 0), ('MIDDLE_IDX', 57342, 0), ('MVLOGS', 0, 0), ('SMALL_DATA', 37120, 0), ('SMALL_IDX', 16383, 0), ('SYSAUX', 32768, 0), ('SYSTEM', 32768, 0), ('TOOLS', 4096, 0), ('UNDOTBS1', 32768, 0), ('USERS', 2048, 0)], 'LAP95': [('LARGE_DATA', 327612, 0), ('LARGE_IDX', 145408, 0), ('MIDDLE_DATA', 40960, 0), ('MIDDLE_IDX', 32768, 0), ('SMALL_DATA', 8192, 0), ('SMALL_IDX', 4096, 0), ('SYSAUX', 65534, 0), ('SYSTEM', 16383, 0), ('TBS_AUDIT', 32767, 0), ('TOOLS', 3072, 0), ('UNDOTBS1', 32768, 0), ('UNDOTBS2', 16384, 0), ('USERS', 0, 0)], 'SCAN95': [('LARGE_DATA', 98301, 0), ('LARGE_IDX', 0, 0), ('MIDDLE_DATA', 65400, 0), ('MIDDLE_IDX', 0, 0), ('SMALL_DATA', 0, 0), ('SMALL_IDX', 0, 0), ('SYSAUX', 0, 0), ('SYSTEM', 0, 0), ('TBS_AUDIT', 2048, 0), ('TOOLS', 0, 0), ('UNDOTBS1', 65536, 0),
('USERS', 0, 0)], 'HOMER95': [('ARCH_DATA', 65536, 0), ('ARCH_IDX', 0, 0), ('LARGE_DATA', 1015808, 0), ('LARGE_DATA2', 1032192, 0), ('LARGE_IDX', 753664, 0), ('MIDDLE_DATA', 0, 0), ('MIDDLE_IDX', 131072, 0), ('MVLOGS', 65536, 0), ('SMALL_DATA', 114688, 0), ('SMALL_IDX', 114688, 0), ('SYSAUX', 49152, 0), ('SYSTEM', 0, 0), ('TOOLS', 65536, 0), ('UNDOTBS11', 0, 0), ('UNDOTBS2', 212992, 0), ('UNDOTBS3', 0, 0), ('USERS', 16384, 0)]}

