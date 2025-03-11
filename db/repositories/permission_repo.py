import uuid
from TabelaFIPE.db.db_model.permission_sql import PermissionDBModel
from db_model.db_base_postgresql import Session
from app.entities.permission import Permission
from typing import Optional

class PermissionPostgresqlRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def __db_to_entity(
            self, db_row: PermissionDBModel
    ) -> Optional[Permission]:
        return Permission(
            id=db_row.id,
            name=db_row.name
        )

    def create(self, name: str) -> Optional[Permission]:
        """ Create permission
        :param name: str
        :return: Optional[permission]
        """
        permission_id = uuid.uuid4()
        permission_db_model = PermissionDBModel(
            id=str(permission_id),
            name=name
        )

        try:
            self.session.add(permission_db_model)
            self.session.commit()
            self.session.refresh(permission_db_model)
        except:
            print("error")

        if permission_db_model is not None:
            return self.__db_to_entity(permission_db_model)
        return None

    def get(self, permission_id: str) -> Optional[Permission]:
        """ Get permission by id
        :param permission_id: permissionId
        :return: Optional[permission]
        """
        result = self.session.query(PermissionDBModel).get(permission_id)
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, permission: Permission) -> Optional[Permission]:
        """ Update permission
        :param permission: permission
        :return: Optional[permission]
        """
        permission_db_model = PermissionDBModel(
            id=permission.id,
            name=permission.name
        )
        result = self.session.query(
            PermissionDBModel
        ).filter_by(
            id=permission.id
        ).update(
            {
                "name": permission.name
            }
        )
        if result == 0:
            return None
        self.session.commit()
        return self.__db_to_entity(permission_db_model)