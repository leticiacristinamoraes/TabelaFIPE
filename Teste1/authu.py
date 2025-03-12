import streamlit as st
import hashlib
import base64


def initialize_users():
    if 'users' not in st.session_state:
        st.session_state.users = {
            "manager": {
                "username": "manager",
                "password_hash": hashlib.sha256("manager123".encode()).hexdigest(),
                "role": "manager",
                "store_id": None  
            },
            "researcher": {
                "username": "researcher",
                "password_hash": hashlib.sha256("researcher123".encode()).hexdigest(),
                "role": "researcher",
                "store_id": 1  
            }
        }
    return st.session_state.users

def check_password(username, password):
    """Check if username/password combination is valid."""
    users = initialize_users()
    if username in users:
        stored_hash = users[username]["password_hash"]
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        if stored_hash == input_hash:
            return True, users[username]["role"]
    return False, None

def get_user_store_assignment(username):
    """Get the store assigned to a user"""
    users = initialize_users()
    if username in users:
        return users[username].get("store_id")
    return None

def login_button():
    """Display login form in sidebar."""
    st.subheader("Login")
    
    #username = st.text_input("Username", key="login_username")
    #password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password")
            return
        
        is_valid, role = check_password(username, password)
        
        if is_valid:
            st.session_state.authenticated = True
            st.session_state.user_role = role
            st.session_state.username = username
            st.session_state.user_store = get_user_store_assignment(username)
            st.success(f"Logged in as {role}")
            st.rerun()
        else:
            st.error("Invalid username or password")

def add_user(username, password, role, store_id=None):
    """Add a new user to the system"""
    users = initialize_users()
    if username in users:
        return False, "Username already exists"
    
    
    users[username] = {
        "username": username,
        "password_hash": hashlib.sha256(password.encode()).hexdigest(),
        "role": role,
        "store_id": store_id
    }
    return True, "User added successfully"

def update_user_role(username, new_role):
    """Update a user's role"""
    users = initialize_users()
    if username not in users:
        return False, "User does not exist"
    
    users[username]["role"] = new_role
    return True, "User role updated successfully"

def update_user_store(username, store_id):
    """Assign a store to a user"""
    users = initialize_users()
    if username not in users:
        return False, "User does not exist"
    
    users[username]["store_id"] = store_id
    return True, "User store assignment updated successfully"

def get_all_users():
    """Get all users"""
    return initialize_users()

def check_authentication(required_role=None):
    """Check if user is authenticated and has the required role."""
    if not st.session_state.get('authenticated', False):
        st.error("Please login to access this page")
        st.stop()
    
    if required_role and st.session_state.get('user_role') != required_role:
        st.error(f"You need to be a {required_role} to access this page")
        st.stop()
