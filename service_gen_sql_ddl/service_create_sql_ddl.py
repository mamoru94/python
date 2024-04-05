import pandas as pd

# Input the desired file names
base_file_name = input("Enter the base file name (without extension): ")

# Input the desired schema type
schema_type = input("Enter the schema type (ods_plus, dds, dim, dm): ")

# Load CSV file into DataFrame with UTF-8 encoding
csv_file_path = f'C:/Users/a.aleksandrov.CORP/Desktop/NLMK scripts/services/service_gen_sql_ddl/{base_file_name}.csv'
df = pd.read_csv(csv_file_path, encoding='utf-8', delimiter=';')

# Values to be excluded from the "COLUMN" column
values_to_exclude = ['load_id', 'load_dttm', 'extraction_query_id', 'op_cd', 'load_ts_dttm']

# Filter out rows where the "COLUMN" column has specified values
df = df[~df['COLUMN'].isin(values_to_exclude)]

# Group by "SCHEMA" and "TABLE", aggregate columns into lists
groups = df.groupby(["SCHEMA", "TABLE", "COMMENT"]).agg({"COLUMN": list, "TYPE": list, "COMMENT COLUMN": list}).reset_index()

# Dictionary to map schema types to beginning columns
schema_columns_mapping = {
    'ods_plus': [
        "load_id STRING COMMENT 'ID загрузки'",
        "load_dttm TIMESTAMP COMMENT 'Дата-время загрузки'",
        "extraction_query_id STRING COMMENT 'ID порции в источнике'",
        "op_cd CHAR(1) COMMENT 'Код операции'",
        "load_ts_dttm TIMESTAMP COMMENT 'Дата-время загрузки'",
    ],
    'dds': [
        "load_id STRING COMMENT 'ID загрузки'",
        "load_dttm TIMESTAMP COMMENT 'Дата-время загрузки'",
        "dataflow_id STRING COMMENT 'Код процесса преобразования'",
        "deleted_flg CHAR(1) COMMENT 'Флаг удалено'",
    ],
    'dds_dim_fct': [
        "load_id STRING COMMENT 'ID загрузки'",
        "load_dttm TIMESTAMP COMMENT 'Дата-время загрузки'",
        "dataflow_id STRING COMMENT 'Код процесса преобразования'",
        "valid_from_dt DATE COMMENT 'Дата действия записи С'",
        "valid_to_dt DATE COMMENT 'Дата действия записи ПО'",
        "deleted_flg CHAR(1) COMMENT 'Флаг удалено'",
    ],    
    'dim': [
        "load_id STRING COMMENT 'ID загрузки'",
        "load_dttm TIMESTAMP COMMENT 'Дата-время загрузки'",
        "valid_from_dt DATE COMMENT 'Дата действия записи С'",
        "valid_to_dt DATE COMMENT 'Дата действия записи ПО'",
        "deleted_flg CHAR(1) COMMENT 'Флаг удалено'",
    ],
    'dm': [
        "load_id STRING COMMENT 'ID загрузки'",
        "load_dttm TIMESTAMP COMMENT 'Дата-время загрузки'",
        "deleted_flg CHAR(1) COMMENT 'Флаг удалено'",
    ],
    'dm_dim': [
        "load_id STRING COMMENT 'ID загрузки'",
        "load_dttm TIMESTAMP COMMENT 'Дата-время загрузки'",
        "valid_from_dt DATE COMMENT 'Дата действия записи С'",
        "valid_to_dt DATE COMMENT 'Дата действия записи ПО'",
        "deleted_flg CHAR(1) COMMENT 'Флаг удалено'",
    ],
}

# Function to format SQL statement
def format_sql(schema, table, comment, columns_info):
    beginning_columns = schema_columns_mapping.get(schema_type, [])  # Get the columns based on schema type
    
    other_columns = [f"{column} {type_} COMMENT '{comment_info}'" for column, type_, comment_info in columns_info]

    columns = ",\n".join(beginning_columns + other_columns)
    template = "CREATE TABLE IF NOT EXISTS {schema}.{table} (\n{columns}\n)\nCOMMENT '{comment}'\nSTORED AS PARQUET\nTBLPROPERTIES ('OBJCAPABILITIES'='HIVEMANAGEDINSERTREAD,HIVEMANAGEDINSERTWRITE', 'transactional'='false', 'transactional_properties'='insert_only');"
    formatted_sql = template.format(schema=schema.strip(), table=table.strip(), comment=comment.strip(), columns=columns)
    return formatted_sql

# Generate and print SQL statements
for _, row in groups.iterrows():
    schema = row["SCHEMA"]
    table = row["TABLE"]
    comment = row["COMMENT"]
    columns_info = zip(row["COLUMN"], row["TYPE"], row["COMMENT COLUMN"])
    sentence = format_sql(schema, table, comment, columns_info)
    
    # Extract the table name from the table variable
    _, table_name = table.split('.') if '.' in table else (schema, table)

    # Save each statement to a separate file
    output_sql_file = f'C:/Users/a.aleksandrov.CORP/Desktop/NLMK scripts/services/service_gen_sql_ddl/sql/{table_name}.sql'
    with open(output_sql_file, 'w', encoding='utf-8', errors='replace') as sqlfile:
        sqlfile.write(sentence + '\n')

    print(f"SQL statement for {schema}.{table} saved to {output_sql_file}")