import logging
import uuid

from psycopg import OperationalError
from sqlalchemy import select, update, delete
from db.db_model.car_sql import CarDBModel
from db.db_model.brand_sql import BrandDBModel
from db.db_model.model_sql import ModelsDBModel
from entities.car import Car, Model, Brand
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
            model_id=db_row.model_id,
            model_year=db_row.model_year
        )

    def create_car(self, model: uuid.UUID, model_year: int):
        car_id = uuid.uuid4()
        car_db_model = CarDBModel(
            id=car_id,
            model_id=model,
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
            model_id=model,
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
    
    def get_cars_years(self, model_id:uuid.UUID):
        result = self.__session.execute(select(CarDBModel).where(CarDBModel.model_id == model_id)).fetchall()
        print(result)
        if result is not None:
            return [self.__db_to_entity(cars[0]).model_year for  cars in result]
        return None
    
    def get_car_by_fields(self, model_id: uuid.UUID, model_year: int) -> Optional[Car]:
        """ Get car by brand, model and model_year
        :param brand: str
        :param model: str
        :param model_year: int
        :return: Optional[car]
        """
        result = self.__session.execute(select(CarDBModel).where(CarDBModel.model_id == model_id, CarDBModel.model_year == model_year)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def get_all(self) -> Optional[CarDBModel]:
        """ Get user by id
        :param user_id: userId
        :return: Optional[user]
        """
        try:
            result = self.__session.execute(select(CarDBModel)).fetchall()
            if result is not None:
                return [self.__db_to_entity(car[0]) for car in result]
        except OperationalError as err:
            logging.error("get all %s", err)

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