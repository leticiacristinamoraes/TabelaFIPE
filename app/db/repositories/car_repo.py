import logging
import uuid

from psycopg import OperationalError
from sqlalchemy import select, update, delete
from db.db_model.car_sql import CarDBModel, ModelsDBModel, BrandDBModel
from app.entities.car import Car, Model, Brand
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
            model_id=db_row.model,
            model_year=db_row.model_year
        )
    def __db_to_entity_models(
            self, db_row: ModelsDBModel
    ) -> Optional[Model]:
        return Model(
            id=db_row.id,
            name=db_row.name,
            model_id=db_row.model_id
        )
    def __db_to_entity_brand(
            self, db_row: BrandDBModel
    ) -> Optional[Brand]:
        return Brand(
            id=db_row.id,
            brand = db_row.name
        )
    def create_car(self, model: uuid.UUID, model_year: str):
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
    def create_model(self, brand_id: int, name:str):
        model_id = uuid.uuid4()
        model_db_model = ModelsDBModel(
            id=model_id,
            name = name,
            brand_id = brand_id
            
        )

        try:
            self.__session.add(model_db_model)
            self.__session.commit()
            self.__session.refresh(model_db_model)
        except:
            print("error")

        if model_db_model is not None:
            return self.__db_to_entity_models(model_db_model)
        return None
    def create_brand(self, name: str):
        brand_id = uuid.uuid4()
        brand_db_model = BrandDBModel(
            id= brand_id,
            name = name
        )
        try:
            self.__session.add(brand_db_model)
            self.__session.commit()
            self.__session.refresh(brand_db_model)
        except:
            print("error")

        if brand_db_model is not None:
            return self.__db_to_entity_brand(brand_db_model)

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
    def get_all_models(self, brand_id: int):
        try:
            result = self.__session.execute(select(ModelsDBModel).where(ModelsDBModel.brand_id == brand_id)).fetchall()
            if result is not None:
                return [self.__db_to_entity_brand_model(model[0]) for model in result]
        except OperationalError as err:
            logging.error("get all %s", err)
    def get_all_brands(self):
        try:
            result = self.__session.execute(select(BrandDBModel)).fetchall()
            if result is not None:
                return [self.__db_to_entity_brand(brand[0]) for brand in result]
        except OperationalError as err:
            logging.error("get all %s", err)
    def get_brand_id_by_name(self, brand_name:str):
        result = self.__session.execute(select(BrandDBModel).where(BrandDBModel.name == brand_name)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result).id
        return None
    def get_cars_years(self, model_id:uuid.UUID):
        try:
            result = self.__session.execute(select(CarDBModel)).fetchall()
            if result is not None:
                return [self.__db_to_entity(cars[0]).model_year for  cars in result]
        except OperationalError as err:
            logging.error("get all %s", err)
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