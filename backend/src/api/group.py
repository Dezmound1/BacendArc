from fastapi import APIRouter, Depends

from src.scheme.group import UserGroupRead
from src.service.group import GroupService
from src.model.user import User
from src.util.user_config import current_user, teacher_current_user

router = APIRouter(
    prefix="/group",
    tags=["Group"],
)


@router.get("/get_groups", summary="получение списка групп (Учитель)")
async def get_groups(
    user: User = Depends(teacher_current_user),
):
    response = await GroupService().get_groups()
    return response


@router.get("/get_stud_by_group", summary="получение студентов по группе (Учитель)")
async def get_stud_by_group(
    group_id: int,
    user: User = Depends(teacher_current_user),
):
    """# для отображения указываем id группы"""
    response = await GroupService().get_stud_by_group(group_id)
    return response


@router.post("/add_stud_at_group", summary="добавление студента в группу (Студент)")
async def add_stud_at_group(
    group_id: int,
    user: User = Depends(current_user),
) -> UserGroupRead:
    """# для отображения указываем id группы"""
    stmt = await GroupService().add_user_at_group(group_id, user.id)
    return stmt
