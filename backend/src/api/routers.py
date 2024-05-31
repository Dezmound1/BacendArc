from src.api.user import router as user_router
from src.api.answer import router as answer_router
from src.api.question import router as question_router
from src.api.group import router as group_router


all_routers = [
    user_router,
    answer_router,
    question_router,
    group_router,
]
