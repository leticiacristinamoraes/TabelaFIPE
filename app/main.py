import streamlit as st


from lib.data import check_user_role, get_avg_price_by_car, get_cars, initialize_data, set_role_to_user



st.set_page_config(
    page_title="Tabela Fipe",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

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

#-------------------------------------------------------

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