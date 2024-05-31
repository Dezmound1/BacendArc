
from src.scheme.group import GroupRead, UserGroupCreate, UserGroupRead
from src.repositories.group import OperationGroupRepository, OperationUserGroupRepository
from src.repositories.user import OperationUserRepository


class GroupService:
    async def add_user_at_group(
        self,
        group_id: int,
        user_id: int,
    ) -> UserGroupRead:
        user = await OperationUserRepository().find_one(user_id)
        schema = UserGroupCreate(
            user_id=user.id,
            group_id=group_id,
        )
        schema = schema.model_dump()
        stmt = await OperationUserGroupRepository().add_one(schema)
        return stmt

    async def get_groups(
        self,
    ):
        response = await OperationGroupRepository().find_all()
        list_response = []
        for res in response:
            list_response.append(res)
        print(list_response)
        return list_response
    
    async def get_stud_by_group(
            slef,
            group_id: int,

    ):
        response = await OperationUserGroupRepository().get_sudent_by_group(group_id)
        return response
