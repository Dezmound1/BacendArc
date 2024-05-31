from typing import List

from src.scheme.question import AddQuiz, QuestionCreate, QuestionRead, QuizRead, UserQuizCreate

from src.model.user import User
from src.repositories.question import (
    OperationQuestionRepository,
    OperationQuizQuestionRepository,
    OperationQuizRepository,
    OperationUserQuizRepository,
)


class QuestionService:

    async def add_quiz(
        self,
        model: AddQuiz,
    ) -> AddQuiz:
        quiz_dump = model.quiz.model_dump()
        stmt_quiz = await OperationQuizRepository().add_one(quiz_dump)
        question_list = []
        for question in model.question:
            question_dump = question.model_dump()
            stmt_question = await OperationQuestionRepository().add_one(question_dump)

            await OperationQuizQuestionRepository().add_question_at_quiz(
                stmt_quiz.quiz_id,
                stmt_question.question_id,
            )
            question_list.append(question_dump)

        return AddQuiz(
            quiz=quiz_dump,
            question=question_list,
        )

    async def put_questions(
        self,
        question_id: int,
        model: QuestionCreate,
    ) -> QuestionRead:
        dict_data = model.model_dump()
        stmt = await OperationQuestionRepository().put_question(
            question_id,
            dict_data,
        )

        return QuestionRead(
            question_id=question_id,
            text=stmt.text,
            right_answer=stmt.right_answer,
        )

    async def get_questions_by_quiz(
        self,
        quiz_id: int,
    ) -> List[QuestionRead]:

        response = await OperationQuestionRepository().get_result(quiz_id)
        return response

    async def add_quiz_to_user(
        self,
        model: UserQuizCreate,
    ) -> UserQuizCreate:
        model_dict = model.model_dump()
        response = await OperationUserQuizRepository().add_quiz_to_user(model_dict)
        response = UserQuizCreate(
            quiz_id=response.quiz_id,
            user_id=response.user_id,
        )
        return response

    async def get_list_quiz(
        self,
        user_id: int,
    )-> List[QuizRead]:
        response = await OperationQuizRepository().get_quiz_by_user_id(user_id)
        return response
