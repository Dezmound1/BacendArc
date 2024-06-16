from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_add_specific_user(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "dudos@mail.ru",
        "first_name": "Daniil",
        "last_name": "Frolov",
        "role": "teacher",
        "password": "gigachad"
        }
    )

    assert response.status_code == 201

async def test_add_specific_user_422(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "dudos@mail.ru",
        "first_name": "Daniil",
        "last_name": "Frolov",
        "role": "asdfgsadfg",
        "password": "gigachad"
        }
    )

    assert response.status_code == 422