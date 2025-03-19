import datetime
import sys
import os

# Adicione o caminho correto do seu projeto
sys.path.append(os.path.abspath("app"))

from database.config import get_connection


def create_prices_store_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS month_price_stores (
            id SERIAL PRIMARY KEY,
            loja_id INTEGER NOT NULL,
            cotacao_total NUMERIC(10,2) NOT NULL,
            data DATE NOT NULL, -- Adicionando a coluna de data
            FOREIGN KEY (loja_id) REFERENCES stores(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def create_price_store(loja_id, new_cotacao_total, data):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO "month_price_stores" (loja_id, cotacao_total, data) 
        VALUES ( %s, %s, %s);
    ''', (loja_id, new_cotacao_total, data))
    
    conn.commit()
    cur.close()
    conn.close()
    
    
    
    return "ok"

def get_total_prices_store():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM month_price_store;")
    avg_prices = cur.fetchall()
    cur.close()
    conn.close()
    return avg_prices

def get_cotation_by_data(store_id, date_start, date_final):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT cotacao_total, data  FROM "month_price_stores" WHERE loja_id=%s AND "data" BETWEEN %s AND %s GROUP BY "cotacao_total","data";''', (store_id, date_start,date_final))
    cotations = cur.fetchall()
    print(cotations)
    cur.close()
    conn.close()
    return {p[1]: p[0] for p in cotations}

def update_price_store(price_id, veiculo_id, loja_id, preco, data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE prices SET veiculo_id = %s, loja_id = %s, preco = %s, data = %s 
        WHERE id = %s;
    """, (veiculo_id, loja_id, preco, data, price_id))
    conn.commit()
    cur.close()
    conn.close()

def calculate_month_price_store(prices, value_multiplier):
    new_month_price = prices * value_multiplier
    return new_month_price

def update_month_price_store(store_id, new_cotacao_total, data):
    pass

def delete_price(price_id, veiculo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM prices WHERE id = %s;", (price_id,))
    conn.commit()
    cur.close()
    conn.close()
    
def drop_price_store():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS month_price_stores;''')
    conn.commit()
    cur.close()
    conn.close()
    return "ok"

def get_cotations_count_by_month(store_id: int, date_start: datetime, date_final:datetime):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT COUNT("preco") AS total_precos, EXTRACT(YEAR FROM "data") "year", EXTRACT(MONTH FROM "data") "month"  FROM "prices" WHERE loja_id=%s AND "data" BETWEEN %s AND %s GROUP BY "year","month";''', (store_id, date_start,date_final))
    cotations = cur.fetchone()
    print(cotations)
    cur.close()
    conn.close()
    return {'total': cotations[0], 'year': int(cotations[1]), 'month': int(cotations[2])}