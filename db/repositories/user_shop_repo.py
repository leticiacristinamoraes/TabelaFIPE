import uuid

from sqlalchemy import select
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

    def update(self, user_shop: UserShop) -> Optional[UserShop]:
        """ Update user role
        :param user_shop: user_shop
        :return: Optional[user_shop]
        """
        user_shop_db_model = UserShopDBModel(
            id=user_shop.id,
            user_id=user_shop.user_id,
            shop_id=user_shop.shop_id
        )
        result = self.__session.query(
            UserShopDBModel
        ).filter_by(
            id=user_shop.id
        ).update(
            {
                "user_id": user_shop.user_id,
                "shop_id": user_shop.shop_id
            }
        )
        if result == 0:
            return None
        self.__session.commit()
        return self.__db_to_entity(user_shop_db_model)