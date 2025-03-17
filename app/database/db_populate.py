
from database.config import get_connection
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.config import get_connection

def record_exists(query, params=()):
    """Verifica se já existem registros na tabela."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists

def insert_brands():
    """Insere marcas de veículos."""
    if record_exists("SELECT 1 FROM brands LIMIT 1;"):
        print("✅ Marcas já inseridas.")
        return
    
    conn = get_connection()
    cur = conn.cursor()
    
    brands = ["Ford", "Chevrolet", "Toyota", "Honda", "Volkswagen"]
    query = "INSERT INTO brands (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING RETURNING id;"
    
    for brand in brands:
        cur.execute(query, (brand,))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Marcas inseridas com sucesso!")

def insert_models():
    """Insere modelos de veículos vinculados às marcas."""
    if record_exists("SELECT 1 FROM models LIMIT 1;"):
        print("✅ Modelos já inseridos.")
        return
    
    conn = get_connection()
    cur = conn.cursor()
    
    models = [
        (1, "Fiesta"), (1, "Focus"), (2, "Onix"), (2, "Prisma"),
        (3, "Corolla"), (3, "Hilux"), (4, "Civic"), (4, "Fit"),
        (5, "Golf"), (5, "Polo")
    ]
    
    query = """
        INSERT INTO models (brand_id, nome) 
        VALUES (%s, %s) 
        ON CONFLICT DO NOTHING;
    """
    
    for model in models:
        cur.execute(query, model)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Modelos inseridos com sucesso!")

def insert_vehicles():
    """Insere veículos fictícios na base de dados."""
    if record_exists("SELECT 1 FROM vehicles LIMIT 1;"):
        print("✅ Veículos já inseridos.")
        return
    
    conn = get_connection()
    cur = conn.cursor()
    
    vehicles = [
        (1, 2018, 2019), (2, 2020, 2021), (3, 2019, 2020),
        (4, 2021, 2022), (5, 2022, 2023), (6, 2017, 2018),
        (7, 2015, 2016), (8, 2019, 2020), (9, 2020, 2021),
        (10, 2018, 2019)
    ]
    
    query = """
        INSERT INTO vehicles (model_id, ano_fab, ano_modelo) 
        VALUES (%s, %s, %s) 
        ON CONFLICT DO NOTHING;
    """
    
    for vehicle in vehicles:
        cur.execute(query, vehicle)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Veículos inseridos com sucesso!")

def insert_stores():
    """Insere lojas fictícias na base de dados."""
    if record_exists("SELECT 1 FROM stores LIMIT 1;"):
        print("✅ Lojas já inseridas.")
        return
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Obtendo um ID de pesquisador válido
    cur.execute("SELECT id FROM users WHERE papel = 'pesquisador' LIMIT 1;")
    pesquisador = cur.fetchone()
    
    if not pesquisador:
        print("⚠ Nenhum pesquisador encontrado. Criando um padrão...")
        cur.execute(
            "INSERT INTO users (nome, email, papel) VALUES (%s, %s, %s) RETURNING id;",
            ('Pesquisador Padrão', 'pesquisador@email.com', 'pesquisador')
        )
        pesquisador_id = cur.fetchone()[0]
        conn.commit()
    else:
        pesquisador_id = pesquisador[0]

    stores = [
        ("AutoCar", "Rua 1", "00.000.000/0001-00", pesquisador_id),
        ("SuperCarros", "Rua 2", "11.111.111/0001-11", pesquisador_id)
    ]
    
    query = """
    INSERT INTO stores (nome, endereco, cnpj, pesquisador_id) 
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (cnpj) DO UPDATE SET 
        nome = EXCLUDED.nome,
        endereco = EXCLUDED.endereco,
        pesquisador_id = EXCLUDED.pesquisador_id;
"""

    
    for store in stores:
        print(f"Inserindo loja: {store}")
        cur.execute(query, store)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Lojas inseridas com sucesso!")

def insert_users():
    """Insere usuários fictícios."""
    conn = get_connection()
    cur = conn.cursor()
    
    users = [
        ("Alice", "alice@email.com", "pesquisador"),
        ("Bob", "bob@email.com", "pesquisador"),
        ("Carlos", "carlos@email.com", "gestor"),
        ("Diana", "diana@email.com", "gestor"),
        
    ]
    
    query = "INSERT INTO users (nome, email, papel) VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING RETURNING id;"
    for user in users:
        cur.execute(query, user)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Usuários inseridos com sucesso!")

def insert_prices():
    """Insere preços fictícios dos veículos nas lojas existentes no banco."""
    if record_exists("SELECT 1 FROM prices LIMIT 1;"):
        print("✅ Preços já inseridos.")
        return
    conn = get_connection()
    cur = conn.cursor()

    # Buscar IDs reais das lojas
    cur.execute("SELECT id FROM stores;")
    store_ids = [row[0] for row in cur.fetchall()]

    # Buscar IDs reais dos veículos
    cur.execute("SELECT id FROM vehicles;")
    vehicle_ids = [row[0] for row in cur.fetchall()]

    # Se não houver lojas ou veículos, não há o que inserir
    if not store_ids or not vehicle_ids:
        print("⚠ Nenhuma loja ou veículo encontrado. Nenhum preço inserido.")
        cur.close()
        conn.close()
        return

    # Criar preços associando IDs reais
    prices = []
    for i, vehicle_id in enumerate(vehicle_ids):
        store_id = store_ids[i % len(store_ids)]  # Distribui os preços entre as lojas
        price = 45000 + (i * 1000)  # Gera preços fictícios
        prices.append((store_id, vehicle_id, price))

    query = """
    INSERT INTO prices (loja_id, veiculo_id, preco) 
    VALUES (%s, %s, %s) 
    ON CONFLICT DO NOTHING;
    """

    for price in prices:
        cur.execute(query, price)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Preços inseridos com sucesso!")

def insert_average_prices():
    """Calcula e insere preços médios para cada veículo."""
    if record_exists("SELECT 1 FROM average_price LIMIT 1;"):
        print("✅ Preços médios já calculados.")
        return
    
    conn = get_connection()
    cur = conn.cursor()

    # Garante que veiculo_id seja UNIQUE na tabela average_price
    cur.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.table_constraints 
                WHERE table_name = 'average_price' 
                AND constraint_type = 'UNIQUE'
            ) THEN
                ALTER TABLE average_price ADD CONSTRAINT unique_veiculo UNIQUE (veiculo_id);
            END IF;
        END $$;
    """)
    conn.commit()

    # Insere ou atualiza os preços médios corretamente
    cur.execute("""
        INSERT INTO average_price (veiculo_id, average_price)
        SELECT veiculo_id, AVG(preco) AS avg_price
        FROM prices
        GROUP BY veiculo_id
        ON CONFLICT (veiculo_id) 
        DO UPDATE SET average_price = EXCLUDED.average_price;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Preços médios calculados e inseridos com sucesso!")

def populate_database():
    """Chama todas as funções para popular o banco de dados."""
    insert_brands()
    insert_models()
    insert_vehicles()
    insert_stores()
    insert_users()
    insert_prices()
    insert_average_prices()
    print("🎉 Banco de dados populado com sucesso!")

# Executar a função principal
if __name__ == "__main__":
    populate_database()
