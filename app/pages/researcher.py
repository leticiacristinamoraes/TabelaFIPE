import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from datetime import datetime

# from database.config import get_connection
# from database.stores import get_stores
# from database.brands import get_brands
# from database.models import get_models
# from database.vehicles import get_vehicle_years
from lib.data import get_models, get_vehicle_years,get_shops, get_cars, get_shop_id, get_brand_id_by_name, set_car_register
from lib.auth import check_authentication, get_user_store_assignment


st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Pesquisador")
st.write("Bem vindo de volta Pesquisador. Insira os preços dos carros da loja pesquisada")
'''
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

# Seleção da loja leticia
store_names = [store[1] for store in stores]  # Assume que o nome da loja está na segunda posição da tupla
'''


'''
# Seleção da marca leticia
brands = get_cars()
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
'''

shops = get_shops()
store_names = [store.name for store in shops]  # Assume que o nome da loja está na segunda posição da tupla
selected_store = st.selectbox("Selecione a loja", store_names)

cars = get_cars()
brand_options = [brand.name for brand in cars]
selected_brand_name = st.selectbox("Marca", options=brand_options)

    
if selected_brand_name:
    brand_id = get_brand_id_by_name(selected_brand_name)
    models = get_models(brand_id)
    models_names = [model.name for model in models]

    selected_model_name = st.selectbox("Modelo", options=models_names)


    
    if selected_model_name:
        model_id = [model.id for model in models if model.name == selected_model_name]
        year_options = get_vehicle_years(model_id=model_id)
        selected_year = st.selectbox("Ano", options=year_options)

    # Campo para inserir o preço
        price = st.number_input("Informe o preço", min_value=0.0, format="%.2f")

        # Botão para salvar o preço
        if st.button("Salvar Preço"):
            store_id = get_shop_id(selected_store)
            if store_id and model_id and selected_year:
                set_car_register(model_id, store_id, price)
                st.success("Preço cadastrado com sucesso!")
            else:
                st.error("Erro ao cadastrar o preço. Verifique os dados e tente novamente.")
