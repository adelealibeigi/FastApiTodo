from pydantic import BaseModel, Field, EmailStr


class UserResponseSchema(BaseModel):
    id: int = Field(..., description="Unique identifier of the object")
    username: str = Field(..., max_length=250, min_length=3, description="Username of the user")
    password: str = Field(..., description="Password of the user")
    phone_number: str | None = Field(default=None, min_length=11, max_length=11, description="Phone number of the user")
    email: EmailStr | None = Field(description='Email address of the user')
