
from database.config import get_connection
import sys
import os
from datetime import datetime
import random
from datetime import datetime, timedelta

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
    
    brands = ["Ford", "Chevrolet", "Toyota", "Honda", "Volkswagen", "Hyundai", "Nissan", "Fiat", "Renault", "Jeep"]
    brands = ["Ford", "Chevrolet", "Toyota", "Honda", "Volkswagen",
        "Nissan", "Hyundai", "Renault", "Fiat", "Jeep",
        "Peugeot", "Citroën", "Mitsubishi", "Subaru", "Mazda",
        "Suzuki", "Mercedes-Benz", "BMW", "Audi", "Volvo"]
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
        (1, "Fiesta"), (1, "Focus"), (1, "Ka"), (1, "EcoSport"), (1, "Ranger"),
        (2, "Onix"), (2, "Prisma"), (2, "S10"), (2, "Spin"), (2, "Cruze"),
        (3, "Corolla"), (3, "Hilux"), (3, "Yaris"), (3, "SW4"), (3, "RAV4"),
        (4, "Civic"), (4, "Fit"), (4, "HR-V"), (4, "City"), (4, "Accord"),
        (5, "Golf"), (5, "Polo"), (5, "Jetta"), (5, "T-Cross"), (5, "Tiguan"),
        (6, "HB20"), (6, "Creta"), (6, "Tucson"), (6, "Santa Fe"), (6, "Kona"),
        (7, "March"), (7, "Versa"), (7, "Sentra"), (7, "Frontier"), (7, "Kicks"),
        (8, "Uno"), (8, "Mobi"), (8, "Argo"), (8, "Toro"), (8, "Cronos"),
        (9, "Kwid"), (9, "Sandero"), (9, "Logan"), (9, "Duster"), (9, "Captur"),
        (10, "Renegade"), (10, "Compass"), (10, "Commander"), (10, "Cherokee"), (10, "Wrangler")
        (1, "Fiesta"), (1, "Focus"), (1, "Ka"),
        (2, "Onix"), (2, "Prisma"), (2, "Tracker"),
        (3, "Corolla"), (3, "Hilux"), (3, "Yaris"),
        (4, "Civic"), (4, "Fit"), (4, "HR-V"),
        (5, "Golf"), (5, "Polo"), (5, "T-Cross"),
        (6, "March"), (6, "Versa"), (6, "Kicks"),
        (7, "HB20"), (7, "Creta"), (7, "Tucson"),
        (8, "Kwid"), (8, "Sandero"), (8, "Duster"),
        (9, "Uno"), (9, "Palio"), (9, "Argo"),
        (10, "Renegade"), (10, "Compass"), (10, "Commander"),
        (11, "208"), (11, "2008"), (11, "3008"),
        (12, "C3"), (12, "C4 Cactus"), (12, "Aircross"),
        (13, "Lancer"), (13, "Outlander"), (13, "ASX"),
        (14, "Impreza"), (14, "Forester"), (14, "WRX"),
        (15, "Mazda3"), (15, "CX-5"), (15, "MX-5 Miata"),
        (16, "Swift"), (16, "Vitara"), (16, "Jimny"),
        (17, "Classe A"), (17, "Classe C"), (17, "GLC"),
        (18, "Série 3"), (18, "X1"), (18, "X5"),
        (19, "A3"), (19, "Q3"), (19, "Q5"),
        (20, "XC40"), (20, "XC60"), (20, "S90")
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
    
    vehicles = []
    for model_id in range(1, 51):  # Adicionando mais modelos
        for ano_fab in range(2015, 2024):
            vehicles.append((model_id, ano_fab, ano_fab + 1))
    vehicles = [
        (1, 2018, 2019), (2, 2020, 2021), (3, 2019, 2020),
        (4, 2021, 2022), (5, 2022, 2023), (6, 2017, 2018),
        (7, 2015, 2016), (8, 2019, 2020), (9, 2020, 2021),
        (10, 2018, 2019), (11, 2021, 2022), (12, 2023, 2024),
        (13, 2016, 2017), (14, 2020, 2021), (15, 2022, 2023),
        (16, 2019, 2020), (17, 2021, 2022), (18, 2023, 2024),
        (16, 2019, 2020), (17, 2021, 2022), (18, 2023, 2024)
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
    """Insere lojas fictícias na base de dados para cada pesquisador."""
    if record_exists("SELECT 1 FROM stores LIMIT 1;"):
        print("✅ Lojas já inseridas.")
        return
    
    conn = get_connection()
    cur = conn.cursor()

    # Obtendo os IDs de todos os pesquisadores
    cur.execute("SELECT id FROM users WHERE papel = 'pesquisador';")
    pesquisadores = cur.fetchall()
    
    cur.execute("SELECT id FROM users WHERE papel = 'pesquisador' LIMIT 1;")
    pesquisador = cur.fetchone()
    
    if not pesquisador:

    if not pesquisadores:

        print("⚠ Nenhum pesquisador encontrado. Criando um padrão...")
        cur.execute(
            "INSERT INTO users (nome, email, papel) VALUES (%s, %s, %s) RETURNING id;",
            ('Pesquisador Padrão', 'pesquisador@email.com', 'pesquisador')
        )
        pesquisador_id = cur.fetchone()[0]
        conn.commit()
        pesquisadores = [(pesquisador_id,)]

    # Lojas fictícias a serem atribuídas aos pesquisadores
    stores = [
        ("AutoCar", "Avenida Brasil, 123", "00.000.000/0001-00", pesquisador_id),
        ("SuperCarros", "Rua das Flores, 456", "11.111.111/0001-11", pesquisador_id),
        ("Top Veículos", "Alameda Santos, 789", "22.222.222/0001-22", pesquisador_id),
        ("Prime Motors", "Estrada do Sol, 321", "33.333.333/0001-33", pesquisador_id),
        ("Elite Cars", "Rodovia Central, 654", "44.444.444/0001-44", pesquisador_id),
        ("Lux Auto", "Avenida Paulista, 987", "55.555.555/0001-55", pesquisador_id),
        ("Speed Veículos", "Rua XV de Novembro, 258", "66.666.666/0001-66", pesquisador_id),
        ("Auto Fácil", "Praça das Nações, 753", "77.777.777/0001-77", pesquisador_id),
        ("Master Motors", "Boulevard Shopping, 159", "88.888.888/0001-88", pesquisador_id),
        ("City Cars", "Avenida Independência, 357", "99.999.999/0001-99", pesquisador_id)
        ("AutoCar", "Rua 1", "00.000.000/0001-00"),
        ("SuperCarros", "Rua 2", "11.111.111/0001-11"),
        ("CarCenter", "Rua 3", "22.222.222/0001-22"),
        ("MegaCarros", "Rua 4", "33.333.333/0001-33"),
        ("CarShop", "Rua 5", "44.444.444/0001-44"),
        ("SpeedCars", "Rua 6", "55.555.555/0001-55"),
        ("FastAuto", "Rua 7", "66.666.666/0001-66"),
        ("CarWorld", "Rua 8", "77.777.777/0001-77"),
        ("AutoZone", "Rua 9", "88.888.888/0001-88"),
        ("CarHouse", "Rua 10", "99.999.999/0001-99"),
        ("FastLane", "Rua 11", "10.101.010/0001-10"),
        ("QuickCar", "Rua 12", "11.121.212/0001-11"),
        ("TopCars", "Rua 13", "12.131.313/0001-12"),
        ("PrimeCar", "Rua 14", "13.141.414/0001-13"),
        ("LuxuryCars", "Rua 15", "14.151.515/0001-14"),
        ("PowerCars", "Rua 16", "15.161.616/0001-15"),
        ("UltraCars", "Rua 17", "16.171.717/0001-16"),
        ("CityCars", "Rua 18", "17.181.818/0001-17"),
        ("DreamCars", "Rua 19", "18.191.919/0001-18"),
        ("SpeedAuto", "Rua 20", "19.202.020/0001-19")
    ]
    
    query = """
    INSERT INTO stores (nome, endereco, cnpj, pesquisador_id) 
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (cnpj) DO UPDATE SET 
        nome = EXCLUDED.nome,
        endereco = EXCLUDED.endereco,
        pesquisador_id = EXCLUDED.pesquisador_id;
    """
    
    # Garantindo que cada pesquisador tenha uma loja
    for i, pesquisador_id in enumerate(pesquisadores):
        store = stores[i % len(stores)]  # Atribui uma loja para cada pesquisador
        print(f"Inserindo loja: {store[0]} para pesquisador ID: {pesquisador_id[0]}")
        cur.execute(query, (store[0], store[1], store[2], pesquisador_id[0]))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Lojas inseridas com sucesso!")


def insert_users():
    """Insere usuários fictícios."""
    conn = get_connection()
    cur = conn.cursor()
    
    users = [
        ("Cristina", "lleehmoraes@gmail.com", "pesquisador"),
        ("Letícia", "leticiacristinafmds@gmail.com", "gestor"),
        ("Juca", "usuariodetestetestando@gmail.com", "pesquisador"),
        ("França", "leehcristinna@gmail.com", "gestor"),
        ("Hilario", "hilarioglobo2025@gmail.com", "pesquisador")
        ("Alice", "alice@email.com", "pesquisador"),
        ("Bob", "bob@email.com", "pesquisador"),
        ("Carlos", "carlos@email.com", "gestor"),
        ("Diana", "diana@email.com", "gestor"),
        ("Eve", "eve@email.com", "pesquisador"),
        ("Frank", "frank@email.com", "pesquisador"),
        ("Grace", "grace@email.com", "pesquisador"),
        ("Hannah", "hannah@email.com", "pesquisador"),
        ("Ivy", "ivy@email.com", "pesquisador"),
        ("Jack", "jack@email.com", "pesquisador"),
        ("Kim", "kim@email.com", "pesquisador"),
        ("Liam", "liam@email.com", "pesquisador"),
        ("Mia", "mia@email.com", "pesquisador"),
        ("Nathan", "nathan@email.com", "pesquisador"),
        ("Olivia", "olivia@email.com", "pesquisador"),
        ("Paul", "paul@email.com", "pesquisador"),
        ("Quinn", "quinn@email.com", "pesquisador"),
        ("Riley", "riley@email.com", "pesquisador"),
        ("Sophia", "sophia@email.com", "pesquisador"),
        ("Tom", "tom@email.com", "pesquisador"),
        ("Uma", "uma@email.com", "pesquisador")   
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

    cur.execute("SELECT id FROM stores;")
    store_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id FROM vehicles;")
    vehicle_ids = [row[0] for row in cur.fetchall()]

    if not store_ids or not vehicle_ids:
        print("⚠ Nenhuma loja ou veículo encontrado. Nenhum preço inserido.")
        cur.close()
        conn.close()
        return

    prices = []
    for i, vehicle_id in enumerate(vehicle_ids):
        store_id = store_ids[i % len(store_ids)]
        price = 45000 + (i * 500)  
        data_cotacao = datetime.now().date()  
        prices.append((store_id, vehicle_id, price, data_cotacao))

    query = """
    INSERT INTO prices (loja_id, veiculo_id, preco, data_cotacao) 
    # Criar preços associando IDs reais
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 1, 1)
    prices = []

    # Gerando 500 preços
    for _ in range(500):
        store_id = random.choice(store_ids)  # Escolhe aleatoriamente uma loja
        vehicle_id = random.choice(vehicle_ids)  # Escolhe aleatoriamente um veículo
        price = random.randint(20000, 100000)  # Gera preços aleatórios entre 20.000 e 100.000
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))  # Gera data aleatória
        prices.append((store_id, vehicle_id, price, date))

    query = """
    INSERT INTO prices (loja_id, veiculo_id, preco, data) 
    VALUES (%s, %s, %s, %s) 
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
    insert_users()
    insert_stores()
    insert_prices()
    insert_average_prices()
    print("🎉 Banco de dados populado com sucesso!")

# Executar a função principal
if __name__ == "__main__":
    populate_database()
