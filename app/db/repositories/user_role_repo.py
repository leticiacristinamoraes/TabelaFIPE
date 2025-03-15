import uuid

from sqlalchemy import delete, select, text, update
from db.db_model.user_role_sql import UserRoleDBModel
from app.entities.user_role import UserRole
from dataclasses import dataclass, asdict
from typing import Optional


# Classe de repositório de usuários e roles para realizar CRUD com o banco de dados.
class UserRolePostgresqlRepository():
    def __init__(self, session) -> None:
        self.__session = session

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
            self.__session.add(user_role_db_model)
            self.__session.commit()
            self.__session.refresh(user_role_db_model)
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
        result = self.__session.execute(select(UserRoleDBModel).where(UserRoleDBModel.id == user_role_id)).fetchone()[0]
        if result is not None:
            return self.__db_to_entity(result)
        return None

    def get_all(self) -> Optional[UserRole]:
        """ Get all users
        :return: Optional[user_role]
        """
        result = self.__session.execute(select(UserRoleDBModel)).fetchall()
        if result is not None:
            return [self.__db_to_entity(user_role) for user_role in result]
        return None
    
    def get_users_by_role_id(self, role_id: uuid.UUID) -> Optional[UserRole]:
        """ Get all users by role id
        :return: Optional[user_role]
        """
        result = self.__session.execute(select(UserRoleDBModel).where(UserRoleDBModel.role_id == role_id)).fetchall()
        if result is not None:
            return [self.__db_to_entity(user_role) for user_role in result]
        return None
    
    def get_roles_by_user_id(self, user_id: uuid.UUID) -> Optional[UserRole]:
        """ Get all roles by user id
        :return: Optional[user_role]
        """
        result = self.__session.execute(select(UserRoleDBModel).where(UserRoleDBModel.user_id == user_id)).fetchall()
        if result is not None:
            return [self.__db_to_entity(user_role) for user_role in result]
        return None
    
    def get_user_role_by_ids(self, user_id: uuid.UUID, role_id: uuid.UUID) -> Optional[UserRole]:
        """ Get user role by user_id and role_id
        :param user_id: str
        :param role_id: str
        :return: Optional[user_role]
        """

        result = self.__session.execute(select(UserRoleDBModel).where(UserRoleDBModel.user_id == user_id, UserRoleDBModel.role_id == role_id)).fetchone()
        print(result)
        if result is not None:
            return True

        return False
    

    def delete_by_ids(self, user_id: uuid.UUID, role_id: uuid.UUID) -> Optional[UserRole]:
        """ Delete role permission by id
        :param user_role_id: userRoleId
        """
        result =self.__get_user_role_by_ids(user_id, role_id)
        if result is not None:
            self.__session.execute(delete(UserRoleDBModel).where(UserRoleDBModel.id == result.id))
            self.__session.commit()
            return result
        return None
    
    def inner_join(self, user_id:uuid.UUID):
        
        query = (text('''
        SELECT "Users".email, "Roles".name AS "role", "Permissions".name AS "permissions" FROM "Users" 
                      INNER JOIN "Users_roles" ON "Users".id=:user_id
                      INNER JOIN "Roles" ON "Users_roles".role_id="Roles".id INNER JOIN "Roles_permissions" ON "Roles".id="Roles_permissions".role_id 
                      INNER JOIN "Permissions" ON "Roles_permissions".permission_id="Permissions".id'''))
        
        result = self.__session.execute(query, {'user_id':user_id}).fetchone()
        
        print(result)
        if result is not None:
            return result
        return None
