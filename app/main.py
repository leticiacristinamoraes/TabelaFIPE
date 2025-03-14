import os
import streamlit as st
import dotenv
import pandas as pd
from lib.auth import Authenticator
from lib.data import check_user_role, get_avg_price_by_car, get_cars, initialize_data, set_role_to_user
from lib.data import get_models, get_vehicle_years,get_shops, get_cars, get_shop_id, get_brand_id_by_name, set_car_register

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
st.set_page_config(
    page_title="Tabela Fipe",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Tabela de preços de veículos")

# Inicializa autenticação

authenticator = Authenticator(
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
    '''
    conn = get_connection()
    cur = conn.cursor()  # Agora o cursor está definido corretamente
    '''
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
    brand_options = [brand.name for brand in cars]

    # Dropdown de marcas
    marca_selecionada = st.selectbox("Marca", ["Selecione"] + brand_options)

    # Se a marca foi selecionada, busca os modelos
    if marca_selecionada != "Selecione":
        brand_id = get_brand_id_by_name(marca_selecionada)
        models = get_models(brand_id)
        models_names = [model.name for model in models]

        # Dropdown de modelos
        modelo_selecionado = st.selectbox("Modelo", ["Selecione"] + models_names)

        # Se um modelo foi selecionado, busca os anos disponíveis
        if modelo_selecionado != "Selecione":
            model_id = [model.id for model in models if model.name == modelo_selecionado]
            year_options = get_vehicle_years(model_id=model_id)
            ano_selecionado = st.selectbox("Ano do veículo", ["Selecione"] + year_options)
                
            if ano_selecionado:
                with st.spinner("Fetching price information..."):
                    df = get_avg_price_by_car(marca_selecionada,modelo_selecionado, ano_selecionado)
                    
                    if df.empty:
                        st.warning("Nenhum resultado encontrado.")
                    else:
                        st.dataframe(df)
except Exception as e:
    st.error(f"Error fetching vehicle data: {str(e)}")
    st.info("Please try again later or contact support.")




if st.button("testar"):
    set_role_to_user(role_name='researcher', user_email='rodrigoquaglio@hotmail.com')
