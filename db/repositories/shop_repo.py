import uuid
from TabelaFIPE.db.db_model.shop_sql import ShopDBModel
from db_model.db_base_postgresql import Session
from dataclasses import dataclass, asdict
from app.entities.shop import Shop
from typing import Optional

@dataclass
class Shop:
    id: str
    name: str

class ShopPostgresqlRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def __db_to_entity(
            self, db_row: ShopDBModel
    ) -> Optional[Shop]:
        return Shop(
            id=str(db_row.id),
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
            self.session.add(shop_db_model)
            self.session.commit()
            self.session.refresh(shop_db_model)
        except:
            print("error")

        if shop_db_model is not None:
            return self.__db_to_entity(shop_db_model)
        return None

    def get(self, shop_id: str) -> Optional[Shop]:
        """ Get shop by id
        :param shop_id: shopId
        :return: Optional[shop]
        """
        result = self.session.query(ShopDBModel).get(uuid.UUID(shop_id))
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, shop: Shop) -> Optional[Shop]:
        """ Update shop
        :param shop: shop
        :return: Optional[shop]
        """
        shop_db_model = ShopDBModel(
            id=uuid.UUID(shop.id),
            name=shop.name
        )
        result = self.session.query(
            ShopDBModel
        ).filter_by(
            id=uuid.UUID(shop.id)
        ).update(
            {
                "name": shop.name
            }
        )
        if result == 0:
            return None
        self.session.commit()
        return self.__db_to_entity(shop_db_model)