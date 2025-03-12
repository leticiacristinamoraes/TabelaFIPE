import time
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from app.lib.token_manager import AuthTokenManager
secret_path = os.path.abspath("app/lib/client_secret.json")
class Authenticator:
    def __init__(
        self,
        allowed_users: list,
        secret_path: str,
        redirect_uri: str,
        token_key: str,
        cookie_name: str = "auth_jwt",
        token_duration_days: int = 1,
    ):
        st.session_state["connected"] = st.session_state.get("connected", False)
        self.allowed_users = allowed_users
        self.secret_path = secret_path
        self.redirect_uri = redirect_uri
        self.auth_token_manager = AuthTokenManager(
            cookie_name=cookie_name,
            token_key=token_key,
            token_duration_days=token_duration_days,
        )
        self.cookie_name = cookie_name
        self.valido = None

    def _initialize_flow(self) -> google_auth_oauthlib.flow.Flow:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.secret_path,
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
            ],
            redirect_uri=self.redirect_uri,
        )
        return flow

    def get_auth_url(self) -> str:
        flow = self._initialize_flow()
        auth_url, _ = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )
        return auth_url

    def login(self):
        if not st.session_state["connected"]:
            auth_url = self.get_auth_url()
            st.markdown(f'<a href="{auth_url}" target="_self" style="display: inline-block; padding: 0.5rem 1rem; font-weight: 400; text-align: center; text-decoration: none; border-radius: 0.25rem; color: rgb(255, 255, 255); background-color: rgb(19, 23, 32); border: 1px solid rgba(250, 250, 250, 0.2); cursor: pointer;">Entre com google</a>', unsafe_allow_html=True)

    def check_auth(self):

        if st.session_state["connected"]:
            st.toast(":green[user is authenticated]")
            return

        if st.session_state.get("logout"):
            st.toast(":green[user logged out]")
            return

        token = self.auth_token_manager.get_decoded_token()
        if token is not None:
            st.query_params.clear()
            st.session_state["connected"] = True
            st.session_state["user_info"] = {
                "email": token["email"],
                "oauth_id": token["oauth_id"],
            }
            st.rerun()  # update session state

        time.sleep(1)  # important for the token to be set correctly

        auth_code = st.query_params.get("code")
        st.query_params.clear()
        if auth_code:
            flow = self._initialize_flow()
            flow.fetch_token(code=auth_code)
            creds = flow.credentials

            oauth_service = build(serviceName="oauth2", version="v2", credentials=creds)
            user_info = oauth_service.userinfo().get().execute()
            oauth_id = user_info.get("id")
            email = user_info.get("email")

            if email in self.allowed_users:
                self.auth_token_manager.set_token(email, oauth_id)
                st.session_state["connected"] = True
                st.session_state["user_info"] = {
                    "oauth_id": oauth_id,
                    "email": email,
                }
                self.valido = True
            else:
                st.toast(":red[access denied: Unauthorized user]")
                self.valido = False
            # no rerun

    def logout(self):
        st.session_state["logout"] = True
        st.session_state["user_info"] = None
        st.session_state["connected"] = None
        self.auth_token_manager.delete_token()
        # no rerun
        
import streamlit as st
import hashlib
import base64

#
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

# def check_password(username, password):
#     """Check if username/password combination is valid."""
#     users = initialize_users()
#     if username in users:
#         stored_hash = users[username]["password_hash"]
#         input_hash = hashlib.sha256(password.encode()).hexdigest()
#         if stored_hash == input_hash:
#             return True, users[username]["role"]
#     return False, None

def get_user_store_assignment(username):
    """Get the store assigned to a user"""
    users = initialize_users()
    if username in users:
        return users[username].get("store_id")
    return None


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
        