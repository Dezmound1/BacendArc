from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel


class QuestionRead(BaseModel):
    question_id: int
    text: str
    right_answer: str


class QuestionCreate(BaseModel):
    text: str
    right_answer: str


class QuizRead(BaseModel):
    quiz_id: int
    title: str


class QuizCreate(BaseModel):
    title: str


class AddQuiz(BaseModel):
    quiz: QuizCreate
    question: List[QuestionCreate]


class UserQuizRead(BaseModel):
    quiz_question_id: int
    quiz_id: int
    user_id: int

class UserQuizCreate(BaseModel):
    quiz_id: int
    user_id: int
