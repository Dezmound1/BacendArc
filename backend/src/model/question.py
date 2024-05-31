from __future__ import annotations

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.scheme.question import QuestionRead, QuizRead, UserQuizRead
from src.db.pg import Base


class Question(Base):
    __tablename__ = "question"

    question_id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255))
    right_answer: Mapped[str] = mapped_column(String(255))

    def to_read_model(self) -> QuestionRead:
        return QuestionRead(
            question_id=self.question_id,
            text=self.text,
            right_answer=self.right_answer,
        )


class Quiz(Base):
    __tablename__ = "quiz"

    quiz_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    def to_read_model(self) -> QuizRead:
        return QuizRead(
            quiz_id=self.quiz_id,
            title=self.title,
        )


class UserQuiz(Base):
    __tablename__ = "user_quiz"

    user_quiz_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.quiz_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    


class QuizQuestion(Base):
    __tablename__ = "quiz_question"

    quiz_question_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.quiz_id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("question.question_id"))

    def to_read_model(self) -> UserQuizRead:
        return UserQuizRead(
            quiz_question_id=self.quiz_question_id,
            quiz_id=self.quiz_id,
            question_id=self.question_id,
        )
