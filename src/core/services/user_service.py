from typing import Union

from injector import inject

from src.core.exceptions.service_exceptions import UserNotFoundError
from src.core.service_contract.data_model.user_data_model import UserDataModel
from src.core.service_contract.interface.iuser_service import IUserService
from src.core.service_contract.interface.repository.iuser_repository import IUserRepository
from src.infrastructure.models.user_model import UserModel

import logging

logger = logging.getLogger(__name__)


class UserService(IUserService):

    @inject
    def __init__(self, repository: IUserRepository):
        self.__repository: IUserRepository = repository

    def find(self, username: str) -> UserDataModel:
        if model := self.__repository.get_model_by_user_name(username=username):
            return self.__make_user_data_model(model)
        raise UserNotFoundError()

    @staticmethod
    def __make_user_data_model(model: UserModel) -> UserDataModel:
        return UserDataModel(id=model.id, username=model.username, phone_number=model.phone_number, email=model.email)
