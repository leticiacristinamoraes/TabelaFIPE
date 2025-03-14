import uuid

from sqlalchemy import select, delete, update
from db.db_model.permission_sql import PermissionDBModel
from app.entities.permission import Permission
from typing import Optional

# Classe de repositório de permissões para realizar CRUD com o banco de dados.
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
            id=permission_id,
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

    def get_permission_by_name(self, name: str) -> Optional[Permission]:
        """ Get permission by name
        :param name: str
        :return: Optional[permission]
        """
        result = self.__session.execute(select(PermissionDBModel).where(PermissionDBModel.name == name)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        
    def update(self, permission: Permission) -> Optional[Permission]:
        """ Update permission
        :param permission: Permission
        :return: Optional[permission]
        """
        permission_db_model = self.get(permission.id)
        if permission_db_model is not None:
            self.__session.execute(update(PermissionDBModel).where(PermissionDBModel.id==permission.id).values(name=permission.name))
            self.__session.commit()
            return self.__db_to_entity(permission_db_model)
        return None
    
    def delete(self, permission_name: str) -> Optional[Permission]:
        """ Delete permission by id
        :param permission_id: permissionId
        :return: Optional[permission]
        """
        permission_model = self.get_permission_by_name(permission_name)
        if permission_model is not None:
            self.__session.execute(delete(PermissionDBModel).where(PermissionDBModel.id == permission_model.id))
            self.__session.commit()
            return self.__db_to_entity(permission_model)
        return None