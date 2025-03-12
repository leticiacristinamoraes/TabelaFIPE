import uuid

from sqlalchemy import select
from db.db_model.permission_sql import PermissionDBModel
from app.entities.permission import Permission
from typing import Optional

class PermissionPostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

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
            id=uuid.UUID(permission_id),
            name=name
        )

        try:
            self.__session.add(permission_db_model)
            self.__session.commit()
            self.__session.refresh(permission_db_model)
        except:
            print("error")

        if permission_db_model is not None:
            return self.__db_to_entity(permission_db_model)
        return None

    def get(self, permission_id: uuid.UUID) -> Optional[Permission]:
        """ Get permission by id
        :param permission_id: permissionId
        :return: Optional[permission]
        """
        result = self.__session.execute(select(PermissionDBModel).where(PermissionDBModel.id == permission_id)).fetchone()[0]
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
        result = self.__session.query(
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
        self.__session.commit()
        return self.__db_to_entity(permission_db_model)