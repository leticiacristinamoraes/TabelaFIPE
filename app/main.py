import streamlit as st
import os
from dotenv import load_dotenv
import threading
import time
import sys
import pandas as pd
import psycopg2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.create_tables import create_all_tables
from database.config import get_connection
from database.brands import get_brands
from database.models import get_models
from database.users import get_users
from database.db_populate import populate_database
from database.vehicles import get_vehicle_years
from database.average_price import calculate_and_update_average_price
from database.researcher_commission import  update_commission
from app.lib.auth import Authenticator

load_dotenv()
create_all_tables()

# def database_ja_populado():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT COUNT(*) FROM brands;")
#     count = cur.fetchone()[0]
#     conn.close()
#     return count > 0 

# if not database_ja_populado():
#     populate_database()


# Função para rodar o agendador
def rodar_agendador():
    """Executa o agendador em loop para verificar tarefas pendentes."""
    
    
    schedule.every().day.at("03:00").do(calculate_and_update_average_price)  # Define a tarefa para 03:00 AM
    schedule.every().month.at("03:30").do(update_commission)  # Define a tarefa para 03:30 AM no primeiro dia do mês

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

image_url = "https://i.imgur.com/JUvydxA.jpeg"

st.markdown(
    f"""
    <div style="width: 100%; display: flex; justify-content: center;">
        <img src="{image_url}" style="width: 100%; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)


# Opcional: legenda abaixo da imagem
st.markdown("<p style='text-align: center;'></p>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Confira os preços da Tabela FIPE para as marcas mais vendidas do Brasil!</h2>", unsafe_allow_html=True)

# Criar uma grade com os logos das marcas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image("data:image/png;base64,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", width=100)


with col2:
    st.image("data:image/png;base64,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", width=100)


with col3:
    st.image("data:image/jpeg;base64,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", width=100)

with col4:
    st.image("data:image/png;base64,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", width=100)


with col5:
    st.image("data:image/png;base64,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", width=100)


authenticator.check_auth()

# Creating a layout with columns to position the button in the top right corner
col1, col2 = st.columns([8, 2]) 

# Left part (Title)
with col1:
    st.title("")

# Right part (Login)
with col2:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    if not st.session_state["connected"]:   
        #authenticator.check_auth()
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
              #st.write("👨‍💼 [Gestor Acelera Sao Paulo](Manager.py)")
            
    with pesquisador:
        #if email['role']== 'pesquisador'  
        if st.button("Pesquisador", use_container_width=True) and st.session_state.user_role == 'pesquisador':
               #st.write("🔍 [Pesquisador](Researcher.py)")
               st.switch_page("pages/Researcher.py")
          
if authenticator.valido == False:
    st.write(f"Email inválido, entre em contato com o administrador.")



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



