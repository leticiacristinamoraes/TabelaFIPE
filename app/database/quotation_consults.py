import streamlit as st

from app.database.config import get_connection

def create_quotation_consults_table():
    """Cria a tabela de consultas salvas se não existir."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quotation_consults (
            id SERIAL PRIMARY KEY,
            pesquisador_id INTEGER NOT NULL,
            start_month VARCHAR(20) NOT NULL,
            start_year INTEGER NOT NULL,
            end_month VARCHAR(20) NOT NULL,
            end_year INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pesquisador_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    
def save_quotation_consult(pesquisador_id, start_month, start_year, end_month, end_year):
    """Salva uma nova consulta e retorna o ID."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO quotation_consults (pesquisador_id, start_month, start_year, end_month, end_year) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (pesquisador_id, start_month, start_year, end_month, end_year))
        
        consult_id = cur.fetchone()[0]
        conn.commit()
        return consult_id
    except Exception as e:
        print(f"Erro ao salvar consulta: {e}")
        return None
    finally:
        cur.close()
        conn.close()
    
def get_quotation_consults(pesquisador_id=None, start_month=None, start_year=None, end_month=None, end_year=None):
    """Busca todas as consultas salvas, filtrando por pesquisador_id se necessário."""
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT * FROM quotation_consults"
    conditions = []
    params = []

    if pesquisador_id:
        conditions.append("pesquisador_id = %s")
        params.append(pesquisador_id)

    if start_month:
        conditions.append("start_month = %s")
        params.append(start_month)
    
    if start_year:
        conditions.append("start_year = %s")
        params.append(start_year)
    
    if end_month:
        conditions.append("end_month = %s")
        params.append(end_month)
    
    if end_year:
        conditions.append("end_year = %s")
        params.append(end_year)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cur.execute(query, tuple(params))
    
    colunas = [desc[0] for desc in cur.description]
    consults = [dict(zip(colunas, row)) for row in cur.fetchall()]

    cur.close()
    conn.close()
    
    return consults if consults else []

def delete_quotation_consult(consult_id):
    """Deleta uma consulta pelo ID."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM quotation_consults WHERE id = %s;", (consult_id,))
        conn.commit()
        print(f"Consulta ID {consult_id} removida com sucesso!")
    except Exception as e:
        print(f"Erro ao remover consulta: {e}")
    finally:
        cur.close()
        conn.close()
