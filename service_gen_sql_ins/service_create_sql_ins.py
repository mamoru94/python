import csv
import os
# Input the desired file names
base_file_name = input("Enter the base file name (without extension): ")
SAVE_PATH = r"C:\Users\a.aleksandrov.CORP\Desktop\NLMK scripts\services\service_gen_sql_ins\sql"  # Путь для сохранения файлов

def generate_sql_template(schema, table, column, data_type):
    return f"{column}"

def generate_sql_query(db_name, table, columns):
    sql_query = f"SELECT\n"
    sql_query += f"    load_id,\n"
    sql_query += f"    load_dttm,\n"
    sql_query += f"    extraction_query_id,\n"
    sql_query += f"    cast('I' as char(1)) as op_cd,\n"
    sql_query += f"    to_timestamp(load_ts, 'yyyyMMddHHmmss') AS LOAD_TS_DTTM,\n"

    for column, data_type in columns.items():
        sql_query += f"    {generate_sql_template(db_name, table, column, data_type)},\n"

    sql_query = sql_query.rstrip(",\n") + "\n"
    sql_query += f"FROM ""{p_src_tab_name" "};\n"
    return sql_query

def main():
    csv_file = f'C:/Users/a.aleksandrov.CORP/Desktop/NLMK scripts/services/service_gen_sql_ins/{base_file_name}.csv'
 
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # Пропускаем заголовок
        current_table = None
        current_columns = {}

        for row in reader:
            _, table_name, column, data_type, *_ = row

            if table_name != current_table:  # Новая таблица
                if current_table is not None:  # Если это не первая таблица
                    # Генерируем SQL для предыдущей таблицы и сохраняем в файл
                    sql_query = generate_sql_query(None, current_table, current_columns)
                    with open(os.path.join(SAVE_PATH, f"{current_table}.sql"), "w", encoding='utf-8') as sql_file:
                        sql_file.write(sql_query)

                current_table = table_name
                current_columns = {}

            current_columns[column] = data_type

        # Генерируем SQL для последней таблицы и сохраняем в файл
        if current_table is not None:
            sql_query = generate_sql_query(None, current_table, current_columns)
            with open(os.path.join(SAVE_PATH, f"{current_table}.sql"), "w", encoding='utf-8') as sql_file:
                sql_file.write(sql_query)

if __name__ == "__main__":
    main()
