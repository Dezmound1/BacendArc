from fastapi import APIRouter, Depends
from src.scheme.user import UserCreate, UserRead
from src.util.user_config import fastapi_users, auth_backend

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)