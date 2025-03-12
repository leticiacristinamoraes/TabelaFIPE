import requests
import streamlit as st


BASE_URL = "https://parallelum.com.br/fipe/api/v1/carros"

@st.cache_data(ttl=3600)
def get_brands():
    """Get all car brands from FIPE API."""
    try:
        response = requests.get(f"{BASE_URL}/marcas")
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching brands: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def get_models(brand_code):
    """Get all models for a specific brand."""
    try:
        response = requests.get(f"{BASE_URL}/marcas/{brand_code}/modelos")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching models: {str(e)}")
        return {"modelos": []}

@st.cache_data(ttl=3600)
def get_years(brand_code, model_code):
    """Get all years for a specific model."""
    try:
        response = requests.get(f"{BASE_URL}/marcas/{brand_code}/modelos/{model_code}/anos")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching years: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def get_vehicle_price(brand_code, model_code, year_code):
    """Get price information for a specific vehicle."""
    try:
        response = requests.get(f"{BASE_URL}/marcas/{brand_code}/modelos/{model_code}/anos/{year_code}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching vehicle price: {str(e)}")
        return None
