from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import EmailAlreadyRegisteredError
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        return await self.db.scalar(select(User).where(User.email == email))

    async def add(self, user: User) -> User:
        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            if "uq_users_email" in str(
                exc.orig
            ):  # the nasme comes from the naming convention defined in base.py
                raise EmailAlreadyRegisteredError(user.email) from exc
            raise
        await self.db.refresh(user)  # loads what the database filled in: id, created_at

        return user
