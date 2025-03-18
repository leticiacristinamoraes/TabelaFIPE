import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database.config import get_connection
import os
import psycopg2

sys.path.append(os.path.abspath("app"))
from app.database.average_price import calculate_and_update_average_price

def create_prices_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            veiculo_id INTEGER NOT NULL,
            loja_id INTEGER NOT NULL,
            preco NUMERIC(10,2) NOT NULL,
            data DATE NOT NULL,  -- Adicionando a coluna de data
            FOREIGN KEY (veiculo_id) REFERENCES vehicles(id) ON DELETE CASCADE,
            FOREIGN KEY (loja_id) REFERENCES stores(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def create_price(veiculo_id, loja_id, preco, data):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO prices (veiculo_id, loja_id, preco, data) 
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (veiculo_id, loja_id, preco, data))
    
    price_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    calculate_and_update_average_price(veiculo_id)
    
    return price_id

def get_prices():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prices;")
    prices = cur.fetchall()
    cur.close()
    conn.close()
    return prices

def update_price(price_id, veiculo_id, loja_id, preco, data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE prices SET veiculo_id = %s, loja_id = %s, preco = %s, data = %s 
        WHERE id = %s;
    """, (veiculo_id, loja_id, preco, data, price_id))
    conn.commit()
    cur.close()
    conn.close()
    
    calculate_and_update_average_price(veiculo_id)

def calcular_e_atualizar_media(veiculo_id):
    """Calcula a média dos preços de um veículo e armazena na tabela average_price."""

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT preco FROM prices WHERE veiculo_id = %s
    """, (veiculo_id,))
    
    precos = cur.fetchall()  
    
    if not precos:  
        print(f"Nenhum preço encontrado para o veículo {veiculo_id}")
        return
    
    media_preco = round(sum(p[0] for p in precos) / len(precos), 2)

    cur.execute("""
        INSERT INTO average_price (veiculo_id, average_price)
        VALUES (%s, %s)
        ON CONFLICT (veiculo_id) DO UPDATE 
        SET average_price = EXCLUDED.average_price;
    """, (veiculo_id, media_preco))

    conn.commit()
    cur.close()
    conn.close()
    
    print(f"Preço médio atualizado para veículo {veiculo_id}: R$ {media_preco}")

def delete_price(price_id, veiculo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM prices WHERE id = %s;", (price_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    calculate_and_update_average_price(veiculo_id)
