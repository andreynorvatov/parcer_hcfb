from bs4 import BeautifulSoup

jmeter_log_file_path = 'data/log.xml'

with open(jmeter_log_file_path, encoding='utf-8') as file:
    src = file.read()

    soup = BeautifulSoup(src, "lxml")

# print(soup)

sample_name_tn = soup.find('sample')
sample_name_tn2 = sample_name_tn.find('lb')


print(sample_name_tn2)