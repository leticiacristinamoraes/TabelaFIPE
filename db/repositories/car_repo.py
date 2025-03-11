import uuid
from TabelaFIPE.db.db_model.car_sql import CarDBModel
from db_model.db_base_postgresql import Session
from app.entities.car import Car
from typing import Optional

class CarPostgresqlRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def __db_to_entity(
            self, db_row: CarDBModel
    ) -> Optional[Car]:
        return Car(
            id=db_row.id,
            brand=db_row.brand,
            model=db_row.model,
            model_year=db_row.model_year
        )

    def create(self, brand: str, model: str, model_year: int) -> Optional[Car]:
        """ Create car
        :param brand: str
        :param model: str
        :param model_year: int
        :return: Optional[car]
        """
        car_id = uuid.uuid4()
        car_db_model = CarDBModel(
            id=str(car_id),
            brand=brand,
            model=model,
            model_year=model_year
        )

        try:
            self.session.add(car_db_model)
            self.session.commit()
            self.session.refresh(car_db_model)
        except:
            print("error")

        if car_db_model is not None:
            return self.__db_to_entity(car_db_model)
        return None

    def get(self, car_id: str) -> Optional[Car]:
        """ Get car by id
        :param car_id: carId
        :return: Optional[car]
        """
        result = self.session.query(CarDBModel).get(car_id)
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, car: Car) -> Optional[Car]:
        """ Update car
        :param car: car
        :return: Optional[car]
        """
        car_db_model = CarDBModel(
            id=car.id,
            brand=car.brand,
            model=car.model,
            model_year=car.model_year
        )
        result = self.session.query(
            CarDBModel
        ).filter_by(
            id=car.id
        ).update(
            {
                "brand": car.brand,
                "model": car.model,
                "model_year": car.model_year
            }
        )
        if result == 0:
            return None
        self.session.commit()
        return self.__db_to_entity(car_db_model)