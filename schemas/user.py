from pydantic import BaseModel


class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: str
    isEmailVerified: bool
    dob: str

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: str

