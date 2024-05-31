from typing import List
from fastapi import APIRouter, Depends

from src.service.question import QuestionService
from src.scheme.question import AddQuiz, QuestionCreate, QuestionRead, QuizRead, UserQuizCreate, UserQuizRead
from src.model.user import User
from src.util.user_config import current_user, teacher_current_user

router = APIRouter(
    prefix="/question",
    tags=["Question"],
)


@router.post("/add_quiz", summary="Добавление нового теста с вопросами (Учитель)")
async def add_quiz(
    model: AddQuiz,
    user: User = Depends(teacher_current_user),
) -> AddQuiz:
    stmt = await QuestionService().add_quiz(model)
    return stmt


@router.put("/put_question", summary="Изменить вопрос (Учитель)")
async def put_question(
    question_id: int,
    model: QuestionCreate,
    user: User = Depends(teacher_current_user),
):
    stmt = await QuestionService().put_questions(question_id, model)
    return stmt


@router.get("/get_questions_by_quiz", summary="Получение вопросов по тесту (Учитель)")
async def get_question_by_quiz(
    quiz_id: int,
    user: User = Depends(teacher_current_user),
) -> List[QuestionRead]:
    response = await QuestionService().get_questions_by_quiz(quiz_id)
    return response


@router.post("/add_quiz_to_user", summary="Добавление тестов студенту (Учитель)")
async def add_quiz_by_user(
    model: UserQuizCreate,
    user: User = Depends(teacher_current_user),
) -> UserQuizCreate:
    stmt = await QuestionService().add_quiz_to_user(model)
    return stmt


@router.get("/get_quiz_by_user", summary="Получение тестов назначенных студенту (Студент)")
async def get_quiz_by_user(
    user: User = Depends(current_user),
):
    response = await QuestionService().get_list_quiz(user.id)
    return response
