import uuid

from sqlalchemy import select, delete
from db.db_model.role_permission_sql import RolePermissionDBModel
from app.entities.role_permission import RolePermission
from dataclasses import dataclass, asdict
from typing import Optional


# Classe de repositório de roles e permissions para realizar CRUD com o banco de dados.
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

    def get(self, role_permission_id: uuid.UUID) -> Optional[RolePermission]:
        """ Get role permission by id
        :param role_permission_id: rolePermissionId
        :return: Optional[role_permission]
        """
        result = self.__session.execute(select(RolePermissionDBModel).where(RolePermissionDBModel.id == role_permission_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def get_all(self) -> Optional[RolePermission]:
        """ Get all roles
        :return: Optional[role_permission]
        """
        result = self.__session.execute(select(RolePermissionDBModel)).fetchall()
        if result is not None:
            return [self.__db_to_entity(i) for i in result]
        return None
    
    def get_all_permissions_by_role_id(self, role_id: uuid.UUID) -> Optional[RolePermission]:
        """ Get all permissions by role_id
        :param role_id: str
        :return: Optional[role_permission]
        """
        result = self.__session.execute(select(RolePermissionDBModel).where(RolePermissionDBModel.role_id == role_id)).fetchall()
        if result is not None:
            return [self.__db_to_entity(role_permission) for role_permission in result]
        return None
    
    def get_all_roles_by_permission_id(self, permission_id: uuid.UUID) -> Optional[RolePermission]:
        """ Get all roles by permission_id
        :param permission_id: str
        :return: Optional[role_permission]
        """
        result = self.__session.execute(select(RolePermissionDBModel).where(RolePermissionDBModel.permission_id == permission_id)).fetchall()
        if result is not None:
            return [self.__db_to_entity(role_permission) for role_permission in result]
        return None
    

    def __get_role_permission_by_ids(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> Optional[RolePermission]:
        """ Get role permission by role_id and permission_id
        :param role_id: str
        :param permission_id: str
        :return: Optional[role_permission]
        """
        result = self.__session.execute(select(RolePermissionDBModel).where(RolePermissionDBModel.role_id == role_id).where(RolePermissionDBModel.permission_id == permission_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None
    
    def delete_by_ids(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> Optional[RolePermission]:
        """ Delete role permission by id
        :param role_permission_id: rolePermissionId
        :return: Optional[role_permission]
        """
        result =self.__get_role_permission_by_ids(role_id, permission_id)
        if result is not None:
            self.__session.execute(delete(RolePermissionDBModel).where(RolePermissionDBModel.id == result.id))
            self.__session.commit()
            return result
        return None