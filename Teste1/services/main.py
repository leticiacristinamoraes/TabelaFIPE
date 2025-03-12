import streamlit as st
import time
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.auth import Authenticator


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
allowed_users = os.getenv("ALLOWED_USERS").split(",")

authenticator = Authenticator(
                allowed_users=allowed_users,
                token_key=os.getenv("TOKEN_KEY"),
                secret_path="client_secret.json",
                redirect_uri="http://localhost:8501",
            )

#-------------------------------------------------------

# Creating a layout with columns to position the button in the top right corner
col1, col2 = st.columns([8, 2]) 

# Left part (Title)
with col1:
    st.title("Tabela FIPE")

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
    gestor, pesquisador = st.columns(2)
    with gestor:
        if st.button("Gestor", use_container_width=True):
            st.switch_page("pages/gestor.py")
    with pesquisador:
        if st.button("Pesquisador", use_container_width=True):
            st.switch_page("pages/pesquisador.py")

if authenticator.valido == False:
    st.write(f"Email inválido, entre em contato com o administrador.")

