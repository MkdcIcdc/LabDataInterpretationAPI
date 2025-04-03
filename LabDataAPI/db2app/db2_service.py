import ibm_db
import ibm_db_dbi
import pandas as pd
from .db2_conn import DB2_DSN
 
def load_medstat_data(history_number):
    print("оказались в методе")
    conn = ibm_db.connect(DB2_DSN, "", "")
    print("если мы тут то к медстату подрубились")
    try:
        if not conn:
            raise Exception("Ошибка подключения к DB2")
        
        sql_query = f'''
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
            WHERE h.HISTORYNUMBER = '{history_number}'
            ORDER BY r.ACTUALDATETIME DESC
            FETCH FIRST 5 ROWS ONLY;
        '''
        
        stmt = ibm_db.exec_immediate(conn, sql_query)
        
        # Базовая структура для хранения данных
        medstat_data = {
            "history_number": history_number,
            "fullname": None,
            "gender": None,
            "researches": {}  # Словарь исследований по ключу research_key
        }
        
        row = ibm_db.fetch_assoc(stmt)
        
        while row:
            research_key = row.get("RESEARCH_KEY")
            patient_result = row.get("PATIENT_RESULT")
            
            # Пропускаем записи без research_key или patient_result
            if not research_key or not patient_result:
                row = ibm_db.fetch_assoc(stmt)
                continue

            # Заполняем ФИО и пол только один раз
            if medstat_data["fullname"] is None:
                medstat_data["fullname"] = f"{row['LAST_NAME']} {row['FIRST_NAME']} {row['MIDDLE_NAME']}".strip()
                medstat_data["gender"] = row["GENDER"]

            # Упаковываем данные исследования
            medstat_data["researches"][research_key] = {
                "research_date": row["RESEARCH_DATE"],
                "patient_result": patient_result
            }
            
            row = ibm_db.fetch_assoc(stmt)

        ibm_db.close(conn)

        if not medstat_data["researches"]:
            return f"Нет данных для истории {history_number}"

        return medstat_data

    except Exception as e:
        return {"error": f"Произошла ошибка: {str(e)}"}

# print(load_medstat_data("58081"))