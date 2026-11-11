from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def test_use_test_database(db: AsyncSession) -> None:
    database = await db.scalar(text("SELECT CURRENT_DATABASE()"))

    assert database == "notifications_test"
