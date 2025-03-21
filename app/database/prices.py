from app.database.config import get_connection
import sys
import os
import psycopg2
from datetime import datetime

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
            data_cotacao DATE NOT NULL,  
            FOREIGN KEY (veiculo_id) REFERENCES vehicles(id) ON DELETE CASCADE,
            FOREIGN KEY (loja_id) REFERENCES stores(id) ON DELETE CASCADE
        );
    """)
    
    cur.execute("CREATE INDEX IF NOT EXISTS idx_prices_id ON prices(id);")
    
    conn.commit()
    cur.close()
    conn.close()

def create_price(veiculo_id, loja_id, preco, data_cotacao):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Garantir que data_cotacao esteja no formato correto (YYYY-MM-DD)
        if isinstance(data_cotacao, str):
            try:
                data_cotacao = datetime.strptime(data_cotacao, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato de data inválido. Use 'YYYY-MM-DD'.")
        elif isinstance(data_cotacao, datetime):
            data_cotacao = data_cotacao.date()  # Converte datetime para apenas a data
        else:
            raise TypeError(f"data_cotacao deve ser uma string 'YYYY-MM-DD' ou datetime, mas recebeu {type(data_cotacao)}")

        print(f"DATA QUE SERÁ INSERIDA NO BANCO: {data_cotacao} (Tipo: {type(data_cotacao)})")

        cur.execute("""
            INSERT INTO prices (veiculo_id, loja_id, preco, data_cotacao) 
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (veiculo_id, loja_id, preco, data_cotacao))
        
        price_id = cur.fetchone()[0]
        conn.commit()

    except Exception as e:
        print(f"Erro ao inserir preço: {e}")
        conn.rollback()
        return None

    finally:
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

def update_price(price_id, veiculo_id, loja_id, preco, data_cotacao):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE prices SET veiculo_id = %s, loja_id = %s, preco = %s, data_cotacao = %s 
        WHERE id = %s;
    """, (veiculo_id, loja_id, preco, data_cotacao, price_id))
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
