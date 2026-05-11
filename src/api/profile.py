from fastapi import APIRouter

from src.api.dependencies import UserIdDep, DBDep
from src.services.profile import ProfileService

router = APIRouter(prefix="/profile", tags=["Профиль"])

@router.get("/")
async def get_me(user_id:UserIdDep, db:DBDep):

    me = await ProfileService(db).get_me(user_id)

    return me