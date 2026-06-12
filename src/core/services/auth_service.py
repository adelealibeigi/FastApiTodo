from injector import inject
from typing import Optional, Union
from src.core.exceptions.service_exceptions import InvalidCredentialsError, InvalidTokenError, UserNotFoundError, \
    UserAlreadyExistsError
from src.core.service_contract.data_model.token_data_model import TokenDataModel, TokenPayloadDataModel, \
    RefreshTokenDataModel
from src.core.service_contract.data_model.user_data_model import UserDataModel
from src.core.service_contract.interface.iauth_service import IAuthService
from src.core.service_contract.interface.ipassword_hasher import IPasswordHasher
from src.core.service_contract.interface.repository.iuser_repository import IUserRepository
from src.infrastructure.security.jwt_provider import ITokenProvider
from src.infrastructure.models.user_model import UserModel
import logging

logger = logging.getLogger(__name__)


class AuthService(IAuthService):
    @inject
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher,
                 token_provider: ITokenProvider):
        self.__user_repository: IUserRepository = user_repository
        self.__password_hasher: IPasswordHasher = password_hasher
        self.__token_provider: ITokenProvider = token_provider

    def login(self, username: str, password: str) -> TokenDataModel:
        user_model = self.__user_repository.get_model_by_user_name(username=username.lower())
        if user_model is None:
            raise UserNotFoundError()
        if not self.__password_hasher.verify_password(plain_password=password, hashed=user_model.password):
            raise InvalidCredentialsError()

        access_token = self.__token_provider.generate_access_token(user_id=user_model.id)
        refresh_token = self.__token_provider.generate_refresh_token(user_id=user_model.id)
        return TokenDataModel(access_token=access_token, refresh_token=refresh_token)

    def register(self, username: str, password: str, phone_number: Union[str, None], email: str) -> int:

        username = username.lower()
        email = email.lower()
        if self.__user_repository.get_model_by_user_name(username=username):
            raise UserAlreadyExistsError()

        password = self.__password_hasher.hash_password(password)
        user_model = UserModel(username=username, password=password, phone_number=phone_number, email=email)
        user_model = self.__user_repository.add(user_model)
        return user_model.id

    def __get_user_data_model_by_user_id(self, user_id: int) -> UserDataModel:
        user = self.__user_repository.get_model_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundError()
        user_data_model = UserDataModel(id=user.id, username=user.username, phone_number=user.phone_number,
            email=user.email)
        return user_data_model

    def refresh_token(self, token: str) -> RefreshTokenDataModel:
        token_payload: TokenPayloadDataModel = self.__token_provider.decode_refresh_token(token)
        user_id: int = token_payload.user_id
        user: UserDataModel = self.__get_user_data_model_by_user_id(user_id=user_id)

        access_token = self.__token_provider.generate_access_token(user_id=user.id)
        return RefreshTokenDataModel(access_token=access_token)

    def get_current_user_by_access_token(self, token: str) -> UserDataModel:
        token_payload: TokenPayloadDataModel = self.__token_provider.decode_access_token(token)
        user_id: int = token_payload.user_id
        user: UserDataModel = self.__get_user_data_model_by_user_id(user_id=user_id)

        return user
