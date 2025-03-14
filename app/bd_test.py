import asyncio
import uuid
import streamlit as st
from sqlalchemy import UUID, Uuid
import db.repositories.user_repo as user_repository
import db.repositories.car_repo as car_repository
import db.repositories.register_repo as register_repository
from db.db_model.db_instance import (
    engine, 
    user_repo, 
    car_repo, 
    register_repo, 
    shop_repo,
    permission_repo, 
    role_repo,
    user_shop_repo,
    role_permission_repo, 
    user_role_repo, 
    avg_price_repo
    )
from db.db_model.db_base_postgresql import Base

def on_startup():
    Base.metadata.create_all(bind=engine)
    
def main():
    on_startup()
    if st.button("Criar"):

        user = user_repo.create(name="rodrigo", email="rodrigoquaglio@gmail.com")
        st.write(user)

    if st.button("getall"):
        users = user_repo.get(uuid.UUID('e6a28446-6f61-4ea5-9c4c-a02a9b33e9f5'))
        role = role_repo.get(uuid.UUID('e194702b-4dec-40f4-b3d4-302721c8d955'))
        permission = permission_repo.get(uuid.UUID('c9ac81a4-517c-4325-ae44-76bc479fc7d5'))
        user_role = user_role_repo.get(uuid.UUID('ae39455b-65db-4f80-acde-7f66b1d1164e'))
        role_permission = role_permission_repo.get(uuid.UUID('959ef0cb-5a2d-4f91-84eb-0cb893e07e94'))
        shop = shop_repo.get(uuid.UUID('34b0b643-19a5-4109-b229-78b775955f6c'))
        car = car_repo.get(uuid.UUID('fab82697-665c-4a15-a9a6-3131d380f362'))
        register = register_repo.get(uuid.UUID('35538138-255f-462e-b9ed-d397c39844fc'))
        user_shop = user_shop_repo.get(uuid.UUID('10171321-8b62-4655-861c-9d1da048a9ca'))


        st.write(shop)
        st.write(car)
        st.write(register)
        st.write(users)
        st.write(role)
        st.write(permission)
        st.write(user_role)
        st.write(role_permission)
        st.write(user_shop)

if __name__ == "__main__":
    main()