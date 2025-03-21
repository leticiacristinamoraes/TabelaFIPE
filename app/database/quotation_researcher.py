from app.database.config import get_connection
import sys
import os
import psycopg2
from datetime import datetime
import calendar

sys.path.append(os.path.abspath("app"))

def create_quotation_researcher_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quotation_researcher (
            id SERIAL PRIMARY KEY,
            consult_id INTEGER NOT NULL,
            researcher_id INTEGER NOT NULL,
            prices_id INTEGER NOT NULL,
            month VARCHAR(20) NOT NULL CHECK (month IN ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')),
            year INTEGER NOT NULL,
            FOREIGN KEY (consult_id) REFERENCES quotation_consults(id) ON DELETE CASCADE,
            FOREIGN KEY (researcher_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (prices_id) REFERENCES prices(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def save_quotation_researcher(consult_id, researcher_id, prices_id, month, year):
    """Salva uma nova cotação vinculada a uma consulta."""
    print(f"Chamando save_quotation_researcher com: {consult_id}, {researcher_id}, {prices_id}, {month}, {year}")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO quotation_researcher (consult_id, researcher_id, prices_id, month, year)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (consult_id, researcher_id, prices_id, month, year))
        
        quotation_id = cur.fetchone()[0]
        conn.commit()
        return quotation_id
    except Exception as e:
        print(f"Erro ao salvar cotação: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_quotation_researchers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM quotation_researcher;")
    quotations = cur.fetchall()
    cur.close()
    conn.close()
    return quotations

def get_researcher_quotations(start_month, start_year, end_month, end_year, pesquisador_id):
    conn = get_connection()
    cur = conn.cursor()

    meses_dict = {
        "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
        "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
        "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
    }

    start_month_num = meses_dict[start_month]
    end_month_num = meses_dict[end_month]

    data_inicio = f"{start_year}-{start_month_num:02d}-01"
    ultimo_dia = calendar.monthrange(end_year, end_month_num)[1]  
    data_fim = f"{end_year}-{end_month_num:02d}-{ultimo_dia}"

    query = """
        SELECT u.nome AS pesquisador, 
               TO_CHAR(p.data_cotacao, 'Month') AS mes, 
               COUNT(p.id) AS total_cotacoes
        FROM users u
        JOIN stores s ON u.id = s.pesquisador_id
        JOIN prices p ON s.id = p.loja_id
        WHERE p.data_cotacao BETWEEN %s AND %s
    """

    params = [data_inicio, data_fim]

    if pesquisador_id:
        query += " AND u.id = %s"
        params.append(pesquisador_id)

    query += " GROUP BY u.nome, mes ORDER BY u.nome, mes"

    cur.execute(query, params)
    result = cur.fetchall()

    cur.close()
    conn.close()

    return result

def delete_quotation_researcher(quotation_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM quotation_researcher WHERE id = %s;", (quotation_id,))
    conn.commit()
    cur.close()
    conn.close()
