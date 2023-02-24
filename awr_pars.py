import os
import requests
from bs4 import BeautifulSoup
import lxml
import re
import urllib3


awr_stat_dict = {
    'standart': {
        'db_time': 0,
        'cpu_time': 0,
        'elapsed_time': 0,
        'io_time': 0,
        'buffer_gets': 0,
        'physical_reads': 0,
        'captured_sql_executions': 0,
        'cluster_wait_time': 0,
        'awr_elapsed_time': 0,
        'awr_time': 0,
        'db_time_node1': 0,
        'db_time_node2': 0,
        'avg_active_sessions_node1':0,
        'avg_active_sessions_node2':0
    },
    'test': {
        'db_time': 0,
        'cpu_time': 0,
        'elapsed_time': 0,
        'io_time': 0,
        'buffer_gets': 0,
        'physical_reads': 0,
        'captured_sql_executions': 0,
        'cluster_wait_time': 0,
        'awr_elapsed_time': 0,
        'awr_time': 0,
        'db_time_node1': 0,
        'db_time_node2': 0,
        'avg_active_sessions_node1':0,
        'avg_active_sessions_node2':0
    }
}


def soup_initial_function(awr_file_name: str, url_or_txt: str) -> BeautifulSoup:
    """
    Функция для инициализаии объека soup.
    Результат работы функции объект soup для парсинга.
    """
    awr_report = "data/"+awr_file_name
    if url_or_txt == 'url':
        "Если есть флаг 'url', то выполняется request"
        with open(awr_report) as file:
            first_line = file.readline()
            second_string = file.readline().strip()[4:]
            urllib3.disable_warnings()
            req = requests.get(second_string, verify=False)
            src = req.text
            # print(f'Тип src {type(src)}')

    else:
        "Если флаг 'url' отсутствует, то читается файл как txt "
        with open(awr_report, encoding='utf-8') as file:
            src = file.read()
    soup = BeautifulSoup(src, "lxml")

    return soup


def cluster_data_base_parser(soup: BeautifulSoup, awr_stat_dict: dict) -> dict:
    """
    Функция для парсинга кластерной БД. На вход подается объект soup и
    словарь для добавления в него данных.
    Возвращает словарь с данными из AWR-отчета
    """
    # в переменной вся таблица по инстансам
    databace_instances_included_in_report = soup.find(class_="tdiff", summary="This table displays information about database instances included in this report")
    
    # данные для 1-го инстанса эталона
    standart_first_instance_begin_snap_time = databace_instances_included_in_report.find_all("td", class_="awrc")[7].text
    standart_first_instance_end_snap_time = databace_instances_included_in_report.find_all("td", class_="awrc")[8].text
    standart_first_instance_elapsed_time = float(databace_instances_included_in_report.find_all("td", class_="awrc")[9].text)
    standart_first_instance_db_time = float(databace_instances_included_in_report.find_all("td", class_="awrc")[10].text.replace(",", ""))
    standart_first_instance_avg_active_sessions = float(databace_instances_included_in_report.find_all("td", class_="awrc")[12].text.replace(",", ""))
 
    # данные 2-го инстанса эталона
    standart_second_instance_begin_snap_time = databace_instances_included_in_report.find_all("td", class_="awrnc")[7].text
    standart_second_instance_end_snap_time = databace_instances_included_in_report.find_all("td", class_="awrnc")[8].text
    standart_second_instance_elapsed_time = float(databace_instances_included_in_report.find_all("td", class_="awrnc")[9].text)
    standart_second_instance_db_time = float(databace_instances_included_in_report.find_all("td", class_="awrnc")[10].text.replace(",", ""))
    standart_second_instance_avg_active_sessions = float(databace_instances_included_in_report.find_all("td", class_="awrnc")[12].text.replace(",", ""))
    
    # данные для 1-го инстанса теста
    test_first_instance_begin_snap_time = databace_instances_included_in_report.find_all("td", class_="awrct")[7].text
    test_first_instance_end_snap_time = databace_instances_included_in_report.find_all("td", class_="awrct")[8].text
    test_first_instance_elapsed_time = float(databace_instances_included_in_report.find_all("td", class_="awrct")[9].text)
    test_first_instance_db_time = float(databace_instances_included_in_report.find_all("td", class_="awrct")[10].text.replace(",", ""))
    test_first_instance_avg_active_sessions = float(databace_instances_included_in_report.find_all("td", class_="awrct")[12].text.replace(",", ""))

    # данные для 2-го инстанса теста
    test_second_instance_begin_snap_time = databace_instances_included_in_report.find_all("td", class_="awrnc")[21].text
    test_second_instance_end_snap_time = databace_instances_included_in_report.find_all("td", class_="awrnc")[22].text
    test_second_instance_elapsed_time = float(databace_instances_included_in_report.find_all("td", class_="awrnc")[23].text)
    test_second_instance_db_time = float(databace_instances_included_in_report.find_all("td", class_="awrnc")[24].text.replace(",", ""))
    test_second_instance_avg_active_sessions = float(databace_instances_included_in_report.find_all("td", class_="awrnc")[26].text.replace(",", ""))

    # Топы по запросам (общие данные)

    # ожидаемое значение 75
    ul_tags = soup.find_all("ul")

    # топ Elapsed time
    top_sql_elapsed_time_notation = ul_tags[20].find_all("li")
    top_sql_elapsed_time_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_elapsed_time_notation[4].text)

    standart_top_sql_elapsed_time_summ = float(top_sql_elapsed_time_summ[0][0].replace(",", ""))
    test_top_sql_elapsed_time_summ = float(top_sql_elapsed_time_summ[1][0].replace(",", ""))

    # топ CPU Time
    top_sql_cpu_time_notation = ul_tags[21].find_all("li")
    top_sql_cpu_time_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_cpu_time_notation[3].text)

    standart_top_sql_cpu_time_summ = float(top_sql_cpu_time_summ[0][0].replace(",", ""))
    test_top_sql_cpu_time_summ = float(top_sql_cpu_time_summ[1][0].replace(",", ""))

    # топ IO Time
    top_sql_io_time_notation = ul_tags[22].find_all("li")
    top_sql_io_time_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_io_time_notation[4].text)

    standart_top_sql_io_time_summ = float(top_sql_io_time_summ[0][0].replace(",", ""))
    test_top_sql_io_time_summ = float(top_sql_io_time_summ[1][0].replace(",", ""))

    # топ Buffer Gets
    top_sql_buffer_gets_notation = ul_tags[23].find_all("li")
    top_sql_buffer_gets_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_buffer_gets_notation[3].text)

    standart_top_sql_buffer_gets_summ = float(top_sql_buffer_gets_summ[0][0].replace(",", ""))
    test_top_sql_buffer_gets_summ = float(top_sql_buffer_gets_summ[1][0].replace(",", ""))

    # топ Physical Reads
    top_sql_physical_reads_notation = ul_tags[24].find_all("li")
    top_sql_physical_reads_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_physical_reads_notation[4].text)

    standart_top_sql_physical_reads_summ = float(top_sql_physical_reads_summ[0][0].replace(",", ""))
    test_top_sql_physical_reads_summ = float(top_sql_physical_reads_summ[1][0].replace(",", ""))

    # топ Executions
    top_sql_executions_notation = ul_tags[26].find_all("li")
    top_sql_executions_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_executions_notation[2].text)

    standart_top_sql_executions_summ = float(top_sql_executions_summ[0][0].replace(",", ""))
    test_top_sql_executions_summ = float(top_sql_executions_summ[1][0].replace(",", ""))

    # топ Cluster wait taime
    top_sql_cluser_wait_time_notation = ul_tags[30].find_all("li")
    top_sql_cluser_wait_time_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_cluser_wait_time_notation[4].text)

    standart_top_sql_cluser_wait_time_summ = float(top_sql_cluser_wait_time_summ[0][0].replace(",", ""))
    test_top_sql_cluser_wait_time_summ = float(top_sql_cluser_wait_time_summ[1][0].replace(",", ""))

    """
    Добавление данныв в словарь
    """
    awr_stat_dict['standart']['db_time'] = standart_first_instance_db_time + standart_second_instance_db_time
    awr_stat_dict['standart']['cpu_time'] = standart_top_sql_cpu_time_summ
    awr_stat_dict['standart']['elapsed_time'] = standart_top_sql_elapsed_time_summ
    awr_stat_dict['standart']['io_time'] = standart_top_sql_io_time_summ
    awr_stat_dict['standart']['buffer_gets'] = standart_top_sql_buffer_gets_summ
    awr_stat_dict['standart']['physical_reads'] = standart_top_sql_physical_reads_summ
    awr_stat_dict['standart']['captured_sql_executions'] = standart_top_sql_executions_summ
    awr_stat_dict['standart']['cluster_wait_time'] = standart_top_sql_cluser_wait_time_summ
    awr_stat_dict['standart']['awr_time'] = standart_first_instance_begin_snap_time[-5:]+'-'+ standart_first_instance_end_snap_time[-5:]
    awr_stat_dict['standart']['awr_elapsed_time'] = round(standart_first_instance_elapsed_time)
    awr_stat_dict['standart']['db_time_node1'] = standart_first_instance_db_time
    awr_stat_dict['standart']['db_time_node2'] = standart_second_instance_db_time
    awr_stat_dict['standart']['avg_active_sessions_node1'] = standart_first_instance_avg_active_sessions
    awr_stat_dict['standart']['avg_active_sessions_node2'] = standart_second_instance_avg_active_sessions

    awr_stat_dict['test']['db_time'] = test_first_instance_db_time + test_second_instance_db_time
    awr_stat_dict['test']['cpu_time'] = test_top_sql_cpu_time_summ
    awr_stat_dict['test']['elapsed_time'] = test_top_sql_elapsed_time_summ
    awr_stat_dict['test']['io_time'] = test_top_sql_io_time_summ
    awr_stat_dict['test']['buffer_gets'] = test_top_sql_buffer_gets_summ
    awr_stat_dict['test']['physical_reads'] = test_top_sql_physical_reads_summ
    awr_stat_dict['test']['captured_sql_executions'] = test_top_sql_executions_summ
    awr_stat_dict['test']['cluster_wait_time'] = test_top_sql_cluser_wait_time_summ
    awr_stat_dict['test']['awr_time'] = test_first_instance_begin_snap_time[-5:]+'-'+ test_first_instance_end_snap_time[-5:]
    awr_stat_dict['test']['awr_elapsed_time'] = round(test_first_instance_elapsed_time)
    awr_stat_dict['test']['db_time_node1'] = test_first_instance_db_time
    awr_stat_dict['test']['db_time_node2'] = test_second_instance_db_time
    awr_stat_dict['test']['avg_active_sessions_node1'] = test_first_instance_avg_active_sessions
    awr_stat_dict['test']['avg_active_sessions_node2'] = test_second_instance_avg_active_sessions
    
    return awr_stat_dict


def single_instance_data_base_parser(soup: BeautifulSoup, awr_stat_dict: dict) -> dict:
    '''Функция для парсинга БД с одним инстансом'''
    
    # snapshot_table в переменной вся таблица по снэпшотам
    snapshot_table = soup.find("table", summary="This table displays snapshot information")
    
    standart_begin_snap_time = snapshot_table.find_all("td", class_="awrnc")[2].text    
    standart_end_snap_time = snapshot_table.find_all("td", class_="awrnc")[4].text
    standart_elapsed_time = float(snapshot_table.find_all("td", class_="awrnc")[6].text)
    standart_db_time = float(snapshot_table.find_all("td", class_="awrnc")[7].text)

    test_begin_snap_time = snapshot_table.find_all("td", class_="awrnc")[10].text
    test_end_snap_time = snapshot_table.find_all("td", class_="awrnc")[12].text
    test_elapsed_time = float(snapshot_table.find_all("td", class_="awrnc")[14].text)
    test_db_time = float(snapshot_table.find_all("td", class_="awrnc")[15].text)

    # Топы по запросам (общие данные)

    # ожидаемое значение 75
    ul_tags = soup.find_all("ul")

    # топ Elapsed time
    top_sql_elapsed_time_notation = ul_tags[14].find_all("li")
    top_sql_elapsed_time_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_elapsed_time_notation[4].text)

    standart_top_sql_elapsed_time_summ = float(top_sql_elapsed_time_summ[0][0].replace(",", ""))
    test_top_sql_elapsed_time_summ = float(top_sql_elapsed_time_summ[1][0].replace(",", ""))

    # топ CPU Time
    top_sql_cpu_time_notation = ul_tags[15].find_all("li")
    top_sql_cpu_time_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_cpu_time_notation[3].text)

    standart_top_sql_cpu_time_summ = float(top_sql_cpu_time_summ[0][0].replace(",", ""))
    test_top_sql_cpu_time_summ = float(top_sql_cpu_time_summ[1][0].replace(",", ""))

    # топ IO Time
    top_sql_io_time_notation = ul_tags[16].find_all("li")
    top_sql_io_time_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_io_time_notation[4].text)

    standart_top_sql_io_time_summ = float(top_sql_io_time_summ[0][0].replace(",", ""))
    test_top_sql_io_time_summ = float(top_sql_io_time_summ[1][0].replace(",", ""))

    # топ Buffer Gets
    top_sql_buffer_gets_notation = ul_tags[17].find_all("li")
    top_sql_buffer_gets_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_buffer_gets_notation[3].text)

    standart_top_sql_buffer_gets_summ = float(top_sql_buffer_gets_summ[0][0].replace(",", ""))
    test_top_sql_buffer_gets_summ = float(top_sql_buffer_gets_summ[1][0].replace(",", ""))

    # топ Physical Reads
    top_sql_physical_reads_notation = ul_tags[18].find_all("li")
    top_sql_physical_reads_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_physical_reads_notation[4].text)

    standart_top_sql_physical_reads_summ = float(top_sql_physical_reads_summ[0][0].replace(",", ""))
    test_top_sql_physical_reads_summ = float(top_sql_physical_reads_summ[1][0].replace(",", ""))

    # топ Executions
    top_sql_executions_notation = ul_tags[20].find_all("li")
    top_sql_executions_summ = re.findall(r"(\d+(,?\d+)*.\d+)", top_sql_executions_notation[2].text)

    standart_top_sql_executions_summ = float(top_sql_executions_summ[0][0].replace(",", ""))
    test_top_sql_executions_summ = float(top_sql_executions_summ[1][0].replace(",", ""))

    """
    Добавление данныв в словарь
    """
    awr_stat_dict['standart']['db_time'] = standart_db_time
    awr_stat_dict['standart']['cpu_time'] = standart_top_sql_cpu_time_summ
    awr_stat_dict['standart']['elapsed_time'] = standart_top_sql_elapsed_time_summ
    awr_stat_dict['standart']['io_time'] = standart_top_sql_io_time_summ
    awr_stat_dict['standart']['buffer_gets'] = standart_top_sql_buffer_gets_summ
    awr_stat_dict['standart']['physical_reads'] = standart_top_sql_physical_reads_summ
    awr_stat_dict['standart']['captured_sql_executions'] = standart_top_sql_executions_summ
    awr_stat_dict['standart']['awr_time'] = standart_begin_snap_time[-5:]+'-'+ standart_end_snap_time[-5:]
    awr_stat_dict['standart']['awr_elapsed_time'] = round(standart_elapsed_time)

    awr_stat_dict['test']['db_time'] = test_db_time
    awr_stat_dict['test']['cpu_time'] = test_top_sql_cpu_time_summ
    awr_stat_dict['test']['elapsed_time'] = test_top_sql_elapsed_time_summ
    awr_stat_dict['test']['io_time'] = test_top_sql_io_time_summ
    awr_stat_dict['test']['buffer_gets'] = test_top_sql_buffer_gets_summ
    awr_stat_dict['test']['physical_reads'] = test_top_sql_physical_reads_summ
    awr_stat_dict['test']['captured_sql_executions'] = test_top_sql_executions_summ
    awr_stat_dict['test']['awr_time'] = test_begin_snap_time[-14:-9]+'-'+ test_end_snap_time[-14:-9]
    awr_stat_dict['test']['awr_elapsed_time'] = round(test_elapsed_time)


    return awr_stat_dict



'''
awr_soup_object = soup_initial_function('CIF85_AWR_HOMER_4946_vs_4957.html', 'html')

cluster_data_base_parser(awr_soup_object, awr_stat_dict)

print(awr_stat_dict['test'])

cluster_db_list = ["CIF", "LAP", "HOMER"]
single_instance_db_list = ["DTS", "SCAN"]

file_name_data = {'CIF': {'env': 'L1', 'standart': 4946, 'test': 4957, 'url_or_txt': 'html', 'file_name': 'CIF85_AWR_HOMER_4946_vs_4957.html'},
'DTS': {'env': 'L1', 'standart': 4946, 'test': 4957, 'url_or_txt': 'url', 'file_name': 'DTS85_AWR_HOMER_4946_vs_4957.html.url'},
'HOMER': {'env': 'L1', 'standart': 4946, 'test': 4957,'url_or_txt': 'url', 'file_name': 'HOMER85_AWR_HOMER_4946_vs_4957.html.url'},
'LAP': {'env': 'L1', 'standart': 4946, 'test': 4957, 'url_or_txt': 'url', 'file_name': 'LAP85_AWR_HOMER_4946_vs_4957.html.url'},
'SCAN': {'env': 'L1', 'standart': 4946, 'test': 4957, 'url_or_txt': 'url', 'file_name': 'SCAN85_AWR_HOMER_4946_vs_4957.html.url'}}

'''

