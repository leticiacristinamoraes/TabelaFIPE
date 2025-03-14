from database.config import get_connection

def create_prices_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            veiculo_id INTEGER NOT NULL,
            loja_id INTEGER NOT NULL,
            preco NUMERIC(10,2) NOT NULL,
            FOREIGN KEY (veiculo_id) REFERENCES vehicles(id) ON DELETE CASCADE,
            FOREIGN KEY (loja_id) REFERENCES stores(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def create_price(veiculo_id, loja_id, preco):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO prices (veiculo_id, loja_id, preco) VALUES (%s, %s, %s) RETURNING id;
    """, (veiculo_id, loja_id, preco))
    price_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return price_id

def get_prices():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prices;")
    prices = cur.fetchall()
    cur.close()
    conn.close()
    return prices

def update_price(price_id, veiculo_id, loja_id, preco):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE prices SET veiculo_id = %s, loja_id = %s, preco = %s WHERE id = %s;
    """, (veiculo_id, loja_id, preco, price_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_price(price_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM prices WHERE id = %s;", (price_id,))
    conn.commit()
    cur.close()
    conn.close()