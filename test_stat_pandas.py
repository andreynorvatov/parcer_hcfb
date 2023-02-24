import pandas as pd
import numpy as np

from colorama import init, Fore
from colorama import Back
from colorama import Style

from test_settings import *

# standart_number = '5735'
# test_number = '5752'

init(autoreset=True)

sheet_names_list = ["SMS", "WS_count", "WS_time"]
# sheet_names_list = ["SMS"]
# excel_file_path = "data/test_data.xlsx"

excel_file_path = 'data/tests_results.xlsx'

num_colunms_dict = {
    "WS_time" : 4,
    "WS_count" : 4,
    "SMS" : 6
}

def data_frame_agregator(excel_file_path, sheet_name, num_colunms_dict, standart_number, test_number):
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    df = df.set_index('Test number').fillna(0)
    df_rows = df.loc[[standart_number, test_number]]
    df_coumns  = df_rows.iloc[:, num_colunms_dict[sheet_name]-1:]
    df_transpon = df_coumns.transpose()
    df_delta = df_transpon.assign(Delta=round((df_transpon[test_number] - df_transpon[standart_number]), 0))
    df_persent_delta = df_delta.assign(Persent_delta=round((df_delta[test_number] * 100/ df_delta[standart_number] - 100), 0))
    df_result = df_persent_delta.fillna(0)

    return df_result



def console_text_colorizer_ws_time(time_delta, time_delta_pct):
    if time_delta >= 150:
        if time_delta_pct < 15:
            return Style.RESET_ALL
        elif 15 <= time_delta_pct < 25:
                return Fore.BLUE
        elif time_delta_pct >= 25:
                return Fore.RED
    else:
        return Style.RESET_ALL


def console_print(data_frame, sheet_name):
    data_frame = data_frame.replace([-np.inf, np.inf], [-100, 100])
    if sheet_name == "WS_time":
        for i  in data_frame.itertuples():
            if i[3] >= 0:
                print(f"{console_text_colorizer_ws_time(time_delta=int(i[3]), time_delta_pct=int(i[4]))}{i[0]}: {int(i[1])} -> {int(i[2])}ms (+{int(i[3])}ms, +{int(i[4])}%)")
            else:
                print(f"{i[0]}: {int(i[1])} -> {int(i[2])}ms ({int(i[3])}ms, {int(i[4])}%)")
    else:

        for i  in data_frame.itertuples():

            if i[3] >= 0:
                print(f"{i[0]}: {int(i[1])} -> {int(i[2])} (+{int(i[3])}, +{int(i[4])}%)")
            else:
                print(f"{i[0]}: {int(i[1])} -> {int(i[2])} ({int(i[3])}, {int(i[4])}%)") 


def main():    
    data_frame = 0
    for sheet_name in sheet_names_list:
        data_frame = data_frame_agregator(excel_file_path, sheet_name, num_colunms_dict, standart_number, test_number)
        print(f"{Back.YELLOW + Fore.BLACK + Style.DIM}------{sheet_name}-------")
        console_print(data_frame, sheet_name)
        

  
if __name__ == "__main__":
    standart_number = int(standart_number)
    test_number = int(test_number)
    main()
    


# num_colunms = 4 # количество столбцов не для расчета (WS_time, WS_count)
# num_colunms = 6 # количество столбцов не для расчета (SMS)

# standart_number = int(standart_number)
# test_number = int(test_number)

# df = pd.read_excel("data/test_data.xlsx", sheet_name="WS")


# df_modif = df.set_index('Test number').fillna(0) #? Установка в качестве индекса требуемый столбец
# print(df_modif)
# print()
# df_rows = df_modif.loc[[standart_number, test_number]]
# print(df_rows)
# print()
# df_coumns  = df_rows.iloc[:, num_colunms-1:]
# print(df_coumns)
# print()

# df_transpon = df_coumns.transpose()
# print(df_transpon)
# print()
# df_delta = df_transpon.assign(Delta=round((df_transpon[test_number] - df_transpon[standart_number]), 0))
# print(df_delta)
# print()
# df_persent_delta = df_delta.assign(Persent_delta=round((df_delta[test_number] * 100/ df_delta[standart_number] - 100), 0))
# print(df_persent_delta)

# df_persent_delta.transpose().to_excel("data/test_data_1.xlsx", sheet_name="E")

# Печать Pandas(Index='ClientWSEndpoint#searchClientRequest', _1=384.0, _2=526.0, Delta=142.0, Persent_delta=37.0)
#CustomerWSEndpoint#getCustomerDataRequest: 100 -> 116ms (+16ms, +16%)
# for i  in df_persent_delta.itertuples():
#     if i[3] >= 0:
#         print(f"{i[0]}: {int(i[1])} -> {int(i[2])}ms (+{int(i[3])}ms, +{int(i[4])}%)")
#     else:
#         print(f"{i[0]}: {int(i[1])} -> {int(i[2])}ms ({int(i[3])}ms, {int(i[4])}%)")