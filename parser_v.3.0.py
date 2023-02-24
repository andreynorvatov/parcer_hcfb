import os, time
from file_name_data import awr_file_list_to_file_name_data, file_name_data
from awr_pars import soup_initial_function, cluster_data_base_parser, single_instance_data_base_parser, awr_stat_dict
from console_print import console_print
from sms import db_query_for_sms, db_query_for_event_hub_check, lap_db_credentials, homer_db_credentials, sms_count_dict
from excel_writer import excel_writer_sms, excel_writer_awr, node_balance_data_dict_agrigator, data_node_balance_excel_writer, node_balance_data_dict
from ws_control_elstic import wl_stat_data_parcer, wl_stat_excel_writer, es, ws_methods_control_list, wl_stat_dict

from test_settings import *

#?_______Settings______#

# test_date = '16.06.2022'
# test_time_start = '12:40'
# test_time_end = '13:40'

# release = 'RT22.06.2 Final-3 long run [интервал из теста 5751]'

console_print_activator = True # True если нужно вывести данные AWR в консоль, False если нет
awr_excel_writer_activator = True # True если нужно записать данные AWR в Excel, False если нет
sms_db_query_and_excel_writer_activator = True  # True если нужно узнать кол-во смс за тест, False если нет
event_hub_check_activator = True # True если нужно проверить отработку джоба по переносу событий из Гомер в Event_hub
data_node_balance_excel_writer_activator = True # True если нужно записать разницу по нодам LAP и CIF в Excel
ws_control_elastic_activator = True # если нужно проверить метриик WS (запись в эксель)

excel_file_path = 'data/tests_results.xlsx'
path_to_awr_reports = 'data'
cluster_db_list = ["CIF", "LAP", "HOMER"]
single_instance_db_list = ["DTS", "SCAN"]




awr_file_list = [file for file in os.listdir(path=path_to_awr_reports) if '_AWR_' in file]


awr_file_list_counter = len(awr_file_list)

awr_file_list_to_file_name_data(awr_file_list, file_name_data, test_date, test_time_start, test_time_end, release)
# CIF 85 _AWR_HOMER_ 5469 _vs_ 5490 .html

for db_name in file_name_data.keys():
    """
    Основной цикл. Перебирает все файлы (AWR-отчеты БД) в словаре awr_file_name_data.
    """
    
    awr_file_name = file_name_data[db_name]['file_name']
    url_or_txt = file_name_data[db_name]['url_or_txt']

    awr_soup_object = soup_initial_function(awr_file_name, url_or_txt)

    if db_name in cluster_db_list:
        cluster_data_base_parser(awr_soup_object, awr_stat_dict)
        node_balance_data_dict_agrigator(db_name, awr_stat_dict, node_balance_data_dict, file_name_data)
        if console_print_activator is True:
            console_print(db_name, awr_stat_dict, file_name_data, cluster_db_mark=True) 
    
    else:
        single_instance_data_base_parser(awr_soup_object, awr_stat_dict)
        if console_print_activator is True:
            console_print(db_name, awr_stat_dict, file_name_data, cluster_db_mark=False)
    

   
    
    """
    Есть CIF awr_stat_dict, file_name_data['LAP']['env']
    """

    if awr_excel_writer_activator is True:
        excel_writer_awr(db_name, awr_stat_dict, file_name_data, excel_file_path)

if data_node_balance_excel_writer_activator is True:
    data_node_balance_excel_writer(excel_file_path, node_balance_data_dict)

if sms_db_query_and_excel_writer_activator is True:
    db_query_for_sms(file_name_data["LAP"]["env"], lap_db_credentials, sms_count_dict, test_date, test_time_start, test_time_end)
    excel_writer_sms(sms_count_dict, file_name_data, excel_file_path)

if event_hub_check_activator is True:
    db_query_for_event_hub_check(file_name_data["LAP"]["env"], homer_db_credentials, test_date, test_time_start, test_time_end)

if ws_control_elastic_activator is True:
    index = "load1-homer-*" if file_name_data['CIF']['env'] == 'L1' else "load2-homer-*"
    left_time_bound_prepare = time.strptime(test_date + ' ' + test_time_start, '%d.%m.%Y %H:%M')
    right_time_bound_prepare = time.strptime(test_date + ' ' + test_time_end, '%d.%m.%Y %H:%M')
    struct_left_time_bound = round(time.mktime(left_time_bound_prepare)) * 1000
    struct_right_time_bound = round(time.mktime(right_time_bound_prepare)) * 1000
    
    wl_stat_data_parcer(es, ws_methods_control_list, struct_left_time_bound, struct_right_time_bound, index)
    wl_stat_excel_writer(excel_file_path, wl_stat_dict, file_name_data)