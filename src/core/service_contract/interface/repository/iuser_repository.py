from abc import ABC, abstractmethod
from typing import Union

from src.infrastructure.models.user_model import UserModel


class IUserRepository(ABC):

    @abstractmethod
    def add(self, model) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    def get_model_by_user_name(self, username: str) -> Union[UserModel, None]:
        raise NotImplementedError

    @abstractmethod
    def get_model_by_id(self, user_id:int)->Union[UserModel, None]:
        raise NotImplementedError
