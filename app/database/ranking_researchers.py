from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.database.config import get_connection


def create_ranking_researchers_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ranking_researchers (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(100) NOT NULL,
            total_pesquisa INTEGER NOT NULL
        );                
    """)
    conn.commit()
    cur.close()
    conn.close()
    
def get_ranking_researchers_table():
    """
    Insere ou atualiza a tabela ranking_researchers com a quantidade total pesquisa.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO ranking_researchers (user_id, user_name, total_pesquisa)
            SELECT 
                u.id AS user_id,
                u.nome AS user_name,
                COUNT(p.id) AS total_pesquisa
            FROM users u
            LEFT JOIN stores s ON u.id = s.pesquisador_id
            LEFT JOIN prices p ON s.id = p.loja_id
            WHERE u.papel = 'pesquisador'
            GROUP BY u.id, u.nome
            ORDER BY total_pesquisa DESC
            ON CONFLICT (user_id) DO UPDATE
                SET user_name = EXCLUDED.user_name,
                total_pesquisa = EXCLUDED.total_pesquisa;
        """)
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir pesquisador no ranking: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def generate_research_graph(start_date, end_date):
    """Busca o total de pesquisas por usuário no intervalo de datas informado."""
    query = """
        SELECT 
            u.id AS user_id,
            u.nome AS user_name,
            COUNT(p.id) AS total_pesquisas
        FROM users u
        LEFT JOIN stores s ON u.id = s.pesquisador_id
        LEFT JOIN prices p ON s.id = p.loja_id
        WHERE p.data BETWEEN %s AND %s
        GROUP BY u.id, u.nome
        ORDER BY total_pesquisas DESC
        LIMIT 10;
    """
    
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))
    conn.close()
    
    return df
    
    
