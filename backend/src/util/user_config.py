from enum import Enum
from inspect import signature
from typing import Optional, Sequence, Tuple, Generic
from makefun import with_signature


from fastapi import HTTPException, status
from fastapi_users import BaseUserManager, FastAPIUsers, models
from fastapi_users.manager import UserManagerDependency


from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy, Authenticator
from fastapi_users.authentication.authenticator import (
    name_to_variable_name,
    name_to_strategy_variable_name,
    EnabledBackendsDependency,
)
from fastapi_users.authentication.strategy import Strategy


from src.util.enum import Role
from src.service.user import get_user_manager
from src.model.user import User
from conf import SECRET_AUTH

cookie_transport = CookieTransport(cookie_name="users_cookie", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


class AuthenticatorCustom(Authenticator):
    def current_user(
        self,
        optional: bool = False,
        active: bool = False,
        verified: bool = False,
        superuser: bool = False,
        role: Enum = Role.STUDENT,
        get_enabled_backends: Optional[EnabledBackendsDependency] = None,
    ):
        signature = self._get_dependency_signature(get_enabled_backends)

        @with_signature(signature)
        async def current_user_dependency(*args, **kwargs):
            user, _ = await self._authenticate(
                *args,
                optional=optional,
                active=active,
                verified=verified,
                superuser=superuser,
                role=role,
                **kwargs,
            )
            return user

        return current_user_dependency

    async def _authenticate(
        self,
        *args,
        user_manager: BaseUserManager[models.UP, models.ID],
        optional: bool = False,
        active: bool = False,
        role: Enum = Role.STUDENT,
        **kwargs,
    ) -> Tuple[Optional[models.UP], Optional[str]]:
        user: Optional[models.UP] = None
        token: Optional[str] = None
        enabled_backends: Sequence[AuthenticationBackend] = kwargs.get("enabled_backends", self.backends)
        for backend in self.backends:
            if backend in enabled_backends:
                token = kwargs[name_to_variable_name(backend.name)]
                strategy: Strategy[models.UP, models.ID] = kwargs[name_to_strategy_variable_name(backend.name)]
                if token is not None:
                    user = await strategy.read_token(token, user_manager)
                    if user:
                        break
        status_code = status.HTTP_401_UNAUTHORIZED

        if user:
            status_code = status.HTTP_403_FORBIDDEN
            if active and not user.is_active:
                status_code = status.HTTP_401_UNAUTHORIZED
                user = None

            elif not user.role == role:
                user = None
        if not user and not optional:
            raise HTTPException(status_code=status_code)
        return user, token


class Refresh(FastAPIUsers[models.UP, models.ID]):

    authenticator: Authenticator

    def __init__(
        self,
        get_user_manager: UserManagerDependency[models.UP, models.ID],
        auth_backends: Sequence[AuthenticationBackend],
    ):
        self.authenticator = AuthenticatorCustom(auth_backends, get_user_manager)
        self.get_user_manager = get_user_manager
        self.current_user = self.authenticator.current_user


fastapi_users = Refresh[User, int](
    get_user_manager,
    [auth_backend],
)
authenticator = AuthenticatorCustom([auth_backend], get_user_manager)


current_user = fastapi_users.current_user(role=Role.STUDENT)
teacher_current_user = fastapi_users.current_user(role=Role.TEACHER)
