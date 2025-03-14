import streamlit as st
import os
from dotenv import load_dotenv
import sys
import pandas as pd
from database.create_tables import create_all_tables
from database.config import get_connection
from database.brands import get_brands
from database.models import get_models
from database.db_populate import populate_database
from database.vehicles import get_vehicle_years

#from database.average_price import get_vehicle_price, get_average_price

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.lib.auth import Authenticator

load_dotenv()
create_all_tables()

def database_ja_populado():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM brands;")
    count = cur.fetchone()[0]
    conn.close()
    return count > 0 

if not database_ja_populado():
   populate_database()

st.set_page_config(
    page_title="Tabela Fipe",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Tabela de preços de veículos")

# Inicializa autenticação
allowed_users = os.getenv("ALLOWED_USERS").split(",")
authenticator = Authenticator(
    allowed_users=allowed_users,
    token_key=os.getenv("TOKEN_KEY"),
    secret_path="client_secret.json",
    redirect_uri="http://localhost:8501",
)

# Estados de sessão para armazenar os filtros selecionados
if "selected_brand" not in st.session_state:
    st.session_state["selected_brand"] = None
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = None
if "selected_year" not in st.session_state:
    st.session_state["selected_year"] = None

def buscar_precos(marca=None, modelo=None, ano_fab=None, ano_modelo=None):
    """Busca preços médios dos veículos com base nos filtros informados."""
    conn = get_connection()
    query = """
    SELECT b.nome AS marca, m.nome AS modelo, v.ano_fab, v.ano_modelo, ap.average_price
    FROM vehicles v
    JOIN models m ON v.model_id = m.id
    JOIN brands b ON m.brand_id = b.id
    JOIN average_price ap ON v.id = ap.veiculo_id
    WHERE 1=1
    """
    params = []
    
    if marca:
        query += " AND b.nome = %s"
        params.append(marca)
    if modelo:
        query += " AND m.nome = %s"
        params.append(modelo)
    if ano_fab:
        query += " AND v.ano_fab = %s"
        params.append(ano_fab)
    if ano_modelo:
        query += " AND v.ano_modelo = %s"
        params.append(ano_modelo)
    
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
# Interface no Streamlit
st.title("Consulta Pública de Preços de Veículos")

# Obtém a lista de marcas do banco de dados
marcas = get_brands()  # Retorna [(id, "Marca1"), (id, "Marca2"), ...]
marcas_dict = {nome: id for id, nome in marcas} if marcas else {}

# Dropdown de marcas
marca_selecionada = st.selectbox("Marca", ["Selecione"] + list(marcas_dict.keys()))

# Se a marca foi selecionada, busca os modelos
if marca_selecionada != "Selecione":
    brand_id = marcas_dict[marca_selecionada]
    modelos = get_models(brand_id)  # Agora passamos o ID correto
    modelos_dict = {nome: id for id, nome in modelos} if modelos else {}

    # Dropdown de modelos
    modelo_selecionado = st.selectbox("Modelo", ["Selecione"] + list(modelos_dict.keys()))

    # Se um modelo foi selecionado, busca os anos disponíveis
    if modelo_selecionado != "Selecione":
        model_id = modelos_dict[modelo_selecionado]
        anos = get_vehicle_years(model_id)  # Agora passamos o ID correto

        # Dropdown de ano
        ano_selecionado = st.selectbox("Ano do veículo", ["Selecione"] + anos)

        # Se um ano foi selecionado, buscar os preços
        if ano_selecionado != "Selecione":
            if st.button("Buscar preços"):
                df = buscar_precos(marca_selecionada, modelo_selecionado, ano_selecionado)
                if df.empty:
                    st.warning("Nenhum resultado encontrado.")
                else:
                    st.dataframe(df)


