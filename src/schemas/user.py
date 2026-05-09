from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
    activation_key: str | None = None
    activation_key_expires: datetime | None = None

class UserWithHashedPassword(UserBase):
    hashed_password: str

class UserInDb(UserResponse):
    hashed_password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserRegisterRequest(UserBase):
    password: str
    password_confirm: str



