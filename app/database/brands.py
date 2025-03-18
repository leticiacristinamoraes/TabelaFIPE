import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database.config import get_connection

def create_brands_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) UNIQUE NOT NULL
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def create_brand(nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO brands (nome) VALUES (%s) RETURNING id;
    """, (nome,))
    brand_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return brand_id

def get_brands():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM brands;")
    brands = cur.fetchall()
    cur.close()
    conn.close()
    return brands

def update_brand(brand_id, nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE brands SET nome = %s WHERE id = %s;
    """, (nome, brand_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_brand(brand_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM brands WHERE id = %s;", (brand_id,))
    conn.commit()
    cur.close()
    conn.close()