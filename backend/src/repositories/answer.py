from typing import List, Tuple
from pydantic import BaseModel
from sqlalchemy import insert, select, join, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.question import Question, QuizQuestion
from src.model.answer import Answer, UserAnswer
from src.db.pg import async_session_maker

from src.util.repository import SQLAlchemyRepository


class OperationAnswerRepository(SQLAlchemyRepository):
    model = Answer

    async def get_answers_by_stud(
        self,
        stud_id: int,
        quiz_id: int,
    ):
        async with async_session_maker() as session:
            session: AsyncSession = session

            subquery_quiz_questions = (
                select(QuizQuestion.question_id).where(QuizQuestion.quiz_id == quiz_id)
            ).subquery()

            subquery_questions = (
                select(Question.question_id).where(Question.question_id.in_(subquery_quiz_questions))
            ).subquery()

            subquery_user_answers = (
                select(UserAnswer.answer_id)
                .where(UserAnswer.user_id == stud_id)
                .where(UserAnswer.question_id.in_(subquery_questions))
            ).subquery()

            response = select(self.model).where(self.model.answer_id.in_(subquery_user_answers))

            res = await session.execute(response)
            return [row[0].to_read_model() for row in res.all()]
    
    async def put_answer_by_answer_id(
        self,
        answer_id: int,
        answer_data: dict,
    ):
        async with async_session_maker() as session:
            session: AsyncSession = session
            stmt = (
                update(self.model)
                .where(self.model.answer_id == answer_id)
                .values(**answer_data)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            updated_answer = res.scalar_one_or_none()
            if updated_answer:
                return updated_answer
            else:
                raise ValueError("Failed to update Answer")
    
    async def get_correct_answers(
        self,
        quiz_id: int,
        student_id: int,
    ) -> List[Tuple[str, str]]:
        async with async_session_maker() as session:
            session: AsyncSession = session

            subquery_quiz_questions = (
                select(QuizQuestion.question_id)
                .where(QuizQuestion.quiz_id == quiz_id)
            ).subquery()

            subquery_user_answers = (
                select(UserAnswer.answer_id)
                .where(UserAnswer.user_id == student_id)
                .where(UserAnswer.question_id.in_(subquery_quiz_questions))
            ).subquery()

            response = (
                select(Answer.stud_answer, Question.right_answer)
                .join(UserAnswer, UserAnswer.answer_id == Answer.answer_id)
                .join(Question, Question.question_id == UserAnswer.question_id)
                .where(UserAnswer.answer_id.in_(subquery_user_answers))
            )
            
            res = await session.execute(response)
            return res.all()



class OperationUserAnswerRepository(SQLAlchemyRepository):
    model = UserAnswer
