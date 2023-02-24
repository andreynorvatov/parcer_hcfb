from bs4 import BeautifulSoup
import lxml
import requests
import urllib3
import pandas as pd


def soup_initial_function(awr_file_name: str, url_or_txt: str) -> BeautifulSoup:
    """
    Функция для инициализаии объека soup.
    Результат работы функции объект soup для парсинга.
    """
    awr_report = "".join(["data/", awr_file_name])

    if url_or_txt == 'url':
        # Если есть флаг 'url', то выполняется request
        with open(awr_report) as file:
            first_line = file.readline()
            url = file.readline().strip()[4:]
            urllib3.disable_warnings()
            req = requests.get(url, verify=False)
            src = req.text


    else:
        # Если флаг 'url' отсутствует, то читается файл как txt
        with open(awr_report) as file:
            src = file.read()
    soup = BeautifulSoup(src, "lxml")

    return soup

def html_to_dataframe_converter(soup):


    database_summary = soup.find(class_="tdiff", summary="This table displays top SQL comparisons by elapsed time")    
    database_summary_table = database_summary.find("tbody")
    print(database_summary_table)
    # l = []
    # for th_tag in database_summary_table:
        # print(th_tag.text)
    dfs = pd.read_html(str(database_summary))[0]
    dfs = dfs.set_index('SQL Id')
    dfs.to_excel("data/test.xlsx", sheet_name="L")
    print(dfs)


    pass


def main():
    awr_soup_object = soup_initial_function(awr_file_name, "txt") # url
    # print()
    html_to_dataframe_converter(awr_soup_object)





if __name__ == "__main__":
    awr_file_name = "CIF95_AWR_HOMER_5411_vs_5471.html"
    # awr_file_name = "DTS85_AWR_HOMER_5447_vs_5474.html.url"
    main()