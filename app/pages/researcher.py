import sys
import os

import streamlit as st
import pandas as pd
from datetime import datetime

# from database.config import get_connection
# from database.stores import get_stores
# from database.brands import get_brands
# from database.models import get_models
# from database.vehicles import get_vehicle_years
from lib.data import get_brands, get_models, get_vehicle_years,get_shops, get_cars, get_shop_id, get_brand_id_by_name, set_car_register
from lib.auth import check_authentication, get_user_store_assignment


st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Pesquisador")
st.write("Bem vindo de volta Pesquisador. Insira os preços dos carros da loja pesquisada")


shops = get_shops()
store_names = {shop.name:shop.id  for shop in shops} if shops else {}  # Assume que o nome da loja está na segunda posição da tupla
selected_store = st.selectbox("Selecione a loja", list(store_names.keys()))

brands = get_brands()
brand_options = {brand.name: brand.id for brand in brands} if brands else {}

    # Dropdown de marcas
marca_selecionada = st.selectbox("Marca", ["Selecione"] + list(brand_options.keys()))

    # Se a marca foi selecionada, busca os modelos
if marca_selecionada != "Selecione":
    brand_id = get_brand_id_by_name(marca_selecionada)

    models = get_models(brand_id)
    models_names = {model.name: model.id for model in models} if models else {}

    # Dropdown de modelos
    modelo_selecionado = st.selectbox("Modelo", ["Selecione"] + list(models_names.keys()))

    # Se um modelo foi selecionado, busca os anos disponíveis
    if modelo_selecionado != "Selecione":
        model_id = models_names[modelo_selecionado]
        years = get_vehicle_years(model_id=model_id)

        ano_selecionado = st.selectbox("Ano do veículo", ["Selecione"] + years)
            
# Campo para inserir o preço
        price = st.number_input("Informe o preço", min_value=0.0, format="%.2f")

        # Botão para salvar o preço
        if st.button("Salvar Preço"):
            if model_id and ano_selecionado and price:
                set_car_register(marca_selecionada, model_id,ano_selecionado, store_names[selected_store], str(price))
                st.success("Preço cadastrado com sucesso!")
            else:
                st.error("Erro ao cadastrar o preço. Verifique os dados e tente novamente.")
