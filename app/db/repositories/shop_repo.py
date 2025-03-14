import uuid

from requests import delete
from sqlalchemy import select, update
from db.db_model.shop_sql import ShopDBModel
from dataclasses import dataclass, asdict
from app.entities.shop import Shop
from typing import Optional

# Classe de repositório de shops para realizar CRUD com o banco de dados.
class ShopPostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

    def __db_to_entity(
            self, db_row: ShopDBModel
    ) -> Optional[Shop]:
        return Shop(
            id=db_row.id,
            name=db_row.name
        )

    def create(self, name: str) -> Optional[Shop]:
        """ Create shop
        :param name: str
        :return: Optional[shop]
        """
        shop_id = uuid.uuid4()
        shop_db_model = ShopDBModel(
            id=shop_id,
            name=name
        )

        try:
            self.__session.add(shop_db_model)
            self.__session.commit()
            self.__session.refresh(shop_db_model)
        except:
            print("error")

        if shop_db_model is not None:
            return self.__db_to_entity(shop_db_model)
        return None

    def get(self, shop_id: uuid.UUID) -> Optional[Shop]:
        """ Get shop by id
        :param shop_id: shopId
        :return: Optional[shop]
        """
        result = self.__session.execute(select(ShopDBModel).where(ShopDBModel.id == shop_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def get_shop_by_name(self, shop_name: str) -> Optional[Shop]:
        """ Get shop by name
        :param name: str
        :return: Optional[shop]
        """
        result = self.__session.execute(select(ShopDBModel).where(ShopDBModel.name == shop_name)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, shop: Shop) -> Optional[Shop]:
        """ Update shop
        :param shop: shop
        :return: Optional[shop]
        """
        shop_db_model = ShopDBModel(**asdict(shop))
        self.__session.execute(update(ShopDBModel).where(ShopDBModel.id == shop.id).values(shop_db_model))
        self.__session.commit()
        return shop
    
    def delete_by_name(self, shop_name: str) -> Optional[Shop]:
        """ Delete shop by id
        :param shop_id: shopId
        :return: Optional[shop]
        """
        shop = self.get_shop_by_name(shop_name)
        if shop is not None:
            self.__session.execute(delete(ShopDBModel).where(ShopDBModel.id == shop.id))
            self.__session.commit()
            return shop
        return None
    