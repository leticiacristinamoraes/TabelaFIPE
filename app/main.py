import streamlit as st
<<<<<<< HEAD


from lib.data import check_user_role, get_avg_price_by_car, get_cars, initialize_data, set_role_to_user

=======
import os
from dotenv import load_dotenv
import sys
import pandas as pd
import psycopg2
from database.create_tables import create_all_tables
from database.config import get_connection
from database.brands import get_brands
from database.models import get_models
from database.db_populate import populate_database
from database.vehicles import get_vehicle_years

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.lib.auth import Authenticator
>>>>>>> f24d94c2e88c03a6ff8fa34ed2a7776808768202

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

<<<<<<< HEAD
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None


initialize_data()
#----
import streamlit as st
import time
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.lib.auth import Authenticator


load_dotenv()

# Initialize session state variables if they don't exist
if "connected" not in st.session_state:
    st.session_state["connected"] = False
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "logout" not in st.session_state:
    st.session_state["logout"] = False
if "autenticador" not in st.session_state:
    st.session_state["autenticador"] = None


# emails of users that are allowed to login
#allowed_users = os.getenv("ALLOWED_USERS").split(",")
#allowed_users = os.getenv("ALLOWED_USERS", "user1,user2,user3").split(",")
authenticator = Authenticator(
                token_key=os.getenv("TOKEN_KEY"),
                redirect_uri="http://localhost:8501",
            )
=======
# Inicializa autenticação
allowed_users = os.getenv("ALLOWED_USERS").split(",")
authenticator = Authenticator(
    allowed_users=allowed_users,
    token_key=os.getenv("TOKEN_KEY"),
    secret_path="client_secret.json",
    redirect_uri="http://localhost:8501",
)
>>>>>>> f24d94c2e88c03a6ff8fa34ed2a7776808768202

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
    cur = conn.cursor()  # Agora o cursor está definido corretamente

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

<<<<<<< HEAD
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
    
    cars = get_cars()
    brand_options = {car.brand: i for i,car in enumerate(cars)}
    selected_brand_name = st.selectbox("Marca", options=list(brand_options.keys()))
    selected_brand_code = brand_options[selected_brand_name]

    
    if selected_brand_code:
        model_options = {car.model: i for i,car in enumerate(cars)}
        selected_model_name = st.selectbox("Modelo", options=list(model_options.keys()))
        selected_model_code = model_options[selected_model_name]

        
        if selected_model_code:
            year_options = {car.model_year: i for i,car in enumerate(cars)}
            selected_year_name = st.selectbox("Ano", options=list(year_options.keys()))
            selected_year_code = year_options[selected_year_name]

            
            if selected_year_code:
                with st.spinner("Fetching price information..."):
                    price_info = get_avg_price_by_car(selected_brand_name,selected_model_name, selected_year_name)
                    
                    if price_info:
                        st.subheader("Informacao do Veiculo")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Marca:** {selected_brand_name}")
                            st.markdown(f"**Modelo:** {selected_model_name}")
                            st.markdown(f"**Ano:** {selected_year_name}")
                        
                        with col2:
                            st.markdown(f"**Preco Fipe:** {price_info.avg_price}")
except Exception as e:
    st.error(f"Error fetching vehicle data: {str(e)}")
    st.info("Please try again later or contact support.")




if st.button("testar"):
    set_role_to_user(role_name='researcher', user_email='rodrigoquaglio@hotmail.com')
=======
    cur.execute(query, tuple(params))
    resultados = cur.fetchall()  # Pega os resultados da query

    
    colunas = ["Marca", "Modelo", "Ano Fabricação", "Ano Modelo", "Preço Médio"]
    
    df = pd.DataFrame(resultados, columns=colunas)

    cur.close()
    conn.close()
    return df

st.title("Consulta Pública de Preços de Veículos")

# Obtém a lista de marcas do banco de dados
marcas = get_brands()  
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


>>>>>>> f24d94c2e88c03a6ff8fa34ed2a7776808768202
