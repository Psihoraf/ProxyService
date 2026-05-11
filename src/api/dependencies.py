from typing import Annotated

from fastapi import Depends, Request, HTTPException

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


def get_db_manager():
    return DBManager(session_factory= async_session_maker)

async def get_db():
    async with get_db_manager() as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]

def get_token(request: Request)->str:
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code = 401, detail = "Вы не прдеставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token))->int:
    data = AuthService().decode_token(token)
    return  data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]
