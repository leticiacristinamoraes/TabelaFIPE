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
        role = role_repo.create(name='researcher')
        user2 = user_repo.create(name="leticia", email="leticiacristinafmds@gmail.com")
        role2 = role_repo.create(name='manager')
        permission = permission_repo.create(name='edit')
        user_role = user_role_repo.create(user.id, role.id)
        user_role2 = user_role_repo.create(user2.id, role2.id)
        shop = shop_repo.create('loja 1', 'rua 1', 'cnpj 1')
        shop2 = shop_repo.create('loja 2', 'rua 2', 'cnpj 2')
        
        brand = car_repo.create_brand('ferrari')
        model = car_repo.create_model(brand.id, 'f50')
        car = car_repo.create_car(model.id,2000)
        model2 = car_repo.create_model(brand.id, 'f40')
        car2 = car_repo.create_car(model2.id, 1985)
        brand3 = car_repo.create_brand('fiat')
        model3 = car_repo.create_model(brand3.id, 'palio')
        car3 = car_repo.create_car(model3.id, 2000)
        
        

    if st.button("getall"):
        role = role_permission_repo.create(role_id=uuid.UUID('e8b1e781-55c4-49dc-8db4-d41a83fcf6ec'), permission_id=uuid.UUID('07775ce9-3f77-4b4d-83a7-48b6d9ec4c82'))
        inner = user_role_repo.inner_join(uuid.UUID('4cd47035-f158-4a91-ab1d-5608de23a913'))
        st.write(inner)
        
if __name__ == "__main__":
    main()