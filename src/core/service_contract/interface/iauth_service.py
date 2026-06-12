from abc import ABC, abstractmethod
from typing import Union

from src.core.service_contract.data_model.token_data_model import TokenDataModel, RefreshTokenDataModel
from src.core.service_contract.data_model.user_data_model import UserDataModel


class IAuthService(ABC):
    @abstractmethod
    def login(self, username: str, password: str) -> TokenDataModel:
        raise NotImplementedError

    @abstractmethod
    def register(self, username: str, password: str, phone_number: Union[str, None], email: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def refresh_token(self, token: str) -> RefreshTokenDataModel:
        raise NotImplementedError

    @abstractmethod
    def get_current_user_by_access_token(self, token: str) -> UserDataModel:
        raise NotImplementedError
