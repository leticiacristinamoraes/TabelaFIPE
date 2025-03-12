import uuid

from sqlalchemy import select
from db.db_model.role_sql import RoleDBModel
from app.entities.role import Role
from typing import Optional

class RolePostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

    def __db_to_entity(
            self, db_row: RoleDBModel
    ) -> Optional[Role]:
        return Role(
            id=db_row.id,
            name=db_row.name
        )

    def create(self, name: str) -> Optional[Role]:
        """ Create role
        :param name: str
        :return: Optional[role]
        """
        role_id = uuid.uuid4()
        role_db_model = RoleDBModel(
            id=role_id,
            name=name
        )

        try:
            self.__session.add(role_db_model)
            self.__session.commit()
            self.__session.refresh(role_db_model)
        except:
            print("error")

        if role_db_model is not None:
            return self.__db_to_entity(role_db_model)
        return None

    def get(self, role_id: uuid.UUID) -> Optional[Role]:
        """ Get role by id
        :param role_id: roleId
        :return: Optional[role]
        """
        result = self.__session.execute(select(RoleDBModel).where(RoleDBModel.id == role_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, role: Role) -> Optional[Role]:
        """ Update role
        :param role: role
        :return: Optional[role]
        """
        role_db_model = RoleDBModel(
            id=uuid.UUID(role.id),
            name=role.name
        )
        result = self.__session.query(
            RoleDBModel
        ).filter_by(
            id=uuid.UUID(role.id)
        ).update(
            {
                "name": role.name
            }
        )
        if result == 0:
            return None
        self.__session.commit()
        return self.__db_to_entity(role_db_model)