import asyncio

from app.core.errors import EmailAlreadyRegisteredError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    async def register(self, data: UserCreate) -> User:
        if await self.users.get_by_email(data.email) is not None:
            raise EmailAlreadyRegisteredError(data.email)

        # Argon2 takes -0.1s of CPU on purpose to slow down brute force attacks
        # a worker thread keeps the event loop free

        hashed = await asyncio.to_thread(hash_password, data.password)
        return await self.users.add(User(email=data.email, hashed_password=hashed))
