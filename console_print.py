import locale
from re import LOCALE
locale.setlocale(locale.LC_ALL, '')


def console_print(db_name: str, awr_stat_dict: dict, file_name_data: dict, cluster_db_mark: bool) -> None:
    """
    Функиця для вывода агрегированных данных AWR в консоль для отчета.
    """
    def foo(a, b):
        p = round((b-a)*100/a, 2)
        return str(p).replace(".", ",") if p <= 0 else '+'+str(p).replace(".", ",")

    print('------------------------------------------------')
    print(f"{file_name_data[db_name]['standart']}э")
    print(f"{file_name_data[db_name]['test_number']}")
    print(f"DB Name: {db_name} AWR")
    print(f"DB Time: {locale.format_string('%.2f', awr_stat_dict['standart']['db_time'], grouping=True)} -> {locale.format_string('%.2f', awr_stat_dict['test']['db_time'], grouping=True)} ({foo(awr_stat_dict['standart']['db_time'], awr_stat_dict['test']['db_time'])}%)")
    print(f"CPU Time: {locale.format_string('%.2f', awr_stat_dict['standart']['cpu_time'], grouping=True)} -> {locale.format_string('%.2f', awr_stat_dict['test']['cpu_time'], grouping=True)} ({foo(awr_stat_dict['standart']['cpu_time'], awr_stat_dict['test']['cpu_time'])}%)")
    print(f"Elapsed Time: {locale.format_string('%.2f', awr_stat_dict['standart']['elapsed_time'], grouping=True)} -> {locale.format_string('%.2f', awr_stat_dict['test']['elapsed_time'], grouping=True)} ({foo(awr_stat_dict['standart']['elapsed_time'], awr_stat_dict['test']['elapsed_time'])}%)")
    print(f"I/O Time: {locale.format_string('%.2f', awr_stat_dict['standart']['io_time'], grouping=True)} -> {locale.format_string('%.2f', awr_stat_dict['test']['io_time'], grouping=True)} ({foo(awr_stat_dict['standart']['io_time'], awr_stat_dict['test']['io_time'])}%)")
    print(f"Buffer Gets: {locale.format_string('%.2f', awr_stat_dict['standart']['buffer_gets'], grouping=True)} -> {locale.format_string('%.2f', awr_stat_dict['test']['buffer_gets'], grouping=True)} ({foo(awr_stat_dict['standart']['buffer_gets'], awr_stat_dict['test']['buffer_gets'])}%)")
    print(f"Physical Reads: {locale.format_string('%.2f', awr_stat_dict['standart']['physical_reads'], grouping=True)} -> {locale.format_string('%.2f', awr_stat_dict['test']['physical_reads'], grouping=True)} ({foo(awr_stat_dict['standart']['physical_reads'], awr_stat_dict['test']['physical_reads'])}%)")
    print(f"Captured SQL Executions: {locale.format_string('%.2f', awr_stat_dict['standart']['captured_sql_executions'], grouping=True)} -> {locale.format_string('%.2f', awr_stat_dict['test']['captured_sql_executions'], grouping=True)} ({foo(awr_stat_dict['standart']['captured_sql_executions'], awr_stat_dict['test']['captured_sql_executions'])}%)")
    if cluster_db_mark == True :
        print(f"Cluster Wait Time: {locale.format_string('%.2f', awr_stat_dict['standart']['cluster_wait_time'], grouping=True)} -> {locale.format_string('%.2f', awr_stat_dict['test']['cluster_wait_time'], grouping=True)} ({foo(awr_stat_dict['standart']['cluster_wait_time'], awr_stat_dict['test']['cluster_wait_time'])}%)")
    print()

    return None



# console_print(db_name, awr_stat_dict, file_name_data, cluster_db_mark=False)

# print(locale.format_string('%.2f', file_name_data['CIF']['test_number'], grouping=True))


"""
db_name = "CIF"

awr_stat_dict = {
    'standart': {
        'db_time': 5000,
        'cpu_time': 6000,
        'elapsed_time': 7000,
        'io_time': 8000,
        'buffer_gets': 9000,
        'physical_reads': 99999,
        'captured_sql_executions': 88888,
        'cluster_wait_time': 7777,
        'awr_elapsed_time': 5555,
        'awr_time': 0
    },
    'test': {
        'db_time': 30000,
        'cpu_time': 3333,
        'elapsed_time': 4444,
        'io_time': 5555,
        'buffer_gets': 36666,
        'physical_reads': 3134,
        'captured_sql_executions': 35454,
        'cluster_wait_time': 33545,
        'awr_elapsed_time': 3132,
        'awr_time': '11:11-12:11'
    }
}

file_name_data = {
    "CIF": {
        "env": "L1",
        "standart": 1234,
        "test_number": 4567,
        "date": '18.10.2021',
        'test_time': '15:55-16:55',
        "url_or_txt": "url",
        "file_name": "CIF85_AWR_HOMER_4946_vs_4957.html.url",
        "release": "21.11.1"
    },
    "LAP": {
        "env": "L1",
        "standart": 1234,
        "test_number": 4567,
        "date": '18.10.2021',
        'test_time': '15:55-16:55',
        "url_or_txt": "url",
        "file_name": "LAP85_AWR_HOMER_4946_vs_4957.html.url",
        "release": "21.11.1"
    }
}

"""