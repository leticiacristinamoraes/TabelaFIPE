import os
from typing import List
import streamlit as st
import dotenv
import pandas as pd
from lib.auth import Authenticator
from lib.data import (get_models,check_user_role, get_avg_price_by_car, get_brands, get_cars, initialize_data, set_role_to_user,
 get_vehicle_years,get_shops, get_cars, get_shop_id, get_brand_id_by_name, set_car_register)

dotenv.load_dotenv()
#create_all_tables()
'''
def database_ja_populado():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM brands;")
    count = cur.fetchone()[0]
    conn.close()
    return count > 0 

if not database_ja_populado():
   populate_database()
'''
st.title("Tabela de preços de veículos")

# Inicializa autenticação

authenticator = Authenticator(
    token_key=os.getenv("TOKEN_KEY"),
    redirect_uri="http://localhost:8501",
)

# Estados de sessão para armazenar os filtros selecionados
if "selected_brand" not in st.session_state:
    st.session_state["selected_brand"] = None
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = None
if "selected_year" not in st.session_state:
    st.session_state["selected_year"] = None


st.markdown("</div>", unsafe_allow_html=True)

#-------------------------------------------------------

# show content that requires login
if st.session_state["connected"]:
    email= st.session_state['user_info']['email'] 
    
   #
    gestor, pesquisador = st.columns(2)
    with gestor:
         # if email['role']== 'gestor':
        if st.button("Gestor", use_container_width=True):
            if check_user_role('email@gmail.com', 'manager'):
                st.session_state.user_role = 'manager'

                st.switch_page("pages/Manager.py")                    
                st.write("👨‍💼 [Gestor Acelera Sao Paulo](Manager.py)")
            
    with pesquisador:
        #if email['role']== 'pesquisador'  
        if st.button("Pesquisador", use_container_width=True):
            if check_user_role('email@gmail.com', 'researcher'):
               st.session_state.user_role = 'researcher'
               st.write("🔍 [Pesquisador](Researcher.py)")
               st.switch_page("pages/Researcher.py")
               st.rerun()
    #else    
     #   st.write(f"Email inválido, entre em contato com o administrador.")        

if authenticator.valido == False:
    st.write(f"Email inválido, entre em contato com o administrador.")

#--


st.title("Tabela de preços")
st.write("Venha conhecer os diversos preços no Brasil")
try:

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
                
            if ano_selecionado != "Selecione":
                with st.spinner("Fetching price information..."):
                    df = get_avg_price_by_car(model_id, ano_selecionado)
                    
                    if df.empty:
                        st.warning("Nenhum resultado encontrado.")
                    else:
                        st.dataframe(df)
except Exception as e:
    st.error(f"Error fetching vehicle data: {str(e)}")
    st.info("Please try again later or contact support.")




if st.button("testar"):
    set_role_to_user(role_name='researcher', user_email='rodrigoquaglio@hotmail.com')
