import re

# Словарь для информации из наименований файлов в директории
file_name_data = {}


def awr_file_list_to_file_name_data(awr_file_list: list, file_name_data: dict, test_date: str, test_time_start: str, test_time_end: str, release: str) -> dict:
    """
    Функция для заполнения словаря данных из наименований файлов и входных параметров.
    На выходе словарь file_name_data
    """
    for file in awr_file_list:
        info_list = re.split("_|\.", file)
        db_name = info_list[0][0:-2]
        file_name_data[db_name] = {}
        file_name_data[db_name]["env"] = 'L1' if info_list[0][-2:] == '85' else 'L2'
        file_name_data[db_name]["standart"] = int(info_list[3])
        file_name_data[db_name]["test_number"] = int(info_list[5])
        file_name_data[db_name]["date"] = test_date
        file_name_data[db_name]["test_time"] = test_time_start + "-" + test_time_end
        file_name_data[db_name]["url_or_txt"] = info_list[-1]
        file_name_data[db_name]["file_name"] = file
        file_name_data[db_name]['release'] = release
    return file_name_data


"""
Вид словаря file_name_data
file_name_data ={
    "CIF":{
        "env":"L1",
        "standart":1234,
        "test_number":4567,
        "date":'18.10.2021',
        'test_time':'15:55-16:55',
        "url_or_txt":"url",
        "file_name":"CIF85_AWR_HOMER_4946_vs_4957.html.url",
        "release" : "21.11.1"
    },
    "DTS":{
        "env":"L1",
        "standart":1234,
        "test":4567,
        "url_or_txt":"url",
        "file_name":"DTS85_AWR_HOMER_4946_vs_4957.html.url",
        "release" : "21.11.1"
    }
}

for key in file_name_data3.values():
    print(key['file_name'])

"""
