from app.database.config import get_connection
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def create_average_price_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS average_price (
            id SERIAL PRIMARY KEY,
            veiculo_id INTEGER NOT NULL,
            average_price NUMERIC(10,2) NOT NULL,
            FOREIGN KEY (veiculo_id) REFERENCES vehicles(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def create_average_price(veiculo_id, avg_price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO average_price (veiculo_id, average_price) VALUES (%s, %s) RETURNING id;
    """, (veiculo_id, avg_price))
    avg_price_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return avg_price_id

def get_average_prices():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM average_price;")
    avg_prices = cur.fetchall()
    cur.close()
    conn.close()
    return avg_prices

def update_average_price(avg_price_id, vehicle_id, avg_price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE average_price SET veiculo_id = %s, average_price = %s WHERE id = %s;
    """, (vehicle_id, avg_price, avg_price_id))
    conn.commit()
    cur.close()
    conn.close()
     
def calculate_and_update_average_price(veiculo_id):
    conn = get_connection()
    cur = conn.cursor()

    # Busca todos os preços do veículo na tabela prices
    cur.execute("SELECT preco FROM prices WHERE veiculo_id = %s;", (veiculo_id,))
    precos = cur.fetchall()

    if not precos:  # Se não houver preços, encerra a função
        print(f"[ERRO] Nenhum preço encontrado para veiculo_id {veiculo_id}")
        cur.close()
        conn.close()
        return None

    # Calcula a média dos preços
    precos_lista = [p[0] for p in precos]
    media_preco = sum(precos_lista) / len(precos_lista)
    print(f"[DEBUG] Média calculada: {media_preco}")

    print(f"[INFO] Média calculada para veiculo_id {veiculo_id}: {media_preco}")  # Debug

    # Atualiza ou insere o valor na tabela average_price
    cur.execute("""
    INSERT INTO average_price (veiculo_id, average_price)
    VALUES (%s, %s)
    ON CONFLICT (veiculo_id) DO UPDATE 
    SET average_price = EXCLUDED.average_price;
""", (veiculo_id, media_preco))

    conn.commit()
    cur.close()
    conn.close()

    print(f"[INFO] Preço médio atualizado no banco para veiculo_id {veiculo_id}")

        
def delete_average_price(avg_price_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM average_price WHERE id = %s;", (avg_price_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    calculate_and_update_average_price(7)