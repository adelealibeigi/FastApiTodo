from dataclasses import dataclass


@dataclass
class UserDataModel:
    id: int
    username: str
    phone_number: str
    email: str
    # created_at
    # updated_at
