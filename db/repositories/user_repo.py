import logging
import uuid

from sqlalchemy.exc import OperationalError
from db.db_model.user_sql import UserDBModel
from app.entities.user import User
from typing import Optional
from sqlalchemy import select, UUID

class UserPostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

    def __db_to_entity(
            self, db_row: UserDBModel
    ) -> Optional[User]:
        return User(
            id=db_row.id,
            name=db_row.name,
            email=db_row.email
        )

    def create(self, name: str, email: str) -> Optional[User]:
        """ Create user
        :param name: str
        :param email: str
        :return: Optional[user]
        """
        user_id = uuid.uuid4()
        user_db_model = UserDBModel(
            id=user_id,
            name=name,
            email=email
        )
        print(user_db_model)
        try:
            self.__session.add(user_db_model)
            self.__session.commit()
            self.__session.refresh(user_db_model)
        except OperationalError as err:
            logging.error("create %s", err)

        if user_db_model is not None:
            return self.__db_to_entity(user_db_model)
        return None

    def get(self, user_id: uuid.UUID) -> Optional[UserDBModel]:
        """ Get user by id
        :param user_id: userId
        :return: Optional[user]
        """
        result = self.__session.execute(select(UserDBModel).where(UserDBModel.id == user_id)).fetchone()[0]
        print(result)
        if result is not None:
            return self.__db_to_entity(result)
        return None
    def get_all(self) -> Optional[UserDBModel]:
        """ Get user by id
        :param user_id: userId
        :return: Optional[user]
        """
        try:
            result = self.__session.execute(select(UserDBModel))
            for row in result:
                print(self.__db_to_entity(row))
            if result is not None:
                return result
        except OperationalError as err:
            logging.error("get all %s", err)
    def update(self, user: User) -> Optional[User]:
        """ Update user
        :param user: user
        :return: Optional[user]
        """
        user_db_model = UserDBModel(
            user_id=user.user_id,
            name=user.name,
            email=user.email
        )
        result = self.__session.query(
            UserDBModel
        ).filter_by(
            user_id=user.user_id
        ).update(
            {
                "name": user.name,
                "email": user.email
            }
        )
        if result == 0:
            return None
        self.__session.commit()
        return self.__db_to_entity(user_db_model)