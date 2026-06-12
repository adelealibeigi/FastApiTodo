from fastapi import APIRouter
from fastapi_injector import Injected
from starlette import status

from src.core.service_contract.data_model.token_data_model import TokenDataModel, RefreshTokenDataModel
from src.core.service_contract.interface.iauth_service import IAuthService
from src.service_api.schemas.auth_schema import LoginSchemaRequest, RegisterSchemaRequest, RegisterSchemaResponse, \
    LoginSchemaResponse, RefreshTokenSchemaRequest, RefreshTokenSchemaResponse

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginSchemaResponse)
def user_login(request: LoginSchemaRequest, auth_service: IAuthService = Injected(IAuthService)):
    token: TokenDataModel = auth_service.login(username=request.username, password=request.password)
    return token


@auth_router.post("/register", status_code=status.HTTP_200_OK, response_model=RegisterSchemaResponse)
def user_register(request: RegisterSchemaRequest, auth_service: IAuthService = Injected(IAuthService)):
    user_id: int = auth_service.register(username=request.username, password=request.password,
        email=request.email, phone_number=request.phone_number)

    return {"user_id": user_id}


@auth_router.post('/refresh', status_code=status.HTTP_200_OK, response_model=RefreshTokenSchemaResponse,
    summary="Refresh access token",
    description="Obtain a new access token and refresh token using a refresh token.", )
def refresh_token(request: RefreshTokenSchemaRequest, auth_service: IAuthService = Injected(IAuthService)):
    token: RefreshTokenDataModel = auth_service.refresh_token(request.refresh_token)
    return token
