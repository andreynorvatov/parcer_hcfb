from datetime import datetime, timedelta

from test_settings import *

#?_______Settings______#

# standart_number = '5735'
# standart_date = '07.06.2022'
# standart_time_start = '13:30'
# standart_time_end = '14:30'

# test_number = '5752'
# test_date = '16.06.2022'
# test_time_start = '12:40'
# test_time_end = '13:40'



round_minutes = 6 # Округление по минуте (default = 6)


result_dict = {
    "first_string" : "",
    "second_string" : "",
    "third_string" : "",
    "fourth_string" : "",
    "fifth_string" : ""
}

def date_time_converter(test_time: str, is_start: bool, round_minutes: int) -> list:
    time_list = [] # ['10:40', '-|+', '1-5', 'в разгон|от начала теста|в афтертест|от окончания теста']
    
    # вычисление округленного времени
    time_format = datetime.strptime(test_time, '%H:%M')
    discard = timedelta(minutes=time_format.minute % 10)
    round_time = time_format - discard    
    if discard >= timedelta(minutes=round_minutes):
          round_time += timedelta(minutes=10)

    # вычисление разницы в случае округления в бОльшую сторону
    if discard >= timedelta(minutes=round_minutes):
        discard = round_time - discard
        discard = timedelta(minutes=discard.minute % 10)    

    # Добавление округленого времени в результирующий список на позицию time_list[0]      
    time_list.append(datetime.time(round_time).strftime('%H:%M'))
     
    if is_start: # если старт теста
        if datetime.time(round_time) < datetime.time(time_format): # если округленное значение времени меньше (-)
            time_list.append("+")
            time_list.append(list(str(discard))[3])
            time_list.append("в разгон")
        else: # если округленное значение времени больше (+)
            time_list.append("-")
            time_list.append(list(str(discard))[3])
            time_list.append("от начала теста")
    else:
        # print(f"GHBYN {datetime.time(round_time) - datetime.time(time_format)}")
        if datetime.time(round_time) < datetime.time(time_format): # если округленное значение времени меньше (-)
            time_list.append("-")
            time_list.append(list(str(discard))[3])    
            time_list.append("от окончания теста")
        else: # если округленное значение времени больше (+)
            time_list.append("+")
            time_list.append(list(str(discard))[3])
            time_list.append("в афтертест")

    return time_list

    

def main():
    standart_time_list_start = date_time_converter(standart_time_start, True, round_minutes)
    standart_time_list_end = date_time_converter(standart_time_end, False, round_minutes)
    test_time_list_start = date_time_converter(test_time_start, True, round_minutes)
    test_time_list_end = date_time_converter(test_time_end, False, round_minutes)

    result_dict["first_string"] = f"{standart_number} {standart_date} {standart_time_start} ({standart_time_list_start[0]}) - {standart_time_end} ({standart_time_list_end[0]})"
    result_dict["second_string"] = f"{test_number} {test_date} {test_time_start} ({test_time_list_start[0]}) - {test_time_end} ({test_time_list_end[0]})"
    result_dict["fourth_string"] = f"В AWR эталона {standart_time_list_start[1]}{standart_time_list_start[2]} мин. {standart_time_list_start[3]}, {standart_time_list_end[1]}{standart_time_list_end[2]} мин. {standart_time_list_end[3]}"
    result_dict["fifth_string"] = f"В AWR теста {test_time_list_start[1]}{test_time_list_start[2]} мин. {test_time_list_start[3]}, {test_time_list_end[1]}{test_time_list_end[2]} мин. {test_time_list_end[3]}"

    for key, value in result_dict.items():
        print(value)

if __name__ == "__main__":
    main()


'''
5447  03.03.2022  10:42 (10:40) - 11:42 (11:40)
5484  15.03.2022  13:29 (13:30) - 14:29 (14:30)

В AWR эталона +2 мин. в разгон, -2 мин. от окончания теста
В AWR теста -1 мин. от начала теста, +1 мин. в афтертест

округленное время 4 шт
+ или -
кол-во минут при округлении
в разгон/от начала
от окончания/в афтертест
'''
