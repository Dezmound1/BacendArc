from src.model.user import User
from src.scheme.question import QuestionCreate, UserQuizRead
from src.util.repository import SQLAlchemyRepository
from sqlalchemy import insert, select, join, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.pg import async_session_maker


from src.model.question import Question, Quiz, QuizQuestion, UserQuiz


class OperationQuestionRepository(SQLAlchemyRepository):
    model = Question

    async def put_question(
        self,
        question_id: int,
        question_data: dict,
    ):
        async with async_session_maker() as session:
            session: AsyncSession = session
            stmt = (
                update(self.model)
                .where(self.model.question_id == question_id)
                .values(**question_data)
                .returning(self.model)
            )
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()
    

    async def get_result(self, quiz_id: int):
        async with async_session_maker() as session:
            session: AsyncSession = session
            query = (
                select(self.model)
                .join(QuizQuestion, QuizQuestion.question_id == self.model.question_id)
                .where(QuizQuestion.quiz_id == quiz_id)
            )
            res = await session.execute(query)
            questions = res.scalars().all()
            return [question.to_read_model() for question in questions]


class OperationQuizRepository(SQLAlchemyRepository):
    model = Quiz

    async def get_quiz_by_user_id(
        self,
        user_id: int,
    ):
        async with async_session_maker() as session:
            session: AsyncSession = session
            response = (
                select(self.model)
                .join(UserQuiz, UserQuiz.quiz_id == self.model.quiz_id)
                .where(UserQuiz.user_id == user_id)
            )
            res = await session.execute(response)
            quizzes = res.scalars().all()
            return [quiz.to_read_model() for quiz in quizzes]


class OperationQuizQuestionRepository(SQLAlchemyRepository):
    model = QuizQuestion

    async def add_question_at_quiz(
        self,
        quiz_id: int,
        question_id: int,
    ):
        async with async_session_maker() as session:
            session: AsyncSession = session
            stmt = (
                insert(self.model)
                .values(quiz_id=quiz_id, question_id=question_id)
                .returning(self.model.quiz_question_id)
            )
            res = await session.execute(stmt)
            await session.commit()
            return f"result: {res.scalar_one()}"


class OperationUserQuizRepository(SQLAlchemyRepository):
    model = UserQuiz

    async def add_quiz_to_user(
        self,
        model_dict: dict,
    ):
        async with async_session_maker() as session:
            session: AsyncSession = session
            stmt = insert(self.model).values(**model_dict).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    