from src.exceptions import ObjectNotFoundException,UserNotFoundHTTPException
from src.services.base import BaseService


class ProfileService(BaseService):
    async def get_me(self, user_id: int):
        try:
            me = await self.db.users.get_me(id=user_id)
            return me
        except ObjectNotFoundException:
            raise UserNotFoundHTTPException