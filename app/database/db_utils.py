import psycopg2
import pandas as pd

def executar_query(query):
    """Executa uma query SQL e retorna um DataFrame."""
    conn = psycopg2.connect("dbname=meubanco user=meuuser password=minhasenha host=localhost port=5432")
    cur = conn.cursor()
    
    cur.execute(query)
    colunas = [desc[0] for desc in cur.description]
    dados = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return pd.DataFrame(dados, columns=colunas)
