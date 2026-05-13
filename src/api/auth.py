from fastapi import APIRouter, Response, Request, Body

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import confirm_password, UserNotFoundException, UserNotFoundHTTPException, \
    UserAlreadyLogInException, UserAlreadyLogInHTTPException, UserAlreadyLogOutHTTPException, \
    UserAlreadyExistsException, UserWithSuchEmailAlreadyExistsHTTPExceptions
from src.schemas.user import UserRegisterRequest, UserWithHashedPassword, LoginUser, UserInDb

from src.services.auth import AuthService
from src.tasks.tasks import send_email_with_activation_key
from utils.activation_key import key_generator

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])




@router.post("/register")
async def register_user( db: DBDep, user:UserRegisterRequest = Body(openapi_examples ={
            "1":{"summary": "User1", "value":{
                "email":"user@example.com",
                "password":"QQqq11**",
                "password_confirm":"QQqq11**"
            } },
            "2":{"summary": "User2", "value":{
                "email":"narek77-00@mail.ru",
                "password":"PPpp22$$",
                "password_confirm": "PPpp22$$"

            }},
        })):
    confirm_password(user.password, user.password_confirm)
    try:
        key = await AuthService(db).register_user(user)

        send_email_with_activation_key.delay(
            email=user.email,
            activation_key=key,
        )
    except UserAlreadyExistsException:
        raise UserWithSuchEmailAlreadyExistsHTTPExceptions
    return {"user":user}

@router.post("/login")
async def login_user(db: DBDep, response: Response, request: Request, user: LoginUser =Body(openapi_examples ={
            "1":{"summary": "User1", "value":{
                "email":"user@example.com",
                "password":"QQqq11**",
            } },
            "2":{"summary": "User2", "value":{
                "title":"user2@example.com",
                "location":"PPpp22$$",
            }},
        })):
    try:
        request.cookies.get("access_token")
        access_token = await AuthService(db).login_user(user)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserAlreadyLogInException:
        raise UserAlreadyLogInHTTPException

    response.set_cookie("access_token", access_token)
    return {"email": user.email, "access_token": access_token}

@router.post("/logout")
async def logout_user(response:Response, request:Request):

    if not request.cookies.get("access_token"):
        raise UserAlreadyLogOutHTTPException
    response.delete_cookie("access_token")
    return {"Status":"OK"}

@router.get("/login/profile")
async def get_me(user_id:UserIdDep, db:DBDep):

    me = await AuthService(db).get_me(user_id)

    return me