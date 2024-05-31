from __future__ import annotations

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Enum, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.scheme.answer import AnswerRead, UserAnswerRead
from src.db.pg import Base


class Answer(Base):
    __tablename__ = "answer"

    answer_id: Mapped[int] = mapped_column(primary_key=True)
    stud_answer: Mapped[str] = mapped_column(String(255), nullable=True)

    def to_read_model(self) -> AnswerRead:
        return AnswerRead(
            answer_id=self.answer_id,
            stud_answer=self.stud_answer,
        )


class UserAnswer(Base):
    __tablename__ = "user_answer"

    user_answer_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    answer_id: Mapped[int] = mapped_column(ForeignKey("answer.answer_id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("question.question_id"))

    def to_read_model(self) -> UserAnswerRead:
        return UserAnswerRead(
            user_answer_id=self.user_answer_id,
            user_id=self.user_id,
            answer_id=self.answer_id,
            question_id=self.question_id,
        )
