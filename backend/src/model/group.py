from __future__ import annotations

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Enum, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.scheme.group import GroupRead, UserGroupRead
from src.db.pg import Base


class Group(Base):
    __tablename__ = "group"

    group_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    def to_read_model(self) -> GroupRead:
        return GroupRead(
            group_id=self.group_id,
            name=self.name,
        )


class UserGroup(Base):
    __tablename__ = "user_group"

    user_group_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group.group_id"))

    def to_read_model(self) -> UserGroupRead:
        return UserGroupRead(
            user_group_id=self.user_group_id,
            user_id=self.user_id,
            group_id=self.group_id,
        )
