import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.config import get_connection

def create_stores_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            endereco TEXT NOT NULL,
            cnpj VARCHAR(18) UNIQUE NOT NULL,
            pesquisador_id INTEGER NOT NULL,
            FOREIGN KEY (pesquisador_id) REFERENCES users(id) ON DELETE SET NULL
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def create_store(nome, endereco, cnpj, pesquisador_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO stores (nome, endereco, cnpj, pesquisador_id) VALUES (%s, %s, %s, %s) RETURNING id;
    """, (nome, endereco, cnpj, pesquisador_id))
    store_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return store_id

def get_stores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, endereco, cnpj, COALESCE(pesquisador_id, 0) FROM stores;")
    stores = cur.fetchall()
    cur.close()
    conn.close()
    return stores if stores else []

def update_store(store_id, nome, endereco, cnpj, pesquisador_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE stores SET nome = %s, endereco = %s, cnpj = %s, pesquisador_id = %s WHERE id = %s;
    """, (nome, endereco, cnpj, pesquisador_id, store_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_store(store_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM stores WHERE id = %s;", (store_id,))
    conn.commit()
    cur.close()
    conn.close()