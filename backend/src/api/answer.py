from typing import List, Optional, Sequence
from fastapi import APIRouter, Depends, HTTPException
from src.scheme.answer import AnswerCreate, AnswerRead
from src.service.answer import AnswerServise
from src.util.user_config import current_user, teacher_current_user

from src.model.user import User


router = APIRouter(
    prefix="/answer",
    tags=["Answer"],
)


@router.post("/add_answer", summary="Добавление ответа на вопрос (Студент)")
async def add_answer(
    question_id: int,
    model: AnswerCreate,
    user: User = Depends(current_user),
) -> AnswerRead:
    stmt = await AnswerServise().add_answer(question_id, model, user.id)
    return stmt


@router.get("/get_answer_by_quiz", summary="Получение ответов студента на вопросы по тесту (Преподаватель)")
async def get_answer_by_quiz(
    quiz_id: int,
    stud_id: int,
    user: User = Depends(teacher_current_user),
) -> List[AnswerRead]:
    response = await AnswerServise().get_answer_by_quiz(quiz_id, stud_id)
    return response


@router.put("/put_answer", summary="Изменение ответа на вопрос (Студент)")
async def put_answer(
    answer_id: int,
    model: AnswerCreate,
    user: User = Depends(current_user),
) -> AnswerRead:
    stmt = await AnswerServise().put_answer(answer_id, model)
    return stmt


@router.get("/get_correct_answers_percentage", summary="Получить процент правильных ответов студента на тесте",  tags=["!!! Проверка теста студента !!!"])
async def get_correct_answers_percentage(
    quiz_id: int,
    student_id: int,
    user: User = Depends(teacher_current_user),
) -> float:
    """# для отображения указываем id теста и id студена"""
    percentage = await AnswerServise().calculate_correct_answers_percentage(quiz_id, student_id)
    return percentage