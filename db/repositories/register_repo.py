import uuid

from sqlalchemy import select
from db.db_model.car_sql import CarDBModel
from db.db_model.register_sql import RegisterDBModel

from app.entities.register import Register
from typing import Optional
import datetime

class RegisterPostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

    def __db_to_entity(
            self, db_row: RegisterDBModel
    ) -> Optional[Register]:
        return Register(
            id=db_row.id,
            car_id=db_row.car_id,
            shop_id=db_row.shop_id,
            price=db_row.price,
            created_date=db_row.created_date
        )

    def create(self, car_id: uuid.UUID, shop_id: uuid.UUID, price:str) -> Optional[Register]:

        register_id = uuid.uuid4()
        register_db_model = RegisterDBModel(
            id=register_id,
            car_id=car_id,
            shop_id=shop_id,
            price=price,
        )

        try:
            self.__session.add(register_db_model)
            self.__session.commit()
            self.__session.refresh(register_db_model)
        except:
            print("error")

        if register_db_model is not None:
            return self.__db_to_entity(register_db_model)
        return None

    def get(self, register_id: uuid.UUID) -> Optional[Register]:
        """ Get register by id
        :param register_id: registerId
        :return: Optional[register]
        """
        result = self.__session.execute(select(RegisterDBModel).where(RegisterDBModel.id == register_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None
    
    def get_prices_by_car(self, car_id):
        """ Consulta todos os preços cadastrados de um carro específico """
        query = select(RegisterDBModel).where(RegisterDBModel.car_id == car_id)
        result = self.__session.execute(query).fetchall()

        if result:
            return [{"id": row[0].id, "price": row[0].price, "date": row[0].created_date} for row in result]
        return []

    def get_prices_by_model(self, brand, model, model_year):
        """ Consulta todos os preços cadastrados de um modelo específico """
        car_query = select(CarDBModel.id).where(
            (CarDBModel.brand == brand) & (CarDBModel.model == model)
        )
        car_result = self.__session.execute(car_query).fetchall()

        if not car_result:
            return []

        car_ids = [row[0] for row in car_result]
        query = select(RegisterDBModel).where(RegisterDBModel.car_id.in_(car_ids))
        result = self.__session.execute(query).fetchall()

        return [{"id": row[0].id, "price": row[0].price, "date": row[0].created_date} for row in result]

    def update(self, register: Register) -> Optional[Register]:
        """ Update register
        :param register: register
        :return: Optional[register]
        """
        register_db_model = RegisterDBModel(
            id=register.id,
            car_id=register.car_id,
            shop_id=register.shop_id,
            price=str(register.price),
            created_date=register.created_date
        )
        result = self.__session.query(
            RegisterDBModel
        ).filter_by(
            id=uuid.UUID(register.id)
        ).update(
            {
                "car_id": uuid.UUID(register.car_id),
                "shop_id": uuid.UUID(register.shop_id),
                "price": str(register.price),
                "created_date": register.created_date
            }
        )
        if result == 0:
            return None
        self.__session.commit()
        return self.__db_to_entity(register_db_model)
    
