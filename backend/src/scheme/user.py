from __future__ import annotations
from typing import Any, Dict, Optional, Type, TypeVar

from fastapi_users import schemas
from pydantic import BaseModel
from src.util.enum import Role

SCHEMA = TypeVar("SCHEMA", bound=BaseModel)


def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
    return model.model_dump(*args, **kwargs)

def model_validate(schema: Type[SCHEMA], obj: Any, *args, **kwargs) -> SCHEMA:
    return schema.model_validate(obj, *args, **kwargs)


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return model_dump(
            self,
            exclude_unset=True,
            exclude={
                "id",
                "role",
            },
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})


class UserRead(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: Role

class UserCreate(CreateUpdateDictModel):
    email: str
    first_name: str
    last_name: str
    role: Role
    password: str
    # group_id: Optional[int] = None
