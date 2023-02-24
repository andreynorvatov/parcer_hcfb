import os
import re
import pandas as pd

er_excel_file_path =  'data/'

er_file_list = [file for file in os.listdir(path=er_excel_file_path) if file.startswith("HOMER_compare")]

if len(er_file_list) > 1:
    print("\n")
    print(f"WARNING!!! Много файлов в дирректории! {er_file_list}")
    print("\n")

er_excel_file_name = er_file_list[0]
standart_number = re.search(r'_(\d+)vs', er_excel_file_name).group(1)
test_number = re.search(r'vs(\d+)_', er_excel_file_name).group(1)
env = re.search(r'L(\d+)', er_excel_file_name).group(0)


print(f"Найден файл: {''.join([er_excel_file_path, er_excel_file_name])}")
print(f"Эталон: {standart_number}")
print(f"Тест: {test_number}")
print(f"Среда: {env}")
print("\n")

column_names_metrics = ['Hostname', 'Item',	'Average (Δ)',	'Average (Δ%)',	'Average (A)',	'Average (B)']
check_hosts_metrics_load1 = ["DB Node1 CIF (os-0930)", "DB Node2 CIF (os-0931)", "DB DTS,SCAN (os-4797)"]
check_hosts_metrics_load2 = ["DB Node1 CIF (os-1440)", "DB Node2 CIF (os-1533)", "DB LOG,DTS,SCAN (os-0708)"]
check_items_metrics = ['CPU used %', 'Mem used %']

column_names_agg_report = ['Label (B)', 'Average (A)', 'Average (B)', '90%Line (A)', '90%Line (B)', 'Total Count (A)', 'Total Count (B)', 'Error Count (A)', 'Error Count (B)']
label_names_agg_report = ['dboscan', 'DTS', '.identifyCustomerShortRequest']

df = {}

with pd.ExcelFile(''.join([er_excel_file_path, er_excel_file_name])) as er_report:

    df["Metrics"] = pd.read_excel(er_report, "Metrics", header=1, usecols=column_names_metrics, index_col='Hostname')
    df["Metrics"] = df["Metrics"].dropna().loc[check_hosts_metrics_load1 if env=='L1' else check_hosts_metrics_load2]
    df_metrics = df["Metrics"].query(f"Item in {check_items_metrics}")

    df["Aggregate Report (QAD)"] = pd.read_excel(er_report, "Aggregate Report (QAD)", usecols=column_names_agg_report)
    df["Aggregate Report (QAD)"] = df["Aggregate Report (QAD)"]
    df_agg_report = df["Aggregate Report (QAD)"]
    df_agg_report = df_agg_report[df_agg_report['Label (B)'].str.contains('|'.join(label_names_agg_report))]
    # print(df_agg_report.head(5))


print(f"--------HOST METRICS {test_number} -> {standart_number}--------")
for i  in df_metrics.itertuples():
    print(f"{i[0]} {i[1]}: {round(i[4], 2)} -> {round(i[5], 2)} ({ ''.join(['+', str(round(i[2], 2))]) if i[2] >= 0 else round(i[2], 2)}) (average Δ% {''.join(['+', str(round(i[3] * 100, 2))]) if i[3] >= 0 else round(i[3] * 100, 2)}%)")

print('\n')

print(f"--------AGG REPORT CHECK {test_number} -> {standart_number}--------")
print(df_agg_report)
