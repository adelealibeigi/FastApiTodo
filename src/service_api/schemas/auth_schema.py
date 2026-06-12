from pydantic import BaseModel, Field, model_validator, EmailStr


class TokenBaseSchema(BaseModel):
    access_token: str = Field(..., description='access token of user')
    refresh_token: str = Field(..., description='refresh token of user')


class LoginSchemaRequest(BaseModel):
    username: str = Field(..., max_length=250, min_length=3, description="Username of the user")
    password: str = Field(..., description="Password of the user")


class LoginSchemaResponse(TokenBaseSchema):
    pass


class RegisterSchemaRequest(BaseModel):
    username: str = Field(..., max_length=250, min_length=3, description="username of the user")
    password: str = Field(..., min_length=4, max_length=72, description="password of the user")
    password_confirm: str = Field(..., min_length=4, max_length=72, description="confirm password of the user")
    phone_number: str | None = Field(default=None, min_length=11, max_length=11, description="phone number of the user")
    email: EmailStr = Field(description="email address of the user")

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password!=self.password_confirm:
            raise ValueError("passwords do not match")
        return self


class RegisterSchemaResponse(BaseModel):
    user_id: int = Field(..., description="Id of the user")


class RefreshTokenSchemaRequest(BaseModel):
    refresh_token: str = Field(..., description="refresh token of user.")


class RefreshTokenSchemaResponse(BaseModel):
    access_token: str = Field(..., description="access token of user.")
