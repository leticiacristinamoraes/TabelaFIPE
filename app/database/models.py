import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database.config import get_connection

def create_models_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS models (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            brand_id INTEGER NOT NULL,
            UNIQUE (brand_id, nome),
            FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def create_model(brand_id, nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO models (nome, brand_id) VALUES (%s, %s) ON CONFLICT (brand_id, nome) DO NOTHING RETURNING id;
    """, (nome, brand_id))
    result = cur.fetchone()  # Pode ser None se o modelo já existir
    model_id = result[0] if result else None
    conn.commit()
    cur.close()
    conn.close()
    return model_id

def get_models(brand_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM models WHERE brand_id = %s;", (brand_id,))
    models = cur.fetchall()
    conn.close()
    return models

def update_model(model_id, nome, brand_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE models SET nome = %s, brand_id = %s WHERE id = %s;
    """, (nome, brand_id, model_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_model(model_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM models WHERE id = %s;", (model_id,))
    conn.commit()
    cur.close()
    conn.close()