"""
TODO
+1. Проверка валидности спарсенных данных
+2. Настроить функицию принта в консоль
+3. Добавить данные по релизу
+3.1. Добавить колонку по релизу в шаблон эксель
+3.2. Новый шаблон для чистовика
+4. Сделать фунцию data_node_balance_excel_writer
+4.1. Добавить новые данные в awr_stat_dict
-5. Подумать про if __name__ == '__main__'::
-6. В эксель-writer добавить добавление формул в файл
+7. Вынести путь до файла ексель для записи в settings
+8. Форматирование ячеек Числовой, с разделением разрядов и 2 знаками дробной части
+9. Функция проверки на отработку Джоба по смскам
+9.1 Сделать не зависимым от наличия AWR файла Homer
+10. Console print вывод до десятых
+11. Не работает уведомелнние о новых типах СМС
Для v.3.0
+1. Анализ WS количество, время
+2. Подумать про time ms или s
+3. Запись в эксель данных
+4. Добавить функию по подсчету кол-ва смс в после тестовый период и вывод в консоль (отдельный файл)
-5. Переработать модуль смс, на предмет учета и добаления смс за после-тестовый период в эксель
Для v.4.0
11. Универсальный алгоритм парсинга данных AWR (для кластерных и одиночных БД)
+12. Подготовка AWR-отчетов скриптом
+12.1. Логировнаие операций
12.2. Замеры времени для запрососв в БД (не асинхронных)
12.3. asyncio для асинхронных запросов в БД
-13. Подумать над GUI
14. Перевод на ООП
15. Подумать про if __name__ == '__main__'::
+16. Анализ (сравнение) метрик методов с выводом в консоль
16.1 Фильтр на значительные изменения метрик
+17. Расчет времени теста (преамбула отчета)
18. Вынос глобалных настроек в global_vars.py
Для v.5.0
19. Рефакторинг и объединение модулей в единый скрипт
20. Подготовка файла для отчета "1234.txt"
20.1. Преамбула
20.2. AWR
20.3. WS времена и кол-во
20.4. Аппаратные метрики (не реализовано, брать из ER отчета)
"""