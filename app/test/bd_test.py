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
        shop = shop_repo.create('shop 1')
        car = car_repo.create('peugeot', '206', '2000 gasolina')
        register = register_repo.create(car_id=car.id, shop_id=shop.id, price='10000'),
        
        st.write(shop)
        st.write(car)
        st.write(register)
    if st.button("getall"):
        users = user_repo.get(uuid.UUID('3b0177df-bad9-4c1a-89d4-603dd60b12a2'))
        st.write(users)

if __name__ == "__main__":
    main()