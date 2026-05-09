import re

from fastapi import HTTPException


def confirm_password(password: str, confirm_password: str):
    if password != confirm_password:
        raise HTTPException(status_code=401,
                            detail=f"Пароль в строке password({password}) "
                                   f"не совпадает с паролем в строке confirm_password({confirm_password})")
    check_password_validate(password)

pattern = r'^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-zА-Яа-я\d@$!%*#?&_]{8,}$'
def check_password_validate(password:str):
    if re.match(pattern, password) is None:
        raise HTTPException(status_code=401, detail="Пароль должен быть не меньше 8 символов, "
                                                    "иметь буквы верхнего и "
                                                    "нижнего регистра, иметь хотя бы одну цифру, "
                                                    "а также один или более из специальных "
                                                    "символов(@$!%*#?&_)")



class ProxyServiceExceptions(Exception):

    detail = "Очень неожиданная ошибочка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ProxyServiceExceptions):
    detail = "Объект не найден"


class UserNotFoundException(ProxyServiceExceptions):
    detail = "Пользователь не найден"


class UserAlreadyLogInException(ProxyServiceExceptions):
    detail = "Пользователь уже авторизован"


class UserAlreadyExistsException(ProxyServiceExceptions):

    detail = "Пользователь уже существует"

class ObjectAlreadyExistsException(ProxyServiceExceptions):
    detail = "нет "



class ProxyServiceHTTPExceptions(HTTPException):
    status_code = 404
    detail = None
    def __init__(self, detail: str = None, *args, **kwargs):
        detail = detail or self.detail
        super().__init__(status_code=self.status_code, detail=detail)

class UserWithSuchEmailAlreadyExistsHTTPExceptions(ProxyServiceHTTPExceptions):
    status_code = 409
    detail = "Пользователь уже существует!"


class UserNotFoundHTTPException(ProxyServiceHTTPExceptions):
    status_code = 404
    detail = "Пользователь не найден!"



class WrongPasswordHTTPException(ProxyServiceHTTPExceptions):
    status_code = 401
    detail = "Пароль не верный"

class UserAlreadyLogInHTTPException(ProxyServiceHTTPExceptions):
    status_code = 400
    detail = "Вы уже авторизованы"

class UserAlreadyLogOutHTTPException(ProxyServiceHTTPExceptions):
    status_code = 400
    detail = "Вы уже вышли из аккаунта"