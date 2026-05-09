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