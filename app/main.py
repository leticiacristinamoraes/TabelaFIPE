import streamlit as st
import pandas as pd
import requests
from lib.auth import check_password, login_button
from lib.data import initialize_data
from api.fipe_api import get_brands, get_models, get_years, get_vehicle_price


st.set_page_config(
    page_title="Tabela Fipe",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None


initialize_data()


with st.sidebar:
    st.title("🚗 FIPE")
    
    if not st.session_state.authenticated:
        login_button()
    else:
        st.success(f"Logged in as {st.session_state.user_role.capitalize()}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.rerun()
        
        
        st.subheader("Navigation")
        st.write("📊 [Home Page](/)")
        
        if st.session_state.user_role == 'manager':
            st.write("👨‍💼 [Gestor Acelera Sao Paulo](Manager.py)")
        elif st.session_state.user_role == 'researcher':
            st.write("🔍 [Pesquisador](Researcher.py)")


st.title("Tabela de preços")
st.write("Venha conhecer os diversos preços no Brasil")


try:
    
    brands = get_brands()
    brand_options = {brand['nome']: brand['codigo'] for brand in brands}
    selected_brand_name = st.selectbox("Marca", options=list(brand_options.keys()))
    selected_brand_code = brand_options[selected_brand_name]

    
    if selected_brand_code:
        models = get_models(selected_brand_code)
        model_options = {model['nome']: model['codigo'] for model in models['modelos']}
        selected_model_name = st.selectbox("Modelo", options=list(model_options.keys()))
        selected_model_code = model_options[selected_model_name]

        
        if selected_model_code:
            years = get_years(selected_brand_code, selected_model_code)
            year_options = {year['nome']: year['codigo'] for year in years}
            selected_year_name = st.selectbox("Ano", options=list(year_options.keys()))
            selected_year_code = year_options[selected_year_name]

            
            if selected_year_code:
                with st.spinner("Fetching price information..."):
                    price_info = get_vehicle_price(selected_brand_code, selected_model_code, selected_year_code)
                    
                    if price_info:
                        st.subheader("Informacao do Veiculo")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Marca:** {price_info['Marca']}")
                            st.markdown(f"**Modelo:** {price_info['Modelo']}")
                            st.markdown(f"**Ano:** {price_info['AnoModelo']}")
                            st.markdown(f"**Combustivel:** {price_info['Combustivel']}")
                        
                        with col2:
                            st.markdown(f"**ID:** {price_info['CodigoFipe']}")
                            st.markdown(f"**Mes Referencia:** {price_info['MesReferencia']}")
                            st.markdown(f"**Preco Fipe:** {price_info['Valor']}")
                            st.markdown(f"**Ultima Atualizacao:** {price_info.get('Data', 'N/A')}")
except Exception as e:
    st.error(f"Error fetching vehicle data: {str(e)}")
    st.info("Please try again later or contact support.")
