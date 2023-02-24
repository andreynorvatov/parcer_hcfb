#!/usr/bin/python3
#********************* WORK WITH BLOB *********************************************************************
#author Valery T. Demidov
#***********************************************************************************************************************
import sys, cx_Oracle, logging, os


class command_param:
    param = {}

    def __init__(self, param_string : str = ""):
        if param_string != "":
            try:
                for pr in param_string.split("--"):
                    if pr.strip() !="":
                        self.param.update({pr.strip().split("=")[0]:pr[pr.find("=") + 1:] if pr.find("=") > -1 else ""})
            except: pass
    #*******************************************************************************************************************
    def pget(self, param_name : str = "") -> str:
        result = ""
        if param_name != "":
            try: result = self.param.get(param_name)
            except: pass
        return(result)
    #*******************************************************************************************************************
    def pset(self, param_name : str = "", pvalue = None)  -> bool:
        result = False
        if param_name != "":
            try: self.param.update({param_name : pvalue})
            except: pass

        return(result)
        
def InitializeLog(file_name):
    cons_log_output = True
    if file_name:
        logging.basicConfig(filename=file_name,
                            format="%(asctime)s: %(levelname)s - %(message)s",
                            # level = logging.DEBUG,
                            level=logging.INFO,
                            datefmt="%d.%m.%Y %H:%M:%S")
    cons_hnd = logging.StreamHandler()
    cons_hnd.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt="%d.%m.%Y %H:%M:%S"))
    logging.getLogger().addHandler(cons_hnd)

def main():
    dir = "C:/temp" # Директория для выгрузки
    cmd_prm.param["dbparam"] = "scs/TUNGUSKA2012@SCAN"
    cmd_prm.param["sqlstat"] = """


select tdata.data,doc.objectno from Timagedoc doc
inner join timagedata tdata on tdata.IMAGEDOCID=doc.id
join timagedata d on d.imagedocid=doc.id
where doc.OBJECTNO in
(
'2339346630',
'2339472358',
'2340891916',
'2340644671',
'2339203480',
'2339570091',
'2340161887',
'2339052523',
'2339437622',
'5003353302',
'5003410095',
'2340583315',
'2339897177',
'2339334951',
'2339776484',
'2340498168',
'2340936209',
'2339608553',
'2340373339'

)

"""

    num_blob = 1
    fname_num = 2

    try: num_blob = int(cmd_prm.pget("num_blob")) if cmd_prm.pget("num_blob") else 1
    except:pass
    try: name_num = int(cmd_prm.pget("fname_num")) if cmd_prm.pget("fname_num") else 2
    except: pass


    # --db_param=username/pwd@tns_alias --sqlstat="select tdata.data,doc.objectno from Timagedoc doc
    # inner join timagedata tdata on tdata.IMAGEDOCID=doc.id and tdata.pageno=1
    # join timagedata d on d.imagedocid=doc.id
    # where doc.createdate between to_date('01.02.2020','dd.mm.yyyy') and to_date('08.02.2020','dd.mm.yyyy')
    # and doc.doctypeid=19" --num_blob=1 --fname_num=2

    if cmd_prm.pget("dbparam") or cmd_prm.pget("sqlstat"):
        try:
            uname = cmd_prm.pget("dbparam").split("@")[0].strip().split("/")[0].strip()
            pwd = cmd_prm.pget("dbparam").split("@")[0].strip().split("/")[1].strip()
            dbname = cmd_prm.pget("dbparam").split("@")[1].strip()

            # Коннект к БД
            ora_con = cx_Oracle.connect(user=uname,
                                        password=pwd,
                                        dsn=dbname,
                                        threaded=True)
            # ora_con = cx_Oracle.connect(user='scs',
            #                             password='пароль',
            #                             dsn='scAN',
            #                             threaded=True)
            ora_con.module = "get_blob"
            ora_con.client_identifier = "get_blob"
            cp = ora_con.cursor()
            logging.info("executing statement")
            cp.execute(cmd_prm.pget("sqlstat"))
            ora_rows = cp.fetchall()

            logging.info("Total fetched {} rows".format(len(ora_rows)))

            for ora_row in ora_rows:
                try:
                    blob = ora_row[num_blob - 1].read()
                    fname = os.path.normpath("{}/{}".format(dir, ora_row[fname_num-1]))
                    open(fname, "wb").write(blob)
                    logging.info("Success file: {}".format(fname))
                except Exception as e:
                    logging.info("Error writing blob {}".format(e))
            cp.close()
            try:
                if ora_rows[0][0] > 0: res = 1
            except:
                pass
        except Exception as e:
            logging.error("DB: {}, ORA connection error - {} ".format(dbname, e))
        finally:
            try:
                ora_con.close()
            except:
                pass

cmd_str = ""
for cm in sys.argv[1:]: cmd_str += " " + cm
cmd_prm = command_param(cmd_str)

InitializeLog("get_blob.log")
logging.info("Begin ...")

if __name__ == "__main__": main()
logging.info("end ...")