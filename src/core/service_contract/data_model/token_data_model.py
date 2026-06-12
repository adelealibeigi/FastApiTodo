from dataclasses import dataclass
from typing import Union


@dataclass
class TokenDataModel:
    access_token: str
    refresh_token: str


@dataclass
class RefreshTokenDataModel:
    access_token: str


@dataclass
class TokenPayloadDataModel:
    user_id: int
