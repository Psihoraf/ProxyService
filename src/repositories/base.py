import logging

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.exceptions import ObjectAlreadyExistsException


class BaseRepository:
    model = None
    schema = None
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def add_user(self, data: BaseModel):
        try:
            added_user = insert(self.model).values(**data.model_dump()).returning(self.model)

            result = await self.session_factory.execute(added_user)

            result = result.scalars().one_or_none()
            return self.schema.model_validate(result)

        except IntegrityError as ex:
            print(f"{type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.exception(
                    f"Незнакомая ошибка: не удалось добавить данные в БД, входные данные={data}"
                )
                raise ex