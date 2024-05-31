from typing import List
from src.repositories.question import OperationQuestionRepository
from src.scheme.answer import AnswerCreate, AnswerRead, UserAnswerCreate
from src.repositories.answer import OperationAnswerRepository, OperationUserAnswerRepository

class AnswerServise:
    
    async def add_answer(
        self,
        question_id: int,
        model: AnswerCreate,
        user_id: int,
    ) -> AnswerRead:
        model_dict = model.model_dump()
        print(model_dict)
        stmt = await OperationAnswerRepository().add_one(model_dict)
        
        model_user_answer = UserAnswerCreate(
            user_id = user_id,
            answer_id = stmt.answer_id,
            question_id = question_id
        )
        model_user_answer = model_user_answer.model_dump()
        stmt_dict = await OperationUserAnswerRepository().add_one(model_user_answer)
        return stmt

    async def get_answer_by_quiz(
        self,
        quiz_id: int,
        stud_id: int,
    ) -> List[AnswerRead]:
        # teachers_quiz = await OperationQuestionRepository().find_all
        get_answers = await OperationAnswerRepository().get_answers_by_stud(stud_id, quiz_id)
        return get_answers

    async def put_answer(
        self,
        answer_id: int,
        model: AnswerCreate,
    ) -> AnswerRead:
        model_dict = model.model_dump()
        updated_answer = await OperationAnswerRepository().put_answer_by_answer_id(answer_id, model_dict)
        return AnswerRead(
            answer_id=updated_answer.answer_id,
            stud_answer=updated_answer.stud_answer,
        )
    
    async def calculate_correct_answers_percentage(
        self,
        quiz_id: int,
        student_id: int,
    ) -> float:
        answers = await OperationAnswerRepository().get_correct_answers(quiz_id, student_id)
        correct_answers = sum(1 for stud_answer, right_answer in answers if stud_answer == right_answer)
        total_questions = len(answers)
        if total_questions == 0:
            return 0.0
        return (correct_answers / total_questions) * 100