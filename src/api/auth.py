from fastapi import APIRouter, Response


from src.exceptions import confirm_password
from src.schemas.user import UserRegisterRequest, UserWithHashedPassword, LoginUser

from src.services.auth import AuthService
router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])




@router.post("/register")
async def register_user(user:UserRegisterRequest):
    confirm_password(user.password, user.password_confirm)

    hashed_password = AuthService().hash_password(user.password)

    userWithHashedPassword = UserWithHashedPassword(email=user.email,hashed_password=hashed_password)

    return {"userWithHashedPassword":userWithHashedPassword}

@router.post("/login")
async def login_user(user: LoginUser):
    ...

@router.post("/logout")
async def logout_user(response:Response):
    ...
