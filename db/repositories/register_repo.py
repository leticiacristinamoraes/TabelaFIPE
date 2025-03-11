import uuid
from TabelaFIPE.db.db_model.register_sql import RegisterDBModel
from db_model.db_base_postgresql import Session
from app.entities.register import Register
from typing import Optional
import datetime

class RegisterPostgresqlRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def __db_to_entity(
            self, db_row: RegisterDBModel
    ) -> Optional[Register]:
        return Register(
            id=str(db_row.id),
            car_id=str(db_row.car_id),
            shop_id=str(db_row.shop_id),
            price=str(db_row.price),
            created_date=db_row.created_date
        )

    def create(self, car_id: str, shop_id: str, price:str, created_date: datetime.datetime) -> Optional[Register]:

        register_id = uuid.uuid4()
        register_db_model = RegisterDBModel(
            id=register_id,
            car_id=uuid.UUID(car_id),
            shop_id=uuid.UUID(shop_id),
            price=price,
            created_date=created_date
        )

        try:
            self.session.add(register_db_model)
            self.session.commit()
            self.session.refresh(register_db_model)
        except:
            print("error")

        if register_db_model is not None:
            return self.__db_to_entity(register_db_model)
        return None

    def get(self, register_id: str) -> Optional[Register]:
        """ Get register by id
        :param register_id: registerId
        :return: Optional[register]
        """
        result = self.session.query(RegisterDBModel).get(uuid.UUID(register_id))
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, register: Register) -> Optional[Register]:
        """ Update register
        :param register: register
        :return: Optional[register]
        """
        register_db_model = RegisterDBModel(
            id=uuid.UUID(register.id),
            car_id=uuid.UUID(register.car_id),
            shop_id=uuid.UUID(register.shop_id),
            price=str(register.price),
            created_date=register.created_date
        )
        result = self.session.query(
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
        self.session.commit()
        return self.__db_to_entity(register_db_model)