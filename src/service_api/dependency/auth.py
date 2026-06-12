from fastapi_injector import Injected
from injector import Injector

from src.core.exceptions.service_exceptions import InvalidTokenError, UnauthorizedError
from src.core.service_contract.data_model.user_data_model import UserDataModel
from src.core.service_contract.interface.iauth_service import IAuthService
from src.injection import Injection
from fastapi import Depends, Request
from injector import Injector, inject

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(auto_error=False)


def get_token(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> str:
    if credentials is None:
        raise UnauthorizedError("Missing authorization header")

    if credentials.scheme.lower()!="bearer":
        raise InvalidTokenError("Invalid authentication scheme")

    token: str = credentials.credentials

    if not token:
        raise InvalidTokenError("Token is empty")
    return token


def get_current_user(token: str = Depends(get_token), auth_service: IAuthService = Injected(IAuthService)):
    return auth_service.get_current_user_by_access_token(token=token)
