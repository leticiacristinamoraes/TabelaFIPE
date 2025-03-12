import streamlit as st
import pandas as pd
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from auth import check_authentication, get_user_store_assignment
from data import get_stores, get_evaluations
from fipe_api import get_brands, get_models, get_years


st.set_page_config(
    page_title="Pagina de Pesquisador",
    page_icon="🔍",
    layout="wide"
)


check_authentication(required_role="researcher")


st.title("🔍 Pesquisador")
st.write("Bem vindo de volta Pesquisador. Insira os preços dos carros da loja pesquisada")


with st.sidebar:
    st.title("🚗 FIPE")
    st.success(f"Logado como Pesquisador")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.rerun()
    
    
    st.subheader("Navigation")
    st.write("📊 [Home Page](/)")
    st.write("🔍 [Researcher Dashboard](/Researcher)")


st.header("Insira a pesquisa")

col1, col2 = st.columns(2)


if 'evaluations' not in st.session_state:
    st.session_state.evaluations = []

with st.form("vehicle_evaluation_form"):
    
    stores = get_stores()
    user_store_id = st.session_state.get('user_store')
    
    if user_store_id:
        
        assigned_store_name = "Unknown Store"
        for store in stores:
            if store['id'] == user_store_id:
                assigned_store_name = store['name']
                break
                
        st.info(f"You are assigned to: {assigned_store_name}")
        selected_store = assigned_store_name
        store_id = user_store_id
    else:
        
        store_options = {store['name']: store['id'] for store in stores}
        selected_store = st.selectbox("Loja", options=list(store_options.keys()))
        store_id = store_options[selected_store]
    
    
    try:
        
        brands = get_brands()
        brand_options = {brand['nome']: brand['codigo'] for brand in brands}
        selected_brand_name = st.selectbox("Marca", options=list(brand_options.keys()))
        selected_brand_code = brand_options[selected_brand_name]

        
        models = get_models(selected_brand_code)
        model_options = {model['nome']: model['codigo'] for model in models['modelos']}
        selected_model_name = st.selectbox("Modelo", options=list(model_options.keys()))
        selected_model_code = model_options[selected_model_name]

        
        years = get_years(selected_brand_code, selected_model_code)
        year_options = {year['nome']: year['codigo'] for year in years}
        selected_year_name = st.selectbox("Ano", options=list(year_options.keys()))
        selected_year_code = year_options[selected_year_name]

        
        evaluated_price = st.number_input("Preço levantado (R$)", min_value=0.0, step=100.0)
        
        
        vehicle_condition = st.selectbox("Vehicle Condition", 
                                        options=["Excellent", "Good", "Fair", "Poor"])
        notes = st.text_area("Additional Notes")
        
        
        submitted = st.form_submit_button("Enviar pesquisa")
        
        if submitted:
            if evaluated_price <= 0:
                st.error("Please enter a valid price.")
            else:
                
                new_evaluation = {
                    "id": len(st.session_state.evaluations) + 1,
                    "store_id": store_id,
                    "store_name": selected_store,
                    "brand": selected_brand_name,
                    "model": selected_model_name,
                    "year": selected_year_name,
                    "evaluated_price": evaluated_price,
                    "condition": vehicle_condition,
                    "notes": notes,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "researcher": st.session_state.username
                }
                
                
                st.session_state.evaluations.append(new_evaluation)
                st.success("Vehicle evaluation submitted successfully!")
                
    except Exception as e:
        st.error(f"Error in vehicle selection: {str(e)}")
        st.info("Please try again or contact support.")


st.header("Your Previous Evaluations")
evaluations = get_evaluations()


if 'username' in st.session_state:
    user_evaluations = [e for e in evaluations if e.get('researcher') == st.session_state.username]
    
    if user_evaluations:
        evaluations_df = pd.DataFrame(user_evaluations)
        st.dataframe(evaluations_df, use_container_width=True)
    else:
        st.info("You haven't submitted any evaluations yet.")
