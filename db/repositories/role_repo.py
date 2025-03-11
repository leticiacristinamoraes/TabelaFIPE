import uuid
from TabelaFIPE.db.db_model.role_sql import RoleDBModel
from db_model.db_base_postgresql import Session
from app.entities.role import Role
from typing import Optional

class RolePostgresqlRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

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
            self.session.add(role_db_model)
            self.session.commit()
            self.session.refresh(role_db_model)
        except:
            print("error")

        if role_db_model is not None:
            return self.__db_to_entity(role_db_model)
        return None

    def get(self, role_id: str) -> Optional[Role]:
        """ Get role by id
        :param role_id: roleId
        :return: Optional[role]
        """
        result = self.session.query(RoleDBModel).get(uuid.UUID(role_id))
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
        result = self.session.query(
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
        self.session.commit()
        return self.__db_to_entity(role_db_model)