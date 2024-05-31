from pydantic import BaseModel
from sqlalchemy import insert, select, join
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.pg import async_session_maker

from src.model.group import Group, UserGroup
from src.model.user import User
from src.util.repository import SQLAlchemyRepository


class OperationGroupRepository(SQLAlchemyRepository):
    model = Group

class OperationUserGroupRepository(SQLAlchemyRepository):
    model = UserGroup

    async def get_sudent_by_group(
        self,
        group_id: int,
    ):
        async with async_session_maker() as session:
            session: AsyncSession = session
            response = select(User).where(User.id == self.model.user_id).where(self.model.group_id == group_id)
            res = await session.execute(response)
            res = [row[0].to_read_model() for row in res.all()]
            return res