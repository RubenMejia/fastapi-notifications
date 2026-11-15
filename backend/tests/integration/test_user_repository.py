import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import EmailAlreadyRegisteredError
from app.models.user import User
from app.repositories.user_repository import UserRepository


async def test_add_duplicate_email_raises_domain_error(db: AsyncSession) -> None:
    users = UserRepository(db)
    await users.add(User(email="test@example.com", hashed_password="x"))

    # pytest expects that, catches that type, and fails if it is missing or the wrong type
    with pytest.raises(EmailAlreadyRegisteredError):
        await users.add(User(email="test@example.com", hashed_password="y"))

    assert await users.get_by_email("test@example.com") is not None  # session still useable
