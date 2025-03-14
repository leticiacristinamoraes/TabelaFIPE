import streamlit as st

def initialize_data():
    """Initialize data structures in session state if they don't exist."""
    
    if 'researchers' not in st.session_state:
        st.session_state.researchers = [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1987654321"
            }
        ]
    
    
    if 'stores' not in st.session_state:
        st.session_state.stores = [
            {
                "id": 1,
                "name": "AutoMax",
                "location": "São Paulo, SP",
                "contact": "contact@automax.com"
            },
            {
                "id": 2,
                "name": "CarWorld",
                "location": "Rio de Janeiro, RJ",
                "contact": "info@carworld.com"
            },
            {
                "id": 3,
                "name": "Elite Motors",
                "location": "Brasília, DF",
                "contact": "sales@elitemotors.com"
            }
        ]
    
    
    if 'evaluations' not in st.session_state:
        st.session_state.evaluations = [
            {
                "id": 1,
                "store_id": 1,
                "store_name": "AutoMax",
                "brand": "Fiat",
                "model": "Uno",
                "year": "2020 Gasolina",
                "evaluated_price": 35000.0,
                "condition": "Good",
                "notes": "Minor scratches on the right door",
                "date": "2023-05-10 14:30:00",
                "researcher": "researcher"
            },
            {
                "id": 2,
                "store_id": 2,
                "store_name": "CarWorld",
                "brand": "Volkswagen",
                "model": "Gol",
                "year": "2019 Flex",
                "evaluated_price": 45000.0,
                "condition": "Excellent",
                "notes": "Like new, low mileage",
                "date": "2023-05-15 09:15:00",
                "researcher": "researcher"
            }
        ]

def get_researchers():
    """Get researchers data from session state."""
    if 'researchers' not in st.session_state:
        initialize_data()
    return st.session_state.researchers

def get_stores():
    """Get stores data from session state."""
    if 'stores' not in st.session_state:
        initialize_data()
    return st.session_state.stores

def get_evaluations():
    """Get evaluations data from session state."""
    if 'evaluations' not in st.session_state:
        initialize_data()
    return st.session_state.evaluations
