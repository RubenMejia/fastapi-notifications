import os

os.environ["APP_ENV"] = "test"  # before any app import: settings must read .env.test.

from collections.abc import AsyncIterator

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import make_url, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import BACKEND_DIR, settings
from app.db.base import Base
from app.db.session import get_db, get_session_factory
from app.main import app

# Safety guard: never run tests againt a database whose name does not end in _test.
TEST_DB_NAME = make_url(settings.database_url).database or ""
if not TEST_DB_NAME.endswith("_test"):
    raise RuntimeError(f"Refusing to run tests against database {TEST_DB_NAME!r}")


@pytest.fixture(scope="session", autouse=True)
def run_migrations() -> None:
    """Bring the test database to the latest migration, once per test run."""
    config = Config()  # without alembic.ini: skips its logging setup.
    config.set_main_option("script_location", str(BACKEND_DIR / "migrations"))
    command.upgrade(config, "head")


test_engine = create_async_engine(settings.database_url, poolclass=NullPool)
testSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def clean_db() -> None:
    """Every test starts with a empty tables."""
    tables = ", ".join(f'"{table.name}"' for table in Base.metadata.sorted_tables)
    if tables:
        async with test_engine.begin() as conn:
            await conn.execute(text(f"truncate {tables} RESTART IDENTITY CASCADE"))


@pytest.fixture
async def db() -> AsyncIterator[AsyncSession]:
    """A session on the test database, for arranging data and checking results."""
    async with testSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db: AsyncSession) -> AsyncIterator[AsyncClient]:
    """Calls the app in-process, its database dependencies point to the test database."""
    app.dependency_overrides[get_db] = lambda: db  # use lambda to avoid circular import.
    app.dependency_overrides[get_session_factory] = lambda: testSessionLocal()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
