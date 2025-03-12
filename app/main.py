import asyncio
import uuid
import streamlit as st
from sqlalchemy import UUID, Uuid
import db.repositories.user_repo as user_repository
from db.db_model.db_base_postgresql import Session

def main():
    user_repo = user_repository.UserPostgresqlRepository(Session)
    if st.button("Criar"):
        
        user = user_repo.create('rst3', 'rodrigo3@hotmail.com')
        st.write(user)
    if st.button("getall"):
        users = user_repo.get(uuid.UUID('3b0177df-bad9-4c1a-89d4-603dd60b12a2'))
        st.write(users)

if __name__ == "__main__":
    main()