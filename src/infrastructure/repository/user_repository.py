from typing import Union

from injector import inject

from src.core.service_contract.interface.repository.iuser_repository import IUserRepository
from src.infrastructure.database.ipostgresql_connection import IPostgreSQLConnection
from src.infrastructure.models import UserModel


class UserRepository(IUserRepository):
    @inject
    def __init__(self, database_connection: IPostgreSQLConnection) -> None:
        self.__database_connection: IPostgreSQLConnection = database_connection

    def add(self, model) -> UserModel:
        with self.__database_connection.get_session() as session:
            session.add(model)
            session.commit()
            return model

    def get_model_by_user_name(self, username: str) -> Union[UserModel, None]:
        with self.__database_connection.get_session() as session:
            return session.query(UserModel).filter(UserModel.username==username).one_or_none()

    def get_model_by_id(self, user_id:int)->Union[UserModel, None]:
        with self.__database_connection.get_session() as session:
            return session.query(UserModel).filter(UserModel.id == user_id).one_or_none()
