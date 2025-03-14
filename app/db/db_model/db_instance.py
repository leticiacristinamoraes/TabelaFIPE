import time
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine
import db.repositories.user_repo as user_repository
import db.repositories.car_repo as car_repository
import db.repositories.register_repo as register_repository
import db.repositories.shop_repo as shop_repository
import db.repositories.permission_repo as permission_repository
import db.repositories.role_repo as role_repository
import db.repositories.role_permission_repo as role_permission_repository
import db.repositories.user_role_repo as user_role_repository
import db.repositories.user_shop_repo as user_shop_repository
import db.repositories.avg_price_repo as avg_price_repository
from sqlalchemy_utils import database_exists, create_database

#Classe para instanciar o banco de dados. 
url = 'postgresql+psycopg://postgres:postgres@localhost:5432/testDB4'
if not database_exists(url):
    create_database(url)
engine = create_engine(url, echo=True)

    


Session = scoped_session(sessionmaker(bind=engine))

#Após a criação do banco de dados, é necessário instanciar os repositórios
#para que seja possível realizar as operações de CRUD.

user_repo = user_repository.UserPostgresqlRepository(Session)
role_repo = role_repository.RolePostgresqlRepository(Session)
permission_repo = permission_repository.PermissionPostgresqlRepository(Session)
user_role_repo = user_role_repository.UserRolePostgresqlRepository(Session)
role_permission_repo = role_permission_repository.RolePermissionPostgresqlRepository(Session)
car_repo = car_repository.CarPostgresqlRepository(Session)
shop_repo = shop_repository.ShopPostgresqlRepository(Session)
user_shop_repo = user_shop_repository.UserShopPostgresqlRepository(Session)
register_repo = register_repository.RegisterPostgresqlRepository(Session)
avg_price_repo = avg_price_repository.AvgPricePostgresqlRepository(Session)