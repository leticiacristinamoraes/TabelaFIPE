import uuid

from sqlalchemy import func, select
from TabelaFIPE.db.db_model.car_sql import CarDBModel
from TabelaFIPE.db.db_model.register_sql import RegisterDBModel
from db.db_model.avg_price_sql import AvgPriceDBModel

from app.entities.avg_price import AvgPrice
from dataclasses import dataclass, asdict
from typing import Optional


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
        """ Update avg price
        :param avg_price: avg_price
        :return: Optional[avg_price]
        """
        avg_price_db_model = AvgPriceDBModel(
            id=avg_price.id,
            car_id=avg_price.car_id,
            avg_price=avg_price.avg_price
        )
        result = self.__session.query(
            AvgPriceDBModel
        ).filter_by(
            id=avg_price.id
        ).update(
            {
                "car_id": avg_price.car_id,
                "avg_price": avg_price.avg_price
            }
        )
        if result == 0:
            return None
        self.__session.commit()
        return self.__db_to_entity(avg_price_db_model)
    
    def calculate_and_store_avg_prices(self):
        """ Calcula a média de preços para cada modelo de carro e armazena no banco """

        '''
            acredito que não precisa desse pedaço 
            pois a consulta pode ser feita pegando o get do avg_price e e depois chamando essa função
        
        '''
        
        query = (
            select(RegisterDBModel.car_id, func.avg(RegisterDBModel.price).label("avg_price"))
            .group_by(RegisterDBModel.car_id)
        )

        result = self.__session.execute(query).fetchall()

        for row in result:
            car_id = row[0]
            avg_price = row[1]

            existing_avg = self.__session.execute(
                select(AvgPriceDBModel).where(AvgPriceDBModel.car_id == car_id)
            ).fetchone()

            if existing_avg:
                self.__session.query(AvgPriceDBModel).filter_by(car_id=car_id).update(
                    {"avg_price": avg_price}
                )
            else:
                avg_price_db_model = AvgPriceDBModel(
                    id=uuid.uuid4(),
                    car_id=car_id,
                    avg_price=str(avg_price)
                )
                self.__session.add(avg_price_db_model)

        self.__session.commit()

    def get_avg_price_by_model(self, brand, model):
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