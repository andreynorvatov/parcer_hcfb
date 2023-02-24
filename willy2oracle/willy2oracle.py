# -*- coding: utf-8 -*-
import jaydebeapi
import cx_Oracle
from datetime import datetime, timedelta
import timing

import argparse

parser = argparse.ArgumentParser(description='Process test number')
parser.add_argument('--test', dest='test_number', action='store',
                    help='Test number')

args = parser.parse_args()
test_number = int(args.test_number)

########################################################################################################################

perfmon_con = cx_Oracle.Connection(user="PERFDATAPOOL", password="QWEVJASK01UIdfghjnz9",
                                   dsn="PERFT.LOAD.homecredit.ru/PERFT.HOMECREDIT.RU")

########################################################################################################################

perftool_tests_trunc_cursor = perfmon_con.cursor()
perftool_tests_trunc_cursor_req = "TRUNCATE TABLE PERFDATAPOOL.TMP_QRM_TESTS"
perftool_tests_trunc_cursor.execute(perftool_tests_trunc_cursor_req)
perftool_tests_trunc_cursor.close()

########################################################################################################################

perftool_tests_cursor = perfmon_con.cursor()
perftool_get_test_time_req = '''
SELECT
	tests.END_RAMPUP_TIME start_time,
	tests.END_TIME end_time,
	tests.ENV_ID AS env
FROM PERFMON.PTE_TESTS tests
WHERE TEST_NUMBER = :p_test_number
'''
res_test_info = perftool_tests_cursor.execute(perftool_get_test_time_req, {'p_test_number': test_number})
res_fetch = res_test_info.fetchall()
d_start = res_fetch[0][0]
d_end = res_fetch[0][1]

if res_fetch[0][2] == 1:
    agents = "^os-360[1,2].*"  # LOAD1
else:
    agents = "^os-360[3,4].*"  # LOAD2

perftool_tests_cursor.close()

########################################################################################################################

host = "os-3061.homecredit.ru"
port = "5001"
username = "loaduser"
password = "loaduser"

jdbc_class_name = "com.wily.introscope.jdbc.IntroscopeDriver"
jdbc_driver_loc = "C:\\app\\jdbc\\\IntroscopeJDBC.jar"
jdbc_url = 'jdbc:introscope:net//{0}:{1}@{2}:{3}'.format(username, password, host, port)

conn = jaydebeapi.connect(jdbc_class_name,
                          jdbc_url,
                          [username, password],
                          jdbc_driver_loc)

########################################################################################################################
# Корректировка смещения времени на час в тестовом Wily
d_start += timedelta(hours=1)
d_end += timedelta(hours=1)

str_start_time = datetime.strftime(d_start, '%Y/%m/%d %H:%M:%S')
str_end_time = datetime.strftime(d_end, '%Y/%m/%d %H:%M:%S')


sqlAvg = "select * from metric_data where agent='" + agents \
         + "' and metric='.*Average Response Time \(ms\).*'  and timestamp between '" \
         + str_start_time +"' and '" + str_end_time + "' maxmaaggregateall"
sqlRpi = "select * from metric_data where agent='" \
         + agents + "' and metric='.*Responses Per Interval.*'  and timestamp between '" \
         + str_start_time +"' and '" + str_end_time +"' maxmaaggregateall"

########################################################################################################################


########################################################################################################################

curs = conn.cursor()
curs.executeUnprepared(sqlAvg)
res = curs.fetchall()
perfmon_cursor = perfmon_con.cursor()
query_ins1 = """
INSERT INTO PERFDATAPOOL.TMP_QRM_TESTS("Domain",
                                       "Host",
                                       PROCESS,
                                       AGENTNAME,
                                       Res,
                                       METRICNAME,
                                       RECORD_TYPE,
                                       PERIOD,
                                       INTENDED_END_TIMESTAMP,
                                       ACTUAL_START_TIMESTAMP,
                                       ACTUAL_END_TIMESTAMP,
                                       COUNT,
                                       "Type",
                                       VALUE,
                                       MIN,
                                       MAX,
                                       STRING_VALUE)
VALUES(:p_domain,
       :p_host,
       :p_process,
       :p_agentname,
       :p_resource,
       :p_metricname,
       :p_record_type,
       :p_period,
       to_date(:p_intended_end_timestamp,'YYYY-MM-DD HH24:MI:SS'),
       to_date(:p_actual_start_timestamp,'YYYY-MM-DD HH24:MI:SS'),
       to_date(:p_actual_end_timestamp,'YYYY-MM-DD HH24:MI:SS'),
       :p_count,
       :p_type,
       :p_value,
       :p_min,
       :p_max,
       TO_CHAR(:p_string_value))
"""

for rec in res:
    perfmon_cursor.execute(query_ins1,
                           {'p_domain': rec[0],  # 'SuperDomain'
                            'p_host': rec[1],  # 'ra-vx42'
                            'p_process': rec[2],  # 'WebLogic'
                            'p_agentname': rec[3],  # 'load1/cluster/load1_mng5'
                            'p_resource': rec[4],  # 'Frontends|Apps|ru/HomeR/CIF/ProxyService/ClientWSProxy|URLs|Default'
                            'p_metricname': rec[5],  # 'Average Response Time (ms)'
                            'p_record_type': rec[6],  # '?'
                            'p_period': rec[7],  # 3600
                            'p_intended_end_timestamp': rec[8],  # '2018-03-21 10:37:00'
                            'p_actual_start_timestamp': rec[9],  # '2018-03-21 10:37:00'
                            'p_actual_end_timestamp': rec[10],  # '2018-03-21 11:37:00'
                            'p_count': rec[11],  # 1030
                            'p_type': rec[12],  # 268436481
                            'p_value': rec[13],  # 231
                            'p_min': rec[14],  # 56
                            'p_max': rec[15],  # 1095
                            'p_string_value': rec[16]})
perfmon_cursor.close()
perfmon_con.commit()
########################################################################################################################
curs2 = conn.cursor()
curs2.executeUnprepared(sqlRpi)
res = curs2.fetchall()
perfmon_cursor2 = perfmon_con.cursor()

query_ins2 = """
INSERT INTO PERFDATAPOOL.TMP_QRM_TESTS("Domain",
                                       "Host",
                                       PROCESS,
                                       AGENTNAME,
                                       Res,
                                       METRICNAME,
                                       RECORD_TYPE,
                                       PERIOD,
                                       INTENDED_END_TIMESTAMP,
                                       ACTUAL_START_TIMESTAMP,
                                       ACTUAL_END_TIMESTAMP,
                                       COUNT,
                                       "Type",
                                       VALUE,
                                       MIN,
                                       MAX,
                                       STRING_VALUE)
VALUES(:p_domain,
       :p_host,
       :p_process,
       :p_agentname,
       :p_resource,
       :p_metricname,
       :p_record_type,
       :p_period,
       to_date(:p_intended_end_timestamp,'YYYY-MM-DD HH24:MI:SS'),
       to_date(:p_actual_start_timestamp,'YYYY-MM-DD HH24:MI:SS'),
       to_date(:p_actual_end_timestamp,'YYYY-MM-DD HH24:MI:SS'),
       :p_count,
       :p_type,
       :p_value,
       :p_min,
       :p_max,
       TO_CHAR(:p_string_value)                         )
"""

for rec in res:
    perfmon_cursor2.execute(query_ins2,
                           {'p_domain': rec[0],  # 'SuperDomain'
                            'p_host': rec[1],  # 'ra-vx42'
                            'p_process': rec[2],  # 'WebLogic'
                            'p_agentname': rec[3],  # 'load1/cluster/load1_mng5'
                            'p_resource': rec[4],  # 'Frontends|Apps|ru/HomeR/CIF/ProxyService/ClientWSProxy|URLs|Default'
                            'p_metricname': rec[5],  # 'Average Response Time (ms)'
                            'p_record_type': rec[6],  # '?'
                            'p_period': rec[7],  # 3600
                            'p_intended_end_timestamp': rec[8],  # '2018-03-21 10:37:00'
                            'p_actual_start_timestamp': rec[9],  # '2018-03-21 10:37:00'
                            'p_actual_end_timestamp': rec[10],  # '2018-03-21 11:37:00'
                            'p_count': rec[11],  # 1030
                            'p_type': rec[12],  # 268436481
                            'p_value': rec[13],  # 231
                            'p_min': rec[14],  # 56
                            'p_max': rec[15],  # 1095
                            'p_string_value': rec[16]})
perfmon_cursor2.close()
perfmon_con.commit()
curs.close()
perfmon_con.close()
conn.close()