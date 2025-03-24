import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import date
from app.database.config import get_connection
from app.database.stores import get_stores, get_stores_by_researcher
from app.database.brands import get_brands
from app.database.models import get_models
from app.database.vehicles import get_vehicle_years
from app.database.prices import create_price
from app.database.users import get_researcher_info
from app.database.ranking_researchers import create_ranking_researchers_table
from lib.auth import check_authentication, get_user_store_assignment

st.set_page_config(
    page_title="Pagina de Pesquisador",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Verificar se o usuário está autenticado
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.error("Você precisa estar logado para acessar esta página.")
    st.stop()  # Para a execução da página

st.title("🔍 Pesquisador")
st.write(f"Bem-vindo de volta, {st.session_state['user_info']['email']}. Insira os preços dos carros da loja pesquisada")

# Pega o ID do usuário logado
researcher_id = st.session_state["user_id"]
#st.title(researcher_id)

if st.button("Voltar para a Home"):
   st.switch_page("main.py")

# Função para obter o ID da loja pelo nome
def get_store_id_by_name(store_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM stores WHERE nome = %s;", (store_name,))
    store_id = cur.fetchone()
    cur.close()
    conn.close()
    return store_id[0] if store_id else None

# Função para obter o ID da marca pelo nome
def get_brand_id_by_name(brand_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM brands WHERE nome = %s;", (brand_name,))
    brand_id = cur.fetchone()
    cur.close()
    conn.close()
    return brand_id[0] if brand_id else None

# Layout do painel do pesquisador
st.title("Painel do Pesquisador")

# Seleção da loja
stores = get_stores_by_researcher(researcher_id)
#stores = get_stores()
store_names = [store[1] for store in stores]  # Assume que o nome da loja está na segunda posição da tupla
selected_store = st.selectbox("Selecione a loja", store_names)

# Seleção da marca
brands = get_brands()
brand_names = [brand[1] for brand in brands]  # Assume que o nome da marca está na segunda posição da tupla
selected_brand = st.selectbox("Selecione a marca", brand_names)

if selected_brand:
    brand_id = get_brand_id_by_name(selected_brand)
    models = get_models(brand_id)
    model_names = [model[1] for model in models]
    
    # Seleção do modelo
    selected_model = st.selectbox("Selecione o modelo", model_names)
    
    if selected_model:
        model_id = [m[0] for m in models if m[1] == selected_model][0]
        years = get_vehicle_years(model_id)
        
        # Seleção do ano do modelo
        selected_year = st.selectbox("Selecione o ano do modelo", years)

        # Campo para inserir o preço
        price = st.number_input("Informe o preço", min_value=0.0, format="%.2f")
        
        # Campo para inserir a data da pesquisa
        research_date = st.date_input("Selecione a data da pesquisa", datetime.today().date())

        if st.button("Salvar Preço"):
            store_id = get_store_id_by_name(selected_store)
            if store_id and model_id and selected_year:
                data_cotacao = research_date.strftime('%Y-%m-%d')  # Converte para string correta
                create_price(model_id, store_id, price, data_cotacao)

        selected_date = st.date_input("Selecione a data", value=date.today())

        if st.button("Salvar Preço"):
            store_id = get_store_id_by_name(selected_store)
            if store_id and model_id and selected_year and selected_date:
                create_price(model_id, store_id, price, selected_date)
               
                st.success("Preço cadastrado com sucesso!")
                
            else:
                st.error("Erro ao cadastrar o preço. Verifique os dados e tente novamente.")

