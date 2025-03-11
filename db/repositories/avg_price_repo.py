import uuid
from TabelaFIPE.db.db_model.avg_price_sql import AvgPriceDBModel
from db_model.db_base_postgresql import Session
from app.entities.avg_price import AvgPrice
from dataclasses import dataclass, asdict
from typing import Optional


class AvgPricePostgresqlRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def __db_to_entity(
            self, db_row: AvgPriceDBModel
    ) -> Optional[AvgPrice]:
        return AvgPrice(
            id=db_row.id,
            car_id=db_row.car_id,
            avg_price=db_row.avg_price
        )

    def create(self, car_id: str, avg_price: str) -> Optional[AvgPrice]:
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
            self.session.add(avg_price_db_model)
            self.session.commit()
            self.session.refresh(avg_price_db_model)
        except:
            print("error")

        if avg_price_db_model is not None:
            return self.__db_to_entity(avg_price_db_model)
        return None

    def get(self, avg_price_id: str) -> Optional[AvgPrice]:
        """ Get avg price by id
        :param avg_price_id: avgPriceId
        :return: Optional[avg_price]
        """
        result = self.session.query(AvgPriceDBModel).get(avg_price_id)
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
        result = self.session.query(
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
        self.session.commit()
        return self.__db_to_entity(avg_price_db_model)