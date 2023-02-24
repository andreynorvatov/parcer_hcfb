import cx_Oracle
import os

# from test_settings import *

env = 'L1'

test_date = '01.08.2022'
test_time_start = '17:11'
test_time_end = '19:21'


lap_db_credentials = {
    'db_user_name': 'strmon',
    'db_pwd' : 'strmon_15',
    'db_name_for_L1': 'DBSTRES1.HOMECREDIT.RU/LAP85.HOMECREDIT.RU',
    'db_name_for_L2': "os-1440.HOMECREDIT.RU/LAP95.HOMECREDIT.RU"
}

sms_count_dict = {
    'CREDIT_CARD_RELEASE_IS_APPROVED': 0,
    'CREDIT_IS_APPROVED': 0,
    'CREDIT_IS_ISSUED': 0,
    'CREDIT_IS_ISSUED_ON_OTHER_BANK_ACCOUNT': 0,
    'EHUB_KARTA_POPOLNENIE': 0,
    'EHUB_KARTA_POPOLNENIE_OF': 0,
    'EHUB_KARTA_POPOLNENIE_OFF_PUSH': 0,
    'EHUB_KARTA_POPOLNENIE_PUSH': 0,
    'EHUB_KNPK_POPOLNENIE': 0,
    'EHUB_KNPK_POPOLNENIE_OF': 0,
    'EHUB_KNPK_POPOLNENIE_OF_PUSH': 0,
    'EHUB_KNPK_POPOLNENIE_PUSH': 0,
    'HOMER_CREDITCARD_REJECT': 0,
    'MFO_APPROVE':0,
    'MFO_REFUSE':0,
    'PK_NK_APPR': 0,
    'PK_NK_PRE_APPR': 0,
    'PK_NK_WLCM': 0,
    'RK_APPR': 0,
    'RK_WLCM': 0,
    'TWCMS_DEBET_CARD_APPL_SVYAZNOY':0
}


def db_query_for_after_test_sms(env: str, lap_db_credentials: dict, sms_count_dict: dict, test_date: str, test_time_start: str, test_time_end: str) -> dict:
    """
    Запрос в БД LAP для получения количества СМС за указанный промежуток времени.
    Результат работы функци: заполненный словарь sms_count_dict.
    """

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

    # Форматирование дат для SQL запроса

    test_start = test_date + " " + test_time_start
    test_stop = test_date + " " + test_time_end

    "Текст SQL запроса в БД"
    sql_query_text = f"SELECT COUNT(ID_EVENT), TEMPLATE FROM EVENT_HUB.SMS s WHERE INS_TIME BETWEEN to_date ('{test_start}', 'dd.mm.yyyy hh24:mi') AND to_date ('{test_stop}',	'dd.mm.yyyy hh24:mi') GROUP BY TEMPLATE ORDER BY TEMPLATE"

    "Исполнение курсор"
    cursor.execute(sql_query_text)

    """
    Запись результата работы запроса в переменную sql_query_result: list, sql_query_result[0]: tuple.
    Ожидаемая структура данных: [(153, 'PK_NK_WLCM'), (229, 'RK_APPR'), (220, 'RK_WLCM')]
    """
    sql_query_result = cursor.fetchall()

    """
    Перебор всх значений из sql_query_result и добавление в словарь sms_count_dict,
    если ключа нет, выводится сообщение "Новая СМС, название: sms_name, количество: sms_count" и 
    происходит добавление в словарь sms_count_dict
    """
    for sms_data in sql_query_result:       

        if sms_data[1] not in sms_count_dict:
            sms_count_dict[sms_data[1]] = sms_data[0]
            print(
                f'Новая СМС, название: {sms_data[1]}, количество: {sms_data[0]}')

        sms_count_dict[sms_data[1]] = sms_data[0]
    
    db_connection.commit()
    return sms_count_dict



db_query_for_after_test_sms(env, lap_db_credentials, sms_count_dict, test_date, test_time_start, test_time_end)

lst = []

for key, value in sms_count_dict.items():
    if value != 0:
        lst.append(value)
        print(f'{key}: {value}')

sum = 0        
for l in lst:
    sum += l

print(f"Всего сообщений:{sum}")