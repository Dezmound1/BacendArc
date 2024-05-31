from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel


class GroupRead(BaseModel):
    group_id: int
    name: str

class UserGroupCreate(BaseModel):
    user_id: int
    group_id: int

class UserGroupRead(BaseModel):
    user_group_id: int
    user_id: int
    group_id: int