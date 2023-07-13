from pydantic import BaseModel
from datetime import date
from schemas.application import ApplicationResponse


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_email_verified: bool

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: str
    dob: date


class UserResponse(UserBase):
    id: str
    applications: list[ApplicationResponse] = []


# class LoginUser(BaseModel):
#     email: str
#     password: str
#
#     class Config:
#         orm_mode = True


class CurrentUserResponse(UserBase):
    id: str


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class PasswordResetReq(BaseModel):
    email: str
    hint_question: bool
    hint_answer: str | None

    class Config:
        orm_mode = True
