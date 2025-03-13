import uuid

from sqlalchemy import select, update, delete
from db.db_model.user_shop_sql import UserShopDBModel
from app.entities.user_shop import UserShop
from dataclasses import dataclass, asdict
from typing import Optional
from db.db_model.user_shop_sql import UserShopDBModel

# Classe de repositório de usuários e lojas para realizar CRUD com o banco de dados.
class UserShopPostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

    def __db_to_entity(
            self, db_row: UserShopDBModel
    ) -> Optional[UserShop]:
        return UserShop(
            id=db_row.id,
            user_id=db_row.user_id,
            shop_id=db_row.shop_id
        )

    def create(self, user_id: uuid.UUID, shop_id: uuid.UUID) -> Optional[UserShop]:
        """ Create user role
        :param user_id: str
        :param shop_id: str
        :return: Optional[user_shop]
        """
        user_shop_id = uuid.uuid4()
        user_shop_db_model = UserShopDBModel(
            id=user_shop_id,
            user_id=user_id,
            shop_id=shop_id
        )

        try:
            self.__session.add(user_shop_db_model)
            self.__session.commit()
            self.__session.refresh(user_shop_db_model)
        except:
            print("error")

        if user_shop_db_model is not None:
            return self.__db_to_entity(user_shop_db_model)
        return None

    def get(self, user_shop_id: uuid.UUID) -> Optional[UserShop]:
        """ Get user role by id
        :param user_shop_id: UserShopId
        :return: Optional[user_shop]
        """
        result = self.__session.execute(select(UserShopDBModel).where(UserShopDBModel.id == user_shop_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None
    
    def get_all(self) -> Optional[UserShop]:
        """ Get all users
        :return: Optional[user_shop]
        """
        result = self.__session.execute(select(UserShopDBModel)).fetchall()
        if result is not None:
            return [self.__db_to_entity(user_shop) for user_shop in result]
        return None
    def get_all_users_by_shop_id(self, shop_id: uuid.UUID) -> Optional[UserShop]:
        """ Get all users by shop_id

        :param shop_id: str
        :return: Optional[user_shop]
        """
        result = self.__session.execute(select(UserShopDBModel).where(UserShopDBModel.shop_id == shop_id)).fetchall()
        if result is not None:
            return [self.__db_to_entity(user_shop) for user_shop in result]
        return None
    
    def get_all_shops_by_user_id(self, user_id: uuid.UUID) -> Optional[UserShop]:
        """ Get all shops by user_id

        :param user_id: str
        :return: Optional[user_shop]
        """
        result = self.__session.execute(select(UserShopDBModel).where(UserShopDBModel.user_id == user_id)).fetchall()
        if result is not None:
            return [self.__db_to_entity(user_shop) for user_shop in result]
        return None
    
    def __get_user_shop_by_ids(self, user_id: uuid.UUID, shop_id: uuid.UUID) -> Optional[UserShop]:
        """ Get user role by user_id and role_id
        :param user_id: str
        :param shop_id: str
        :return: Optional[user_shop]
        """
        result = self.__session.execute(select(UserShopDBModel).where(UserShopDBModel.user_id == user_id and UserShopDBModel.shop_id == shop_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None
    
    def delete_by_ids(self, user_id: uuid.UUID, shop_id: uuid.UUID) -> Optional[UserShop]:
        """ Delete role permission by id
        :param role_permission_id: rolePermissionId
        :return: Optional[role_permission]
        """
        result =self.__get_user_shop_by_ids(user_id, shop_id)
        if result is not None:
            self.__session.execute(delete(UserShopDBModel).where(UserShopDBModel.id == result.id))
            self.__session.commit()
            return result
        return None