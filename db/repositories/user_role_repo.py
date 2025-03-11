import uuid
from TabelaFIPE.db.db_model.user_role_sql import UserRoleDBModel
from app.entities.user_role import UserRole
from db_model.db_base_postgresql import Session
from dataclasses import dataclass, asdict
from typing import Optional


class UserRolePostgresqlRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def __db_to_entity(
            self, db_row: UserRoleDBModel
    ) -> Optional[UserRole]:
        return UserRole(
            id=db_row.id,
            user_id=db_row.user_id,
            role_id=db_row.role_id
        )

    def create(self, user_id: uuid.UUID, role_id: uuid.UUID) -> Optional[UserRole]:
        """ Create user role
        :param user_id: str
        :param role_id: str
        :return: Optional[user_role]
        """
        user_role_id = uuid.uuid4()
        user_role_db_model = UserRoleDBModel(
            id=user_role_id,
            user_id=user_id,
            role_id=role_id
        )

        try:
            self.session.add(user_role_db_model)
            self.session.commit()
            self.session.refresh(user_role_db_model)
        except:
            print("error")

        if user_role_db_model is not None:
            return self.__db_to_entity(user_role_db_model)
        return None

    def get(self, user_role_id: uuid.UUID) -> Optional[UserRole]:
        """ Get user role by id
        :param user_role_id: userRoleId
        :return: Optional[user_role]
        """
        result = self.session.query(UserRoleDBModel).get(uuid.UUID(user_role_id))
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, user_role: UserRole) -> Optional[UserRole]:
        """ Update user role
        :param user_role: user_role
        :return: Optional[user_role]
        """
        user_role_db_model = UserRoleDBModel(
            id=user_role.id,
            user_id=user_role.user_id,
            role_id=user_role.role_id
        )
        result = self.session.query(
            UserRoleDBModel
        ).filter_by(
            id=user_role.id
        ).update(
            {
                "user_id": user_role.user_id,
                "role_id": user_role.role_id
            }
        )
        if result == 0:
            return None
        self.session.commit()
        return self.__db_to_entity(user_role_db_model)