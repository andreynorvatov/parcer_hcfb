
"""
! Файл для хранения глобальных переменных.

? db_credentials_dict - словарь с данными для подключения к базам данных.
? lib_dir - директория с Oracle Client
"""

db_credentials_dict = { 
    "FIC" : {
        'db_name':"db_name",
        'db_user_name': 'db_user_name',
        'db_pwd': 'db_pwd',
        'db_name_for_L1': 'db_name_for_L1',
        'db_name_for_L2': "db_name_for_L2",
        'db_number_for_L1': '85',
        'db_number_for_L2': '95',
        'dbid' : 'dbid',
        'Oracle_RAC' : True
    },
    "STD" : {
        'db_name':"db_name",
        'db_user_name': 'db_user_name',
        'db_pwd': 'db_pwd',
        'db_name_for_L1': 'db_name_for_L1',
        'db_name_for_L2': "db_name_for_L2",
        'db_number_for_L1': '85',
        'db_number_for_L2': '95',
        'dbid' : 'dbid',
        'Oracle_RAC' : False
    },
    "REMOH" : {
        'db_name':"db_name",
        'db_user_name': 'db_user_name',
        'db_pwd': 'db_pwd',
        'db_name_for_L1': 'db_name_for_L1',
        'db_name_for_L2': "db_name_for_L2",
        'db_number_for_L1': '85',
        'db_number_for_L2': '95',
        'dbid' : 'dbid',
        'Oracle_RAC' : False
    }, 
    "PAL" : {
        'db_name':"db_name",
        'db_user_name': 'db_user_name',
        'db_pwd': 'db_pwd',
        'db_name_for_L1': 'db_name_for_L1',
        'db_name_for_L2': "db_name_for_L2",
        'db_number_for_L1': '85',
        'db_number_for_L2': '95',
        'dbid' : 'dbid',
        'Oracle_RAC' : False
       
    },
    "NACS" : {
        'db_name':"db_name",
        'db_user_name': 'db_user_name',
        'db_pwd': 'db_pwd',
        'db_name_for_L1': 'db_name_for_L1',
        'db_name_for_L2': "db_name_for_L2",
        'db_number_for_L1': '85',
        'db_number_for_L2': '95',
        'dbid' : 'dbid',
        'Oracle_RAC' : False
    }
}

lib_dir = r'C:\\Oracle Instant Client\\instantclient_21_3'