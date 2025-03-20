import ibm_db
import ibm_db_dbi
import pandas as pd

# Подключение к DB2
DB2_DSN = "DATABASE=medstat;HOSTNAME=172.86.2.71;PORT=51230;PROTOCOL=TCPIP;UID=123132;PWD=123123;"

def get_db2_data():
    """Выполняет SQL-запрос к DB2 и возвращает данные в виде списка словарей."""
    conn = ibm_db.connect(DB2_DSN, "", "")
    
    if not conn:
        raise Exception("Ошибка подключения к DB2")

    sql_query = """
        SELECT * FROM HISTORY h
        LEFT JOIN RESEARCHES r ON r.KEY_HISTORY=h.key
        LEFT JOIN RESEARCH_RESULTSR2 r2 ON r.KEY=r2.KEY_RESEARCH 
        WHERE h.HISTORYNUMBER IN ('0026','0027','58081','6857')
    """

    stmt = ibm_db.exec_immediate(conn, sql_query)
    cols = [ibm_db.field_name(stmt, i) for i in range(ibm_db.num_fields(stmt))]
    rows = []
    
    result = ibm_db.fetch_assoc(stmt)
    while result:
        rows.append({col: result[col] for col in cols})
        result = ibm_db.fetch_assoc(stmt)

    ibm_db.close(conn)
    return rows

if __name__ == "main":
    data = get_db2_data()
    print(pd.DataFrame(data))  # Выведем результат в виде таблицы