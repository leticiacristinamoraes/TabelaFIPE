import uuid

from sqlalchemy import func, select, update, delete
from db.db_model.car_sql import CarDBModel
from db.db_model.register_sql import RegisterDBModel
from db.db_model.avg_price_sql import AvgPriceDBModel
from entities.avg_price import AvgPrice
from dataclasses import dataclass, asdict
from typing import Optional

# Classe de repositório de medias de preços por carro para realizar CRUD com o banco de dados.
class AvgPricePostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

    def __db_to_entity(
            self, db_row: AvgPriceDBModel
    ) -> Optional[AvgPrice]:
        return AvgPrice(
            id=db_row.id,
            car_id=db_row.car_id,
            avg_price=db_row.avg_price
        )

    def create(self, car_id: uuid.UUID, avg_price: str) -> Optional[AvgPrice]:
        """ Create avg price
        :param car_id: str
        :param avg_price: str
        :return: Optional[avg_price]
        """
        avg_price_id = uuid.uuid4()
        avg_price_db_model = AvgPriceDBModel(
            id=avg_price_id,
            car_id=car_id,
            avg_price=avg_price
        )

        try:
            self.__session.add(avg_price_db_model)
            self.__session.commit()
            self.__session.refresh(avg_price_db_model)
        except:
            print("error")

        if avg_price_db_model is not None:
            return self.__db_to_entity(avg_price_db_model)
        return None

    def get(self, avg_price_id: uuid.UUID) -> Optional[AvgPrice]:
        """ Get avg price by id
        :param avg_price_id: avgPriceId
        :return: Optional[avg_price]
        """
        result = self.__session.execute(select(AvgPriceDBModel).where(AvgPriceDBModel.id ==avg_price_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, avg_price: AvgPrice) -> Optional[AvgPrice]:
        """ Update avg price by id
        :param avg_price_id: avgPriceId
        :param avg_price: str
        :return: Optional[avg_price]
        """
        result = self.__session.execute(
            update(AvgPriceDBModel).where(AvgPriceDBModel.id == avg_price.id).values(AvgPriceDBModel.avg_price==avg_price.avg_price)
        )
    
        if result is not None:
            self.__session.commit()
            return avg_price
        return None
    
    def store_avg_prices(self, car_id, new_avg_price):

        existing_avg = self.get_avg_price_by_car_id(car_id)

        if existing_avg:
            result = self.update(AvgPrice(id=existing_avg.id, car_id= car_id, avg_price=new_avg_price))
        else:
            result = self.create(car_id, new_avg_price)

        self.__session.commit()
        if result is not None:
            self.__session.commit()
            return result
        return None
        
    def get_avg_price_by_car_id(self, car_id: uuid.UUID):
        try:
            result = self.__session.execute(select(AvgPriceDBModel).where(AvgPriceDBModel.car_id ==car_id)).fetchone()[0]
        
            if result is not None:
                return self.__db_to_entity(result)
        except:
            return None

    def get_avg_price_by_brand(self, brand, model):
        """ Retorna a média de preços de um modelo específico """
        '''acredito que a mesma coisa dessa! podemos colocar em outro lugar'''

        car_query = select(CarDBModel.id).where(
            (CarDBModel.brand == brand) & (CarDBModel.model == model)
        )
        car_result = self.__session.execute(car_query).fetchall()

        if not car_result:
            return None

        car_ids = [row[0] for row in car_result]
        query = select(func.avg(RegisterDBModel.price)).where(RegisterDBModel.car_id.in_(car_ids))
        result = self.__session.execute(query).scalar()

        return result if result else None