import logging
import uuid

from psycopg import OperationalError
from sqlalchemy import select, update, delete
from db.db_model.car_sql import CarDBModel
from db.db_model.brand_sql import BrandDBModel
from db.db_model.model_sql import ModelsDBModel
from entities.car import Car, Model, Brand
from typing import Optional

class BrandPostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

    def __db_to_entity(
            self, db_row: BrandDBModel
    ) -> Optional[Brand]:
        return Brand(
            id=db_row.id,
            name = db_row.name
        )
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
    
    def get_all_brands(self) -> Optional[Brand]:
        try:
            result = self.__session.execute(select(BrandDBModel)).fetchall()
            if result is not None:
                return [self.__db_to_entity(brand[0]) for brand in result]
        except OperationalError as err:
            logging.error("get all %s", err)
    
    
    def get_brand_id_by_name(self, brand_name:str):
        result = self.__session.execute(select(BrandDBModel).where(BrandDBModel.name == brand_name)).fetchone()[0]
      
        if result is not None:
            return self.__db_to_entity(result).id
        return None
    
    