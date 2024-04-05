import csv
base_file_name = input("Enter the base file name (without extension): ")
def generate_code_from_csv(csv_file):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        code_blocks = []
        return_statements = {}
        for row in reader:
            source = row['source']
            target = row['target']
            fields = row['key_field_list']
            if (source, target) not in return_statements:
                return_statements[(source, target)] = []
            
            # Разделяем строку fields по запятым и удаляем лишние пробелы
            key_fields = [field.strip() for field in fields.split(',')]
            # Удаляем пустые значения, если они есть
            key_fields = [field for field in key_fields if field]
            # Формируем строку для key_field_list
            key_field_list = ', '.join(key_fields)
            return_statements[(source, target)].append(key_field_list)
        
        for (source, target), key_field_lists in return_statements.items():
            # Создаем код только если ключевые поля не пустые
            if key_field_lists:
                code_lines = []
                code_lines.append(f'    #dds.{source}__bpm_dm.{target}')
                code_lines.append('    #pylint: disable=line-too-long')
                code_lines.append(f'    l_dds_{source}__bpm_dm_{target} = generate_tg__dds2dm(')
                code_lines.append('        #pylint: disable=line-too-long')
                code_lines.append('        p_prev_results_dict=l_group_start,')
                code_lines.append(f'        p_flow_id_list=["dds.{source}__bpm_dm.{target}"],')
                code_lines.append('        flow_variables = {')
                code_lines.append('            "load_id":G_LOAD_ID,')
                code_lines.append('            "key_field_list": (')
                code_lines.append(f'                "{", ".join(key_field_lists)}"')
                code_lines.append('            ),')
                code_lines.append('            "add_tables_list":[')
                code_lines.append(f'                "dds.{source}"')
                code_lines.append('            ]')
                code_lines.append('        }')
                code_lines.append('    )')
                
                code_blocks.append('\n'.join(code_lines))
        
        # Генерация строки возвращаемого значения после выполнения основной части
        return_statement_lines = []
        for (source, target), key_field_lists in return_statements.items():
            if key_field_lists:
                return_statement_lines.append(f'        "bpm_dm_{target}": l_dds_{source}__bpm_dm_{target},')
        
        # Добавление строки возвращаемого значения
        if return_statement_lines:
            code_blocks.append("    return {")
            code_blocks.extend(return_statement_lines)
            code_blocks.append("    }")
        
        return '\n'.join(code_blocks)

def select_csv_file():
    csv_file = input("Введите путь к CSV файлу: ")
    return csv_file

def select_save_path():
    save_path = input("Введите путь для сохранения сгенерированного кода: ")
    return save_path

def select_file_name():
    file_name = input("Введите имя файла для сохранения (без расширения): ")
    return file_name

# Выбор пути к CSV файлу
csv_file = select_csv_file()
if csv_file:
    # Генерация кода из CSV файла
    generated_code = generate_code_from_csv(csv_file)
    
    # Выбор пути для сохранения
    save_path = select_save_path()
    if save_path:
        # Выбор имени файла для сохранения
        file_name = select_file_name()
        if file_name:
            # Сохранение сгенерированного кода
            with open(f'{save_path}/{file_name}.py', 'w') as file:
                file.write(generated_code)
            print("Код успешно сохранен.")
        else:
            print("Отмена сохранения. Не указано имя файла.")
    else:
        print("Отмена сохранения. Введен недопустимый путь для сохранения.")
else:
    print("Отмена операции. CSV файл не введен.")
