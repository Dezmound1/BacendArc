from typing import Generic, Optional
from fastapi import Depends, HTTPException, Request, Response

from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models

from src.util.enum import Role
from src.scheme.group import UserGroupCreate
from src.repositories.user import OperationUserRepository
from src.scheme.user import UserCreate
from src.db.pg import async_session_maker
from conf import SECRET_AUTH
from src.util.auth import get_user_db
from src.model.user import User


class UserManager(Generic[models.UP, models.ID], IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_login(self, user: User, request: Optional[Request] = None, response: Optional[Response] = None):
        print(f"User {user.id} logged in.")

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
        # group_id: Optional[int] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = user_create.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        # user_group_id = user_dict.pop("group_id")
        created_user = await OperationUserRepository().add_one(user_dict)
        
        # if user_group_id != 0 and user_dict["role"] == Role.STUDENT:
        #     user_group = UserGroupCreate(
        #         user_id=created_user.id,
        #         group_id=user_group_id,
        #     )
        #     user_group = user_group.model_dump()
        #     await OperationUserGroupRepositiory().add_one(user_group)

        
        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
