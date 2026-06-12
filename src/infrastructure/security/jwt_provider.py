from datetime import timedelta, timezone, datetime

import jwt
from jwt import InvalidSignatureError, DecodeError, ExpiredSignatureError
from src.core.exceptions.service_exceptions import TokenExpiredError, InvalidTokenError
from src.core.service_contract.data_model.token_data_model import TokenPayloadDataModel
from src.core.service_contract.interface.itoken_provider import ITokenProvider
from src.infrastructure.config import settings


class TokenProvider(ITokenProvider):

    @staticmethod
    def generate_access_token(user_id: int, expires_in: int = 15 * 60) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "type": "access",
            "user_id": user_id,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    @staticmethod
    def generate_refresh_token(user_id: int, expires_in: int = 30) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "type": "refresh",
            "user_id": user_id,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(days=expires_in)).timestamp())
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_refresh_token(token: str) -> TokenPayloadDataModel:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise InvalidTokenError("Provided token is missing required claim: user_id")
            if payload.get("type")!="refresh":
                raise InvalidTokenError("Provided token is not a refresh token")
            return TokenPayloadDataModel(user_id=user_id)

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Refresh token has expired")

        except (jwt.InvalidTokenError, jwt.InvalidSignatureError, jwt.DecodeError, ValueError, KeyError) as e:
            raise InvalidTokenError("Invalid refresh token")

    @staticmethod
    def decode_access_token(token: str) -> TokenPayloadDataModel:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise InvalidTokenError("Provided token is missing required claim: user_id")
            if payload.get("type")!="access":
                raise InvalidTokenError("Provided token is not a access token")
            return TokenPayloadDataModel(user_id=user_id)

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("access token has expired")

        except (jwt.InvalidTokenError, jwt.InvalidSignatureError, jwt.DecodeError, ValueError, KeyError) as e:
            raise InvalidTokenError("Invalid access token")
