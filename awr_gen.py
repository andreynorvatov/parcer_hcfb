import logging
import cx_Oracle
from datetime import datetime, timedelta
from time import time
from tqdm import tqdm

from test_settings import *
from global_vars import db_credentials_dict, lib_dir


def InitializeLog(file_name):
    cons_log_output = False
    if file_name:
        logging.basicConfig(filename=file_name,
                            format="%(asctime)s: %(levelname)s - %(message)s",
                            # level = logging.DEBUG,
                            level=logging.INFO,
                            datefmt="%d.%m.%Y %H:%M:%S")
    if cons_log_output:
        cons_hnd = logging.StreamHandler()
        cons_hnd.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt="%d.%m.%Y %H:%M:%S"))
        logging.getLogger().addHandler(cons_hnd)



class Awr_genertor:
    def __init__(self, db_credentials, env, date_time_parameters, standart_number, test_number):
        self.db_credentials = db_credentials
        self.env = env
        self.date_time_parameters = date_time_parameters
        self.standart_number = standart_number
        self.test_number = test_number
        
        self.db_connection = cx_Oracle.connect(
            user=self.db_credentials['db_user_name'],
            password=self.db_credentials['db_pwd'],
            dsn=self.db_credentials['db_name_for_L1' if self.env == 'L1' else 'db_name_for_L2'],
            # dsn=self.db_credentials['db_name_for_L2'],
            encoding='UTF-8'
        )

        self.sql_awr_query_result = ""
    
    @property
    def db_credentials(self):
        return self._db_credentials
   
    @db_credentials.setter
    def db_credentials(self, new_db_credentials):
        Awr_genertor.credentials_check_value(new_db_credentials)
        self._db_credentials = new_db_credentials    

    def credentials_check_value(value):
        if isinstance(value, dict):
            logging.info(f"DB {value['db_name']} credentials is valid")
            return True
        else:
            logging.info(f"DB's credentials IS NOT VALID")
            raise ValueError
    
    @property
    def env(self):
        return self._env
    
    @env.setter
    def env(self, new_env):
        self._env = new_env

    @property
    def date_time_parameters(self):
        return self._date_time_parameters
    
    @date_time_parameters.setter
    def date_time_parameters(self, new_date_time_parameters):
        # Awr_genertor.date_time_parameters_check_value(new_date_time_parameters)
        self._date_time_parameters = new_date_time_parameters
    
    def date_time_parameters_check_value(value):
        if isinstance(value, dict):
            logging.info(f"date_time_parameters is valid")
            return True
        else:
            logging.info(f"date_time_parameters IS NOT VALID")
            raise ValueError

    @property
    def standart_number(self):
        return self._standart_number
    
    @standart_number.setter
    def standart_number(self, new_standart_number):
        self._standart_number = new_standart_number

    @property
    def test_number(self):
        return self._test_number
    
    @test_number.setter
    def test_number(self, new_test_number):
        self._test_number = new_test_number

    def sql_db_query(self, sql_query: str):
        """Метд для выполнения запроса в БД.
        На вход подается текст SQL запроса.
        Возвращает результат запроса в виде"""

        cursor = self.db_connection.cursor()
        sql_db_query_text = sql_query
        # print(sql_query)
        cursor.execute(sql_db_query_text)
        sql_db_query_result = cursor.fetchall()
        self.db_connection.commit()

        return sql_db_query_result

    def snap_select(self, start_time: str, end_time: str) -> int:
        """Метод для подготовки номеров снепшотов (начала и окончания).
        На вход подается дата начала и дата окончания.
        Возвращает результат запроса 2-ух int занчений"""

        query_text = f"select min(snap_id), max(snap_id) from dba_hist_snapshot ds where ds.end_interval_time between to_date('{start_time}', 'yyyy-mm-dd hh24:mi:ss') and to_date('{end_time}', 'yyyy-mm-dd hh24:mi:ss')"
        snap_begin, snap_end = Awr_genertor.sql_db_query(self, sql_query=query_text)[0]
        snap_end = str(int(snap_begin) + 6)
        return snap_begin, snap_end
    

    def awr_generator(self):
        """Метод для полчения dif-awr отчета.
        На вход подается время начала и окончания периода.
        На выходе в параметр присваивается dif-awr отчет str.
        """
  
        standart_snap_begin, standart_snap_end = Awr_genertor.snap_select(self, start_time = self.date_time_parameters['standart_start_time'], end_time=self.date_time_parameters['standart_end_time'])
        test_snap_begin, test_snap_end = Awr_genertor.snap_select(self, start_time = self.date_time_parameters['test_start_time'], end_time=self.date_time_parameters['test_end_time'])
        logging.info(f"{self.db_credentials['db_name']} snap's selected successful, test_snap_begin {test_snap_begin}, test_snap_end {test_snap_end}")
        cluster_db_query_text = f"SELECT output FROM TABLE(dbms_workload_repository.awr_global_diff_report_html({self.db_credentials['dbid']}, NULL, {standart_snap_begin}, {standart_snap_end}, {self.db_credentials['dbid']}, NULL, {test_snap_begin}, {test_snap_end}))"
        single_instance_db_query_text = f"SELECT output FROM TABLE (dbms_workload_repository.awr_diff_report_html({self.db_credentials['dbid']}, 1, {standart_snap_begin}, {standart_snap_end}, {self.db_credentials['dbid']}, 1, {test_snap_begin}, {test_snap_end}))"
        self.sql_awr_query_result =  Awr_genertor.sql_db_query(self, sql_query=cluster_db_query_text if self.db_credentials['Oracle_RAC'] is True else single_instance_db_query_text)
        logging.info(f"{self.db_credentials['db_name']} AWR data selected successful")

        return self.sql_awr_query_result
    
    
    def html_file_writer(self):
        file_path_and_name = ''.join(['data/', self.db_credentials['db_name'], self.db_credentials['db_number_for_L1' if self.env ==
                                'L1' else 'db_number_for_L2'], '_AWR_HOMER_',self.standart_number, '_vs_', self.test_number, '.html'])
        
        with open(file_path_and_name, 'a', encoding='utf-8') as html_file:            
            logging.info(f"File '{file_path_and_name}' start writing . . .")
            for columns in self.sql_awr_query_result:
                for row in columns:
                    if row is not None:
                        html_file.write(row.strip())                        
                    else:
                        html_file.write('\n')
        logging.info(f"File '{file_path_and_name}' writing successful")



def date_time_concat(standart_date: str, standart_time_start: str, standart_time_end: str, test_date: str, test_time_start: str, test_time_end: str, date_time_parameters: dict) -> dict:
    date_time_parameters['standart_start_time'] = " ".join([standart_date, standart_time_start])
    date_time_parameters['standart_end_time'] = " ".join([standart_date, standart_time_end])
    date_time_parameters ['test_start_time'] = " ".join([test_date,test_time_start])
    date_time_parameters ['test_end_time'] = " ".join([test_date, test_time_end])
    
    return date_time_parameters


def date_time_converter(date_time_parameters: dict):       
    """Функиця для округления времени.
    На вход подается словарь со значениями 'дата время', str
    На выходе округленные значения в формате yyyy-mm-dd hh24:mi.
    Округление: 5 мин. в меньшую сторону
    (прим: 10:05 == 10:00, 10:06 == 10:10)"""

    for time_key, time_value in date_time_parameters.items():        
        time_value_in_datetime_format = datetime.strptime(date_time_parameters[time_key], '%d.%m.%Y %H:%M')
        discard = timedelta(minutes=time_value_in_datetime_format.minute % 10)
        time_value_in_datetime_format -= discard

        if discard >= timedelta(minutes=6):
            time_value_in_datetime_format += timedelta(minutes=10)

        if time_key in ['standart_end_time', 'test_end_time']:
            time_value_in_datetime_format += timedelta(minutes=1)
        date_time_parameters[time_key] = time_value_in_datetime_format

    return date_time_parameters 


def main():
    logging.info(f"DB name list: {', '.join(db_name_list)}")

    cx_Oracle.init_oracle_client(lib_dir)
    logging.info(f"cx_Orcale client initialization successful")

    for db_name in tqdm(db_name_list, desc='AWR\'s ready', ncols=100 , colour='BLUE'):
        logging.info(f"Start generate AWR for DB {db_name}")

        instance_of_awr_generator = Awr_genertor(
            db_credentials = db_credentials_dict[db_name],
            env = env,
            date_time_parameters=date_time_parameters,
            standart_number=standart_number,
            test_number=test_number
            )        

        instance_of_awr_generator.awr_generator()
        instance_of_awr_generator.html_file_writer()

 
time_script_start = time()

InitializeLog("z_test.log")
logging.info(f"Begin ...")


#? Данные на вход

# env = 'L1'

# standart_number = '5555'
# standart_date = '04.07.2022'
# standart_time_start = '13:00'
# standart_time_end = '14:00'

# test_number = '9999'
# test_date = '04.07.2022'
# test_time_start = '14:00'
# test_time_end = '15:00'

date_time_parameters = {}


db_name_list = ["CIF", "DTS", "LAP", "SCAN", "HOMER"]
# db_name_list = ["CIF", "DTS", "LAP", "SCAN"]
# db_name_list = ["DTS", "LAP", "SCAN", "HOMER"]
# db_name_list = ["CIF", "LAP", "HOMER"]
# db_name_list = ["DTS", "SCAN"]
# db_name_list = ["CIF"]
# db_name_list = ["DTS"]
# db_name_list = ["LAP"]
# db_name_list = ["SCAN"]
# db_name_list = ["HOMER"]

if __name__ == "__main__":
    date_time_concat(standart_date, standart_time_start, standart_time_end, test_date, test_time_start, test_time_end, date_time_parameters)
    date_time_converter(date_time_parameters)
    main()

logging.info(f"end at {round(time()-time_script_start, 2)} sec ...")


"""

LOAD1
180 sec 
163 sec
235 sec
196.24 sec
189.55 sec
216.66 sec
169.15 sec
195.3 sec
160.88 sec
150.91 sec
170.27 sec
--------
LOAD2
306.17 sec
264.77 sec
"""