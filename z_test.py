# import locale
# locale.setlocale(locale.LC_ALL, '')


# a=1000.15
# b=2
# c=0

# def summ(a, b):
#     c = a+b
#     return c

# def plus_one(q):
#     c = q +1
#     return c

# summ(a,b)

# g = plus_one(c)

# print(g)

# print(locale.format_string('%.1f', a, grouping=True))


# value = '123'

# if 's' in value or 'm' in value:
#     print('s or m in value')
# else:
#     print('NO')

# a = '1.2'

# b = float(a)

# print(b)


# import time

# """
# "gte":1642065540000,"lte":1642069140000,
#       1642065540000       1642069140000
#       1642065540.0
#       1642065540.0
# """

# date_time = '2022-01-13 12:19:00'

# test_date = '13.01.2022'
# test_time_start = '12:19'
# test_time_end = '13:19'

# left_time_bound_prepare = time.strptime(test_date + ' ' + test_time_start, '%d.%m.%Y %H:%M')
# right_time_bound_prepare = time.strptime(test_date + ' ' + test_time_end, '%d.%m.%Y %H:%M')
# struct_left_time_bound = round(time.mktime(left_time_bound_prepare)) * 1000
# struct_right_time_bound = round(time.mktime(right_time_bound_prepare)) * 1000

# print(struct_left_time_bound)
# print(struct_right_time_bound)


# struct_time = time.strptime('13/01/2022 12:19:00', '%d/%m/%Y %H:%M:%S')

# print(round(time.mktime(struct_time))*1000)




# cach = [1, 1 ,1 ,2]

# k = 1

# s = set(cach) # только уникальные значения отсортированные по возрастанию
# print(f's = {s}')
# max_s = max(s)-1
# print(f'max_s = {max_s}')
# v = [i for i in cach if i >= k] # числа, из которых можно вычесть k
# print(f'v = {v}')
# count_v = len(v)
# print(f'count_v = {count_v}')
# max_v = max(v)
# print(f'max_v = {max_v}')
# d = {}
# count = 0
# if count_v > 1:
#       for i in s:
#             if i+k >= max_v:
#                   d[i]=None
# elif count_v == 1:
#       for i in s:
#             if i+k > max_s and i != k:
#                   d[i]=None


# print(d)


# max = max(cach)
# min_max = max - k
# count_max = cach.count(max)

# # print(max, min_max, count_max)

# s = set(cach)
# d = {}

# for i in s:
#       d[i]=i+k

# answer = []
# count = 0

# for c in cach:      
#       if count_max == 1:
#             if d[c] > min_max:
#                   # print(d[c])
#                   answer.append(count + 1)

#       else:
#             if d[c] > max:
#                   answer.append(count + 1)
#       count += 1
#       print(count)


# # print(s)
# # print(d)
# print(answer)

# import logging


# def InitializeLog(file_name):
#     cons_log_output = True
#     if file_name:
#         logging.basicConfig(filename=file_name,
#                             format="%(asctime)s: %(levelname)s - %(message)s",
#                             # level = logging.DEBUG,
#                             level=logging.INFO,
#                             datefmt="%d.%m.%Y %H:%M:%S")
#     cons_hnd = logging.StreamHandler()
#     cons_hnd.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt="%d.%m.%Y %H:%M:%S"))
#     logging.getLogger().addHandler(cons_hnd)


# def div(a, b):
#       print(f"{a}, {b}")
#       try:
#             return a/b
#       except ZeroDivisionError as z:
#             print("THIS")
#             logging.error(f"Foo div:{b} = 0!")

# InitializeLog("z_test.log")
# logging.info("Begin ...")
# print(div(1, 0))
# print("Строка после всего")   
# 
#          



# class Rectangle:
#       def __init__(self, height, width) -> None:
#           self.height = height
#           self.width = width
      
#       @property
#       def width(self):
#             return self._width
      
#       @property
#       def height(self):
#             return self._height

#       @height.setter
#       def height(self, new_height):
#             Rectangle.check_value(new_height)
#             self._height = new_height
#             logging.info(f"Set new height = {new_height}")
      
#       @width.setter
#       def width(self, new_width):
#             Rectangle.check_value(new_width)
#             self._width = new_width
#             logging.info(f"Set new width = {new_width}")      

#       def area(self):
#             logging.info(f"Area of rectangle = {self.height * self.width}") 
#             return self.height * self.width

#       def check_value(value):
#             if value <= 0:
#                   try:
#                         raise Exception
#                   except Exception:
#                      logging.error(f"Value {value} <= 0!")   

#                   # logging.error(f"Value {value} <= 0!")
#                   # raise Exception
                  


# InitializeLog("z_test.log")
# logging.info("Begin ...") 
# rect = Rectangle(3,0)

# print(f"Вывод в консоль, площадь четрехугольника: {rect.area()}")

# a = 'test2'

# file = ''.join([a, '.html'])
# print(file)

# with open(file, 'a', encoding='utf-8') as html_file:
#       html_file.write(file)
      # html_file.write('<h2>Тесты участвующие в сравнении:</h2><p>'+str(tests_pass)+'<p>')
      # html_file.write(df_filter.to_html())


# import collections

# c = collections.Counter()

# for word in ['spam', 'egg', 'spam', 'counter', 'counter', 'counter']:
#      c[word] += 1

# print(c)

# a = [(322446, 322452)]

# c = a[0]

# print(c, type(c))

# s = f"String for number {c}"

# print(s)



# from datetime import datetime, timedelta




# date_time_parameters = {
#     'standart_date_start' : '14.02.2022',
#     'standart_time_start' : '18:09',
#     'standart_time_end' : '19:09',
#     'test_date_start' : '03.03.2022',
#     'test_time_star_' : '10:42',
#     'test_end_time' : '11:42'
# }

# tm = " ".join([date_time_parameters['standart_date_start'], date_time_parameters['standart_time_start']]) 

# # tm = '03.03.2022 10:42'

# t = datetime.strptime(tm, '%d.%m.%Y %H:%M')
# print(t)


# discard = timedelta(minutes=t.minute % 10)
# t -= discard
# if discard >= timedelta(minutes=6):
#       t += timedelta(minutes=10)
# t += timedelta(minutes=1)

# print(t, type(t))


# string = f"select * from dba_jobs where id like {t}"

# print(string)

# import numpy as np

# print(np.array([1,2,3])) # [1 2 3]
# print(np.linspace(0, 100, 5)) # [  0.  25.  50.  75. 100.]
# print(np.linspace(0, 100, 5)[1]) # 25.0

# import asyncio
# from re import T
# import time


# def list_comprehantion(x):
#       return [i for i in range(x)]
      

# # ~ 1.3s
# if __name__ == '__main__':
#       lis = [2000000, 2000000, 2000000, 2000000, 2000000]
#       start_time = time.time()
#       for i in lis:
#             list_comprehantion(i)
           

#       print(f'Выполнено  за {time.time() - start_time} секунд')




# async def list_comprehantion(x):
#       return [i for i in range(x)]


# async def main():
#       start_time = time.time()
#       task_1 = asyncio.create_task(list_comprehantion(2000000))
#       task_2 = asyncio.create_task(list_comprehantion(2000000))
#       task_3 = asyncio.create_task(list_comprehantion(2000000))
#       task_4 = asyncio.create_task(list_comprehantion(2000000))
#       task_5 = asyncio.create_task(list_comprehantion(2000000))

#       await asyncio.gather(task_1, task_2, task_3, task_4, task_5)

#       print(f'Выполнено  за {time.time() - start_time} секунд')


# if __name__ == '__main__':
#       asyncio.run(main())


# from colorama import init, Fore
# from colorama import Back
# from colorama import Style

# init(autoreset=True)


# def text_colorizer(b):
#       if b < 15:
#             return Style.RESET_ALL
#       elif 15 <= b < 25:
#             return Back.YELLOW + Fore.BLACK + Style.DIM
#       elif b >= 25:
#             return Fore.RED



# a = 10
# b = 16

# print(
#       f"{text_colorizer(b)}Печатаем значение а {a} -> b {b} "
# )

# print(Fore.BLUE + 'some red text')
# print(Back.WHITE + 'and with a green background')
# print(Style.BRIGHT + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')

import time
from tqdm import tqdm

mylist = [1,2,3,4,5,6,7,8]

for i in tqdm(mylist, desc='AWR\'s ready', ncols=100 , colour='BLUE'):
    time.sleep(0.5)