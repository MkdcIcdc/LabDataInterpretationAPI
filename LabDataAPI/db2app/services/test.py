import ibm_db
import ibm_db_dbi
import pandas as pd
from db2_conn import DB2_DSN

print("ну файл запустился")
# Подключение к DB2DATABASE


def get_db2_data():
    """Выполняет SQL-запрос к DB2 и возвращает данные в виде pandas DataFrame, выводит и сохраняет в Excel."""
    print("Пытаемся подключиться...")
    conn = ibm_db.connect(DB2_DSN, "", "")

    if not conn:
        raise Exception("Ошибка подключения к DB2")

    print("Успешно подключились к DB2")

    sql_query = """    
    SELECT 
        r2.KEY_RESEARCH AS research_key, 
        r2.RESULTFORMZAKL AS patient_result, 
        r.ACTUALDATETIME AS research_date,
        h.FIRSTNAME AS first_name,
        h.MIDDLENAME AS middle_name,
        h.LASTNAME AS last_name,
        h.SEX AS gender
    FROM HISTORY h
    LEFT JOIN RESEARCHES r ON r.KEY_HISTORY = h.KEY
    LEFT JOIN RESEARCH_RESULTSR2 r2 ON r.KEY = r2.KEY_RESEARCH
    WHERE h.HISTORYNUMBER = '58081'
    ORDER BY r.ACTUALDATETIME DESC
    FETCH FIRST 5 ROWS ONLY;
    """

    # """
    # SELECT * FROM HISTORY h
    # LEFT JOIN RESEARCHES r ON r.KEY_HISTORY = h.KEY
    # LEFT JOIN RESEARCH_RESULTSR2 r2 ON r.KEY = r2.KEY_RESEARCH
    # WHERE h.HISTORYNUMBER IN ('0026','0027','58081','6857');
    # """

    stmt = ibm_db.exec_immediate(conn, sql_query)
    cols = [ibm_db.field_name(stmt, i) for i in range(ibm_db.num_fields(stmt))]
    rows = []

    result = ibm_db.fetch_assoc(stmt)
    while result:
        rows.append([result[col] for col in cols])
        result = ibm_db.fetch_assoc(stmt)

    ibm_db.close(conn)

    # Создаем DataFrame
    df = pd.DataFrame(rows, columns=cols)

    # Полный вывод без сокращений
    pd.set_option("display.max_rows", None)  # Отобразить все строки
    pd.set_option("display.max_columns", None)  # Отобразить все столбцы
    pd.set_option("display.width", 1000)  # Увеличить ширину вывода
    pd.set_option("display.max_colwidth", None)  # Полный вывод данных в ячейках

    print(df)

    # Сохранение в Excel
    excel_path = "db2_data_58081.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Данные сохранены в {excel_path}")


data = get_db2_data()
print(pd.DataFrame(data))  # Выведем результат в виде таблицы
