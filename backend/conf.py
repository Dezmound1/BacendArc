import os

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PASS = os.environ.get("TEST_DB_PASS")


SECRET_AUTH = os.environ.get("SECRET_AUTH")

SQLALCHEMY_ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

TEST_SQLALCHEMY_ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
)