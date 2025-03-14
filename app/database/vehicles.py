from app.database.config import get_connection

def create_vehicles_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id SERIAL PRIMARY KEY,
            model_id INTEGER NOT NULL,
            ano_fab INTEGER NOT NULL,
            ano_modelo INTEGER NOT NULL,
            CONSTRAINT unique_vehicle UNIQUE (model_id, ano_fab, ano_modelo),
            FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()


def create_vehicle(model_id, ano_fab, ano_modelo):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO vehicles (model_id, ano_fab, ano_modelo) 
            VALUES (%s, %s, %s) RETURNING id;
        """, (model_id, ano_fab, ano_modelo))
        vehicle_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.IntegrityError:  # Captura erro de violação da UNIQUE constraint
        conn.rollback()  # Reverte a transação para evitar bloqueios
        cur.execute("""
            SELECT id FROM vehicles 
            WHERE model_id = %s AND ano_fab = %s AND ano_modelo = %s;
        """, (model_id, ano_fab, ano_modelo))
        vehicle_id = cur.fetchone()[0]  # Obtém o ID do veículo já existente
    finally:
        cur.close()
        conn.close()
    
    return vehicle_id

def get_vehicles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles;")
    vehicles = cur.fetchall()
    cur.close()
    conn.close()
    return vehicles

def update_vehicle(vehicle_id, model_id, ano_fab, ano_modelo):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE vehicles SET model_id = %s, ano_fab = %s, ano_modelo = %s WHERE id = %s;
    """, (model_id, ano_fab, ano_modelo, vehicle_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_vehicle(vehicle_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicles WHERE id = %s;", (vehicle_id,))
    conn.commit()
    cur.close()
    conn.close()
    
from database.config import get_connection

def get_vehicle_years(model_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT ano_fab, ano_modelo FROM vehicles WHERE model_id = %s;", (model_id,))
    anos = sorted({ano for row in cur.fetchall() for ano in row})
    conn.close()
    return anos
   