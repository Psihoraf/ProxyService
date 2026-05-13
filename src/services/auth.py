from datetime import datetime, timezone, timedelta
from fastapi import HTTPException

from schemas.user import PatchUserKey
from src.config import  settings
import jwt
from passlib.context import CryptContext

from src.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException, \
    ObjectNotFoundException, UserNotFoundException, UserNotFoundHTTPException
from src.schemas.user import UserRegisterRequest, UserInDb, LoginUser
from src.services.base import BaseService
from utils.activation_key import  key_generator


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password:str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token:str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code = 401, detail = "Неверный токен" )

    async def register_user(self, user: UserRegisterRequest):
        hashed_password = self.hash_password(user.password)

        key = key_generator.generate_activation_key()
        created_at = datetime.now()
        user_in_db = UserInDb(
            email=user.email,
            hashed_password=hashed_password,
            activation_key=key,
            created_at=created_at
        )
        try:
            await self.db.users.add_object(user_in_db)
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

        await self.db.commit()
        return key

    async def login_user(self, user:LoginUser):
        try:
            user_with_hashed_pass = await self.db.users.get_user_with_hashed_password(user.email)
        except ObjectNotFoundException:
            raise UserNotFoundException

        self.verify_password(user.password, user_with_hashed_pass.hashed_password)
        access_token = self.create_access_token({"user_id":user_with_hashed_pass.id})
        return access_token

    async def get_me(self, user_id: int):
        try:
            me = await self.db.users.get_me(id=user_id)
            return me
        except ObjectNotFoundException:
            raise UserNotFoundHTTPException

    async def refresh_key(self, id: int, isPatch: bool):
        key = key_generator.generate_activation_key()
        updated_at = datetime.now()
        data = PatchUserKey(activation_key=key, updated_at=updated_at)


        user = await self.db.users.edit(data, isPatch, id=id)

        await self.db.commit()
        return user

