from pydantic import BaseModel as Base, ConfigDict
from datetime import date
from schemas.application import ApplicationResponse


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_email_verified: bool = False
    scopes: list[str] | str


class CreateUser(UserBase):
    password: str
    dob: date


class UserResponse(UserBase):
    id: int
    applications: list[ApplicationResponse] = []


class CurrentUserResponse(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordResetReq(BaseModel):
    email: str | None
    dob: date
