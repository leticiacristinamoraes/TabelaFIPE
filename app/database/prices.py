import sys
import os
sys.path.append(os.path.abspath("app"))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.config import get_connection
import os
import psycopg2
from datetime import datetime


# Adicione o caminho correto do seu projeto
sys.path.append(os.path.abspath("app"))

from app.database.config import get_connection
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

    # 1. Buscar todos os preços do veículo na tabela 'prices'
    cur.execute("""
        SELECT price FROM prices WHERE veiculo_id = %s
    """, (veiculo_id,))
    
    precos = cur.fetchall()  # Retorna uma lista de tuplas [(preco1,), (preco2,), ...]
    
    if not precos:  # Se não houver preços cadastrados
        print(f"Nenhum preço encontrado para o veículo {veiculo_id}")
        return
    
    # 2. Calcular a média dos preços
    media_preco = round(sum(p[0] for p in precos) / len(precos), 2)

    # 3. Atualizar ou inserir a média na tabela 'average_price'
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

#P13-Feature: Função para pegar a quantidade de cotações para uma determinada loja em um periodo de mês/ano
def get_cotations_count_by_time(store_id, date_start, date_final):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT COUNT("preco"), EXTRACT(YEAR FROM "data") "year",EXTRACT("month" FROM "data") "month" FROM "prices" WHERE loja_id=%s AND "data" BETWEEN %s AND %s GROUP BY "year", "month" ORDER BY "year","month" ASC;''', (store_id, date_start,date_final))
    cotations = cur.fetchall()
    print(cotations)
    cur.close()
    conn.close()
    return {f"{p[1]}/{p[2]}": p[0] for p in cotations}
def count_inputs_researcher(researcher_id, start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT data,
		COUNT(*) AS cotacoes
FROM (SELECT * FROM (SELECT
	prices.loja_id,
	prices.data,
	stores.pesquisador_id
FROM prices
	INNER JOIN stores ON prices.loja_id = stores.id) T 
		WHERE loja_id IN (SELECT id FROM stores WHERE pesquisador_id = {} ) 
		AND data BETWEEN '{}' AND '{}') R
GROUP BY data;

    """.format(researcher_id, start_date, end_date))
    stores_per_researcher = cur.fetchall()
    cur.close()
    conn.close()
    return stores_per_researcher

def count_total(researcher_id, start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
	        SUM(cotacoes)
	        FROM
                (SELECT data,
		            COUNT(*) AS cotacoes
                FROM (SELECT * FROM (SELECT
	                prices.loja_id,
	                prices.data,
	                stores.pesquisador_id
                FROM prices
	            INNER JOIN stores ON prices.loja_id = stores.id) T 
		        WHERE loja_id IN (SELECT id FROM stores WHERE pesquisador_id = {} ) 
		            AND data BETWEEN '{}' AND '{}') R
                GROUP BY data) S;

    """.format(researcher_id, start_date, end_date))
    total_stores_researcher = cur.fetchall()
    cur.close()
    conn.close()
    return total_stores_researcher
