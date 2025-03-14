from app.database.config import get_connection

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
    # conn = get_connection()
    # cur = conn.cursor()
    # cur.execute("""
    #     UPDATE average_price SET veiculo_id = %s, average_price = %s WHERE id = %s;
    # """, (vehicle_id, avg_price, avg_price_id))
    # conn.commit()
    # cur.close()
    # conn.close()
    repo = AvgPricePostgresqlRepository()
    repo.calculate_and_store_avg_prices()
    print("Preços médios atualizados.")



def delete_average_price(avg_price_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM average_price WHERE id = %s;", (avg_price_id,))
    conn.commit()
    cur.close()
    conn.close()