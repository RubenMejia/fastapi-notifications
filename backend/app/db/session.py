from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# the connection pool, one per app. keeps connections alive and reuses them.
# pool_pre_ping=True means that the connection will be pinged before being used.
engine = create_async_engine(settings.database_url, pool_pre_ping=True)
# the session factory, one per app. creates and closes sessions.
# expire_on_commit=False: objects keep their loaded values after commit(), because
# async code cannot lazily reload expired attributes.
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# this is a generator. A dependency injection function with yield returning a scoped lifetime.
async def get_db() -> AsyncIterator[AsyncSession]:
    """One session per request, closed when the request ends."""
    async with SessionLocal() as session:
        yield session


# for background senders. which runs after the request session is closed.
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """For code that must open its own sessions, such as background jobs (NOT-09)."""
    return SessionLocal
