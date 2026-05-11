from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.models import UserOrm
from src.repositories.base import BaseRepository
from src.schemas.user import UserResponse, UserWithHashedPassword


class UserRepository(BaseRepository):
    model = UserOrm
    schema = UserResponse

    async def get_user_with_hashed_password(self, email:EmailStr):

        query = select(self.model).filter_by(email = email)

        result = await self.session_factory.execute(query)

        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return UserWithHashedPassword.model_validate(model)

    async def get_me(self, *filter, **filter_by):
        try:
            query = select(self.model).filter(*filter).filter_by(**filter_by)
            result = await self.session_factory.execute(query)
        except NoResultFound:
            raise ObjectNotFoundException

        result = result.scalars().one()
        return self.schema.model_validate(result)