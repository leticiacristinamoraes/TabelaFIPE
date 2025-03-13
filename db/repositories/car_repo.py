import uuid

from sqlalchemy import select, update, delete
from db.db_model.car_sql import CarDBModel
from app.entities.car import Car
from typing import Optional

# Classe de repositório de cars para realizar CRUD com o banco de dados.
class CarPostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

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
            id=car_id,
            brand=brand,
            model=model,
            model_year=model_year
        )

        try:
            self.__session.add(car_db_model)
            self.__session.commit()
            self.__session.refresh(car_db_model)
        except:
            print("error")

        if car_db_model is not None:
            return self.__db_to_entity(car_db_model)
        return None

    def get(self, car_id: uuid.UUID) -> Optional[Car]:
        """ Get car by id
        :param car_id: carId
        :return: Optional[car]
        """
        result = self.__session.execute(select(CarDBModel).where(CarDBModel.id == car_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def get_car_by_fields(self, brand: str, model: str, model_year: int) -> Optional[Car]:
        """ Get car by brand, model and model_year
        :param brand: str
        :param model: str
        :param model_year: int
        :return: Optional[car]
        """
        result = self.__session.execute(select(CarDBModel).where(CarDBModel.brand == brand, CarDBModel.model == model, CarDBModel.model_year == model_year)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None


    def update(self, car: Car) -> Optional[Car]:
        """ Update car
        :param car: car
        :return: Optional[car]
        """ 
        car_db_model = self.__session.execute(update(CarDBModel).where(CarDBModel.id==car.id).values(brand=car.brand, model=car.model, model_year=car.model_year)).fetchone()[0]
        if car_db_model is None:
            return None
        self.__session.commit()
        return self.__db_to_entity(car_db_model)
    
    def delete(self, car_id: uuid.UUID) -> Optional[Car]:
        """ Delete car
        :param car_id: carId
        :return: Optional[car]
        """ 
        car = self.get(car_id)
        if car is not None:
            self.__session.execute(delete(CarDBModel).where(CarDBModel.id == car.id))
            self.__session.commit()
            return car
        return None