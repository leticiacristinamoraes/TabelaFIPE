import logging
import uuid


from sqlalchemy.exc import OperationalError
from db.db_model.user_sql import UserDBModel
from app.entities.user import User
from typing import Optional
from sqlalchemy import select, delete, update

# Classe de repositório de usuários para realizar CRUD com o banco de dados.
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
    
    def get_user_by_email(self, email: str) -> Optional[UserDBModel]:
        """ Get user by email
        :param email: str
        :return: Optional[user]
        """
        result = self.__session.execute(select(UserDBModel).where(UserDBModel.email == email)).fetchone()[0]
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
        user_model = self.get(user.id)
        if user_model is None:
            return None
        self.__session.execute(update(UserDBModel).where(UserDBModel.id==user.id).values(name=user.name)).fetchone()[0]
        self.__session.commit()
        return user_model
    
    def delete_by_email(self, user_email: str) -> Optional[User]:
        """ Delete user
        :param email: str
        :return: Optional[user]
        """
        result = self.get_user_by_email(user_email)
        if result is None:
            return None
        self.__session.execute(delete(UserDBModel).where(UserDBModel.email == user_email))
        self.__session.commit()
        return result
