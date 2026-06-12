from abc import ABC, abstractmethod

from src.core.service_contract.data_model.token_data_model import TokenPayloadDataModel


class ITokenProvider(ABC):
    @staticmethod
    @abstractmethod
    def generate_access_token(user_id: int, expires_in: int = 50 * 5) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_refresh_token(user_id: int, expires_in: int = 3600 * 24) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def decode_access_token(token: str) -> TokenPayloadDataModel:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def decode_refresh_token(token: str) -> TokenPayloadDataModel:
        raise NotImplementedError
