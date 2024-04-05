import xml.etree.ElementTree as ET
from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog

def xml_to_excel(xml_file, excel_file):
    # Создание нового Excel-файла
    wb = Workbook()
    ws = wb.active

    # Парсинг XML-файла
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Добавление заголовков столбцов вручную
    headers = ["Name", "Datatype", "Size", "Precision", "Scale"]
    ws.append(headers)

    # Извлечение данных из XML и запись их в Excel
    for element in root.findall('.//DIElement'):
        name = element.get('name')

        # Проверка на начало строки '$'
        if name.startswith('$'):
            continue  # Пропускаем этот элемент и переходим к следующему

        datatype = element.get('datatype')
        size = element.get('size')
        precision = element.get('precision')
        scale = element.get('scale')

        # Проверка на None перед преобразованием размера в целое число
        if size is not None:
            size = int(size)
            # Изменение размера, если datatype ='VARCHAR'
            if datatype == 'VARCHAR':
                size *= 2
        else:
            size = ''  # Пустая строка, если размер не указан

        # Преобразование типов данных в соответствии с указанными условиями
        if datatype == 'NUMERIC':
            if precision and int(precision) > 32:
                datatype = 'BIGINT'
                precision = ''  # Пустая строка, если размер не указан
            elif precision and int(precision) < 33:
                datatype = 'INTEGER'
                precision = ''  # Пустая строка, если размер не указан
        elif datatype == 'TIME':
            datatype = 'VARCHAR'
            size = '8'

        row_data = [name, datatype, str(size), precision, scale]
        ws.append(row_data)

    # Сохранение Excel-файла
    wb.save(excel_file)


def select_files():
    # Открытие диалогового окна выбора файлов
    root = tk.Tk()
    root.withdraw()

    # Выбор пути файла XML
    xml_file_path = filedialog.askopenfilename(title="Select XML File", filetypes=[("XML files", "*.xml")])
    if not xml_file_path:
        print("XML file not selected!")
        return

    # Выбор места сохранения файла Excel
    excel_file_path = filedialog.asksaveasfilename(title="Save Excel File", filetypes=[("Excel files", "*.xlsx")], defaultextension=".xlsx")
    if not excel_file_path:
        print("Excel file not saved!")
        return

    # Вызов функции для конвертации XML в Excel
    xml_to_excel(xml_file_path, excel_file_path)
    print("Conversion completed!")

# Вызов функции для выбора файлов и выполнения конвертации
select_files()
