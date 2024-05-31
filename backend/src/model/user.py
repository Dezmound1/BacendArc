from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.scheme.user import UserRead
from src.db.pg import Base

from sqlalchemy import Enum as SqlEnum
from src.util.enum import Role


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    role: Mapped[Role] = mapped_column(SqlEnum(Role))
    hashed_password: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=True) 

    def to_read_model(self) -> UserRead:
        return UserRead(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            role=self.role.value,
        )

