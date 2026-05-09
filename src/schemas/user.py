from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    is_active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    activation_key: str | None = None
    activation_key_expires: datetime | None = None

class UserWithHashedPassword(UserBase):
    hashed_password: str
    id:int

class UserResponse(User):
    id:int

class UserInDb(User):
    hashed_password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserRegisterRequest(UserBase):
    password: str
    password_confirm: str



