import os
from sched import scheduler
from typing import List
import streamlit as st
import dotenv
import pandas as pd
from lib.auth import Authenticator
from lib.data import (get_models,check_user_role, get_avg_price_by_car, get_brands, get_cars, initialize_data, set_role_to_user,
 get_vehicle_years,get_shops, get_cars, get_shop_id, get_brand_id_by_name, set_car_register)
st.set_page_config(
    page_title="Tabela Fipe",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)
dotenv.load_dotenv()
#create_all_tables()
'''
def rodar_agendador():
    """Executa o agendador em loop para verificar tarefas pendentes."""
    scheduler.every().day.at("03:00").do(update_average_price)  # Define a tarefa para 03:00 AM

    while True:
        schedule.run_pending()
        time.sleep(60)  # Espera 60 segundos antes de verificar novamente

# Garantir que o agendador só seja iniciado uma vez
if "agendador_iniciado" not in st.session_state:
    st.session_state["agendador_iniciado"] = True  # Marca como iniciado
    thread = threading.Thread(target=rodar_agendador, daemon=True)
    thread.start()
'''


# Initialize session state variables if they don't exist
if "connected" not in st.session_state:
    st.session_state["connected"] = False
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "user_role" not in st.session_state:  # Adicionando controle de papéis
    st.session_state["user_role"] = None
if "logout" not in st.session_state:
    st.session_state["logout"] = False
if "autenticador" not in st.session_state:
    st.session_state["autenticador"] = None
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


# Creating a layout with columns to position the button in the top right corner
col1, col2 = st.columns([8, 2]) 

# Left part (Title)
with col1:
    st.title("Confira a melhor tabela do mercado")

# Right part (Login)
with col2:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    if not st.session_state["connected"]:   
        authenticator.check_auth()
        authenticator.login()
            
    else:
        email = st.session_state['user_info']['email']
        username = email.split("@")[0] 
        st.write(f"{username}")
   
    if st.button("Logout"):
            authenticator.logout()
            st.session_state["connected"] = False
            st.session_state["user_info"] = None
            st.session_state["user_role"] = None
            """ 
            # Atualiza a lista de e-mails e papéis após logout
            users = get_users()  # Atualiza os dados de usuários
            emails = [user[2] for user in users]  # Atualiza a lista de e-mails
            """
            # Re-atualiza a autenticação com os e-mails mais recentes
            """  emails_string = ",".join(emails)
            allowed_users = emails_string.split(",") 
            """

st.markdown("</div>", unsafe_allow_html=True)

#-------------------------------------------------------

# show content that requires login
if st.session_state["connected"]:
    email= st.session_state['user_info']['email'] 
    roles = st.session_state['user_role'].role
    gestor, pesquisador = st.columns(2)

    with gestor:
         # if email['role']== 'gestor':
        if st.button("Gestor", use_container_width=True):
            if check_user_role(email, 'manager'):
                st.session_state.user_role = 'manager'

                st.switch_page("pages/Manager.py")                    
                st.write("👨‍💼 [Gestor Acelera Sao Paulo](Manager.py)")

    with pesquisador:
        #if email['role']== 'pesquisador'  
        if st.button("Pesquisador", use_container_width=True):
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
                    
                    if not df:
                        st.warning("Nenhum resultado encontrado.")
                    else:
                        st.dataframe(df)
except Exception as e:
    st.error(f"Error fetching vehicle data: {str(e)}")
    st.info("Please try again later or contact support.")




if st.button("testar"):
    set_role_to_user(role_name='researcher', user_email='rodrigoquaglio@hotmail.com')
