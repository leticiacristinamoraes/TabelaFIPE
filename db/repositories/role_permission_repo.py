import uuid

from sqlalchemy import select
from db.db_model.role_permission_sql import RolePermissionDBModel
from app.entities.role_permission import RolePermission
from dataclasses import dataclass, asdict
from typing import Optional



class RolePermissionPostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

    def __db_to_entity(
            self, db_row: RolePermissionDBModel
    ) -> Optional[RolePermission]:
        return RolePermission(
            id=db_row.id,
            role_id=db_row.role_id,
            permission_id=db_row.permission_id
        )

    def create(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> Optional[RolePermission]:
        """ Create role permission
        :param role_id: str
        :param permission_id: str
        :return: Optional[role_permission]
        """
        role_permission_id = uuid.uuid4()
        role_permission_db_model = RolePermissionDBModel(
            id=role_permission_id,
            role_id=role_id,
            permission_id=permission_id
        )

        try:
            self.__session.add(role_permission_db_model)
            self.__session.commit()
            self.__session.refresh(role_permission_db_model)
        except:
            print("error")

        if role_permission_db_model is not None:
            return self.__db_to_entity(role_permission_db_model)
        return None

    def get(self, role_permission_id: str) -> Optional[RolePermission]:
        """ Get role permission by id
        :param role_permission_id: rolePermissionId
        :return: Optional[role_permission]
        """
        result = self.__session.execute(select(RolePermissionDBModel).where(RolePermissionDBModel.id == role_permission_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def update(self, role_permission: RolePermission) -> Optional[RolePermission]:
        """ Update role permission
        :param role_permission: role_permission
        :return: Optional[role_permission]
        """
        role_permission_db_model = RolePermissionDBModel(
            id=role_permission.id,
            role_id=role_permission.role_id,
            permission_id=role_permission.permission_id
        )
        result = self.__session.query(
            RolePermissionDBModel
        ).filter_by(
            id=role_permission.id
        ).update(
            {
                "role_id": role_permission.role_id,
                "permission_id": role_permission.permission_id
            }
        )
        if result == 0:
            return None
        self.__session.commit()
        return self.__db_to_entity(role_permission_db_model)