import uuid
import streamlit as st
from db.db_model.db_instance import  (   
    user_repo, 
    car_repo,
    model_repo,
    brand_repo,
    register_repo, 
    shop_repo,
    permission_repo, 
    role_repo,
    user_shop_repo,
    role_permission_repo, 
    user_role_repo, 
    avg_price_repo
    )
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


def get_user_id(user_email):
    user = user_repo.get_user_by_email(user_email)
    return user.id

def get_role_id(role_name):
    role = role_repo.get_role_by_name(role_name)
    return role.id

def get_permission_id(permission_name):
    permission = permission_repo.get_permission_by_name(permission_name)
    return permission.id

def get_role_permissions(role_id):
    role_permissions = role_permission_repo.get_role_permission(role_id)
    return role_permissions

def check_user_role(user_email, role_name):
    user_id = get_user_id(user_email)
    role_id = get_role_id(role_name)
    check = user_role_repo.get_user_role_by_ids(user_id, role_id)
    return check


def check_role_permission(role_name, permission_name):
    try:
        role_id = get_role_id(role_name)
        permission_id = get_permission_id(permission_name)
        check = role_permission_repo.get_role_permission_by_ids(role_id=role_id, permission_id=permission_id)
        return True
    except:
        return ("usuario não tem papel atribuido.")  
    
def get_shop_id(shop_name):
    shop_id = shop_repo.get_shop_by_name(shop_name)
    return shop_id

def get_car_id(model_id, model_year):
    car = car_repo.get_car_by_fields(model_id, model_year)
    return car.id

def get_register_price_by_car(car_id):
    prices = register_repo.get_prices_by_car(car_id)
    return prices

def get_avg_price_by_car(model_id, model_year):
    car_id = get_car_id(model_id, model_year)
    avg_price = avg_price_repo.get_avg_price_by_car_id(car_id)
    return avg_price

def get_user_shops(user_id):
    user_shops = user_shop_repo.get_all_shops_by_user_id(user_id)
    return user_shops

def set_user(user_name, user_email):
    result = user_repo.create(user_name, user_email)
    return result

def set_role(role_name):
    result = role_repo.create(role_name)
    return result

def set_shop(shop_name):
    result = shop_repo.create(shop_name)
    return result

def set_permission(permission_name):
    result = permission_repo.create(permission_name)
    return result

def set_role_to_user(role_name, user_email):
    user_id = get_user_id(user_email=user_email)
    role_id = get_role_id(role_name=role_name)
    result = user_role_repo.create(user_id=user_id, role_id=role_id)
    return result

def set_permission_to_role(permission_name, role_name):
    permission_id = get_permission_id(permission_name=permission_name)
    role_id = get_role_id(role_name=role_name)
    result = role_permission_repo.create(role_id=role_id,permission_id=permission_id)
    return result

def set_user_to_shop(user_mail, shop_name):
    user_id = get_user_id(user_email=user_mail)
    shop_id = get_shop_id(shop_name=shop_name)
    result = user_shop_repo.create(user_id=user_id, shop_id=shop_id)
    return result

def set_car(brand, model,model_year):
    result = car_repo.create(brand, model, model_year)
    return result

def set_car_register(brand, model, model_year, price, shop_name):
    car_id = get_car_id(brand, model, model_year)
    shop_id = get_shop_id(shop_name)
    result = register_repo.create(car_id, shop_id, price)
    return result

def set_avg_price(car_id, avg_price):
    result = avg_price_repo.create(car_id=car_id, avg_price=avg_price)
    return result

def get_researchers():
    """Get researchers data from session state."""
    try:
        role_id = get_role_id('researcher')
        researchers = user_role_repo.get_users_by_role_id(role_id=role_id)        
        return researchers
    except:
        return ("Erro ao buscar researchers")
    
def get_shops():
    try:
        shops = shop_repo.get_all()
        return shops
    except:
        return ("Erro ao buscar lojas")
    
def get_cars():
    try:
        cars = car_repo.get_all()
        return cars
    except:
        return ("Erro ao buscar lojas")
    
def get_vehicle_years(model_id:uuid.UUID):

    years = car_repo.get_cars_years(model_id)
    print(years)
    return years

def get_brand_id_by_name(brand_name):
    try:
        brand_id = brand_repo.get_brand_id_by_name(brand_name)
      
        return brand_id
    except Exception as e:
        return (e)
    
def get_models(brand_id: uuid.UUID):
    try:
        models = model_repo.get_all_models(brand_id)
  
        return models
    except Exception as e:
        return (e)
    
def get_brands():
    try:
        brands = brand_repo.get_all_brands()
       
        return brands
    except:
        return ("Erro ao buscar lojas")
    
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
