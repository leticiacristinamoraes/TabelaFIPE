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
            self, db_row: ModelsDBModel
    ) -> Optional[Model]:
        return Model(
            id=db_row.id,
            name=db_row.name,
            brand_id=db_row.brand_id
        )
    
    def create_model(self, brand_id: uuid.UUID, name:str):
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
            return self.__db_to_entity(model_db_model)
        return None
    
    def get_all_models(self, brand_id: uuid.UUID) -> Optional[Model]:
        try:
            result = self.__session.execute(select(ModelsDBModel).where(ModelsDBModel.brand_id == brand_id)).fetchall()
            if result is not None:
                return [self.__db_to_entity(model[0]) for model in result]
        except OperationalError as err:
            logging.error("get all %s", err)
    
    
    
    
