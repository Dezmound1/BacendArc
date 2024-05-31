from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel

class AnswerRead(BaseModel):
    answer_id: int
    stud_answer: Optional[str | None] = str

class AnswerCreate(BaseModel):
    stud_answer: Optional[str | None] = str

class UserAnswerCreate(BaseModel):
    user_id: int
    answer_id: int
    question_id: int

class UserAnswerRead(BaseModel):
    user_answer_id: int
    user_id: int
    answer_id: int
    question_id: int