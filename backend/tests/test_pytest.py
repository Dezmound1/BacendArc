import pytest
from sqlalchemy import insert, select
from src.model.user import User
from conftest import client, async_session_maker




def test_register_422():
    response = client.post("/auth/register", json={
        "email": "dudos@mail.ru",
        "first_name": "Daniil",
        "last_name": "Frolov",
        "role": "asdfg",
        "password": "gigachad"
        }
    )

    assert response.status_code == 422


def test_register_201():
    response = client.post("/auth/register", json={
        "email": "dudos@mail.ru",
        "first_name": "Daniil",
        "last_name": "Frolov",
        "role": "teacher",
        "password": "gigachad"
        }
    )

    assert response.status_code == 201