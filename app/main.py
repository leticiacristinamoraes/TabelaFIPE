import streamlit as st
import os
from dotenv import load_dotenv
import threading
#import schedule
import time
import sys
import pandas as pd
import psycopg2
from database.create_tables import create_all_tables
from database.config import get_connection
from database.brands import get_brands
from database.models import get_models
from database.users import get_users
from database.db_populate import populate_database
from database.vehicles import get_vehicle_years
from database.average_price import calculate_and_update_average_price

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

# Initialize session state variables if they don't exist
if "connected" not in st.session_state:
    st.session_state["connected"] = False
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "user_role" not in st.session_state:  # Adicionando controle de papéis
    st.session_state["user_role"] = None
if "logout" not in st.session_state:
    st.session_state["logout"] = False
if "user_id" not in st.session_state:  # Adicionando controle de papéis
    st.session_state["user_id"] = None
if "autenticador" not in st.session_state:
    st.session_state["autenticador"] = None

users = get_users()  # Chama a função get_users() que retorna todos os usuários
emails = [user[2] for user in users]

# Inicializa autenticação
emails_string = ",".join(emails)
allowed_users = emails_string.split(",")
authenticator = Authenticator(
    allowed_users=allowed_users,
    token_key=os.getenv("TOKEN_KEY"),
    secret_path="client_secret.json",
    redirect_uri="http://localhost:8501",
)

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

            # Atualiza a lista de e-mails e papéis após logout
            users = get_users()  # Atualiza os dados de usuários
            emails = [user[2] for user in users]  # Atualiza a lista de e-mails

            # Re-atualiza a autenticação com os e-mails mais recentes
            emails_string = ",".join(emails)
            allowed_users = emails_string.split(",")

st.markdown("</div>", unsafe_allow_html=True)

# show content that requires login
if st.session_state["connected"]:
    email= st.session_state['user_info']['email'] 
    for user in users:
            if user[2] == email:  # user[2] é o campo "email" na tupla
                st.session_state.user_role = user[3]
                st.session_state.user_id = user[0]
    
   #
    gestor, pesquisador = st.columns(2)
    with gestor:
         # if email['role']== 'gestor':
        if st.button("Gestor", use_container_width=True) and st.session_state.user_role == 'gestor':
              st.switch_page("pages/Manager.py")                    
              st.write("👨‍💼 [Gestor Acelera Sao Paulo](Manager.py)")
            
    with pesquisador:
        #if email['role']== 'pesquisador'  
        if st.button("Pesquisador", use_container_width=True) and st.session_state.user_role == 'pesquisador':
               st.write("🔍 [Pesquisador](Researcher.py)")
               st.switch_page("pages/Researcher.py")
          
if authenticator.valido == False:
    st.write(f"Email inválido, entre em contato com o administrador.")

st.title("Tabela de preços")
st.write("Venha conhecer os diversos preços no Brasil")

# Estados de sessão para armazenar os filtros selecionados
if "selected_brand" not in st.session_state:
    st.session_state["selected_brand"] = None
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = None
if "selected_year" not in st.session_state:
    st.session_state["selected_year"] = None
  
def buscar_precos_medios(marca=None, modelo=None, ano=None):
    """Retorna os preços médios dos veículos já armazenados na tabela average_price."""
    conn = get_connection()
    cur = conn.cursor()

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
    if ano:
        query += " AND v.ano_fab = %s"
        params.append(ano)

    cur.execute(query, tuple(params))
    resultados = cur.fetchall()

    cur.close()
    conn.close()

    import pandas as pd
    df = pd.DataFrame(resultados, columns=["Marca", "Modelo", "Ano Fabricação", "Ano Modelo", "Preço Médio"])
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
                df = buscar_precos_medios(marca_selecionada, modelo_selecionado, ano_selecionado)
    
                if df.empty:
                   st.warning("Nenhum resultado encontrado.")
                else:
                    st.dataframe(df)  # Exibe a tabela completa
        
        # Exibir o preço médio destacado
                    preco_medio = df["Preço Médio"].mean()  # Como já buscamos da average_price, deve ser um único valor
                    if not pd.isna(preco_medio):
                       st.metric(label="Preço Médio do Veículo", value=f"R$ {preco_medio:,.2f}")



