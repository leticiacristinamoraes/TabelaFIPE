import streamlit as st
import pandas as pd
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.auth import check_authentication, get_all_users, add_user, update_user_role, update_user_store
from lib.data import get_researchers, get_stores


st.set_page_config(
    page_title="Gestor",
    page_icon="👨‍💼",
    layout="wide"
)


check_authentication(required_role="manager")


st.title("👨‍💼 Pagina do Gestor")
st.write("Bem vindo a pagina, acesse a lista de pesquisadores, lojas e gerencie usuarios")


with st.sidebar:
    st.title("🚗 FIPE")
    st.success(f"Logged in as Manager")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.rerun()
    
    
    st.subheader("Navigation")
    st.write("📊 [Home Page](/)")
    st.write("👨‍💼 [Manager Dashboard](/Manager)")


tab1, tab2, tab3 = st.tabs(["Researchers", "Stores", "User Management"])

with tab1:
    st.header("Researchers")
    researchers_data = get_researchers()
    
    
    with st.expander("Add New Researcher"):
        with st.form("add_researcher_form"):
            new_name = st.text_input("Name")
            new_email = st.text_input("Email")
            new_phone = st.text_input("Phone")
            
            submit_button = st.form_submit_button("Add Researcher")
            if submit_button and new_name and new_email:
                
                new_id = max([r["id"] for r in researchers_data]) + 1 if researchers_data else 1
                
                
                researchers_data.append({
                    "id": new_id,
                    "name": new_name,
                    "email": new_email,
                    "phone": new_phone
                })
                
                
                st.session_state.researchers = researchers_data
                st.success(f"Researcher {new_name} added successfully!")
                st.rerun()
    
    
    if researchers_data:
        researchers_df = pd.DataFrame(researchers_data)
        st.dataframe(researchers_df, use_container_width=True)
    else:
        st.info("No researchers found. Add some using the form above.")

with tab2:
    st.header("Lojas")
    stores_data = get_stores()
    
    
    with st.expander("Adicionar Nova Loja"):
        with st.form("add_store_form"):
            new_name = st.text_input("Store Name")
            new_location = st.text_input("Location")
            new_contact = st.text_input("Contact Info")
            
            submit_button = st.form_submit_button("Add Store")
            if submit_button and new_name and new_location:
                
                new_id = max([s["id"] for s in stores_data]) + 1 if stores_data else 1
                
                
                stores_data.append({
                    "id": new_id,
                    "name": new_name,
                    "location": new_location,
                    "contact": new_contact
                })
                
                
                st.session_state.stores = stores_data
                st.success(f"Store {new_name} added successfully!")
                st.rerun()
    
    
    if stores_data:
        stores_df = pd.DataFrame(stores_data)
        st.dataframe(stores_df, use_container_width=True)
    else:
        st.info("No stores found. Add some using the form above.")

with tab3:
    st.header("User Management")
    
    
    users = get_all_users()
    stores_data = get_stores()
    
    
    users_list = []
    for username, user_data in users.items():
        
        store_name = "Not assigned"
        store_id = user_data.get("store_id")
        if store_id:
            for store in stores_data:
                if store["id"] == store_id:
                    store_name = store["name"]
                    break
        
        users_list.append({
            "username": username,
            "role": user_data["role"],
            "store_id": store_id,
            "store_name": store_name
        })
    
    
    if users_list:
        st.subheader("Existing Users")
        users_df = pd.DataFrame(users_list)
        st.dataframe(users_df, use_container_width=True)
    
    
    with st.expander("Adicionar novo usuario"):
        with st.form("add_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["manager", "researcher"])
            
            
            store_options = {store['name']: store['id'] for store in stores_data}
            store_options["Not Assigned"] = None
            selected_store = st.selectbox("Assign to Store", options=list(store_options.keys()))
            selected_store_id = store_options[selected_store]
            
            submit_button = st.form_submit_button("Add User")
            if submit_button and new_username and new_password:
                success, message = add_user(
                    username=new_username, 
                    password=new_password, 
                    role=new_role, 
                    store_id=selected_store_id
                )
                
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    
    with st.expander("Update User Role"):
        with st.form("update_role_form"):
            username_options = list(users.keys())
            selected_username = st.selectbox("Select User", options=username_options, key="role_username")
            new_role = st.selectbox("New Role", ["manager", "researcher"], key="role_selection")
            
            submit_button = st.form_submit_button("Update Role")
            if submit_button and selected_username:
                success, message = update_user_role(selected_username, new_role)
                
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    
    with st.expander("Assign User to Store"):
        with st.form("assign_store_form"):
            
            researcher_users = [username for username, user_data in users.items() 
                              if user_data["role"] == "researcher"]
            
            if researcher_users:
                selected_username = st.selectbox("Select Researcher", options=researcher_users)
                
                store_options = {store['name']: store['id'] for store in stores_data}
                store_options["Not Assigned"] = None
                selected_store = st.selectbox("Assign to Store", options=list(store_options.keys()), key="store_assignment")
                selected_store_id = store_options[selected_store]
                
                submit_button = st.form_submit_button("Update Store Assignment")
                if submit_button and selected_username:
                    success, message = update_user_store(selected_username, selected_store_id)
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.info("No researchers found. Add some users with researcher role first.")
