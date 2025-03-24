import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection1():
    return psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )

def update_ranking_researchers_table1():
    """
    Insere ou atualiza a tabela ranking_researchers com a quantidade total pesquisa.
    """
    conn = get_connection1()
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

def update():
    update_ranking_researchers_table1()
    print("Tabela de ranking dos pesquissadores atualizada!")

if __name__ == "__main__":
    update()