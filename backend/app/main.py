import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

# import settings. A missing variable stops the server at import time before it accepts any request.
from app.core.config import settings
from app.db.session import engine
from app.routers import health

# prints next to the server's own startup lines.
# that means we can see the logs in the terminal where the server is running.useful for debugging.
logger = logging.getLogger("uvicorn.error")


# this decorator makes the function a context manager that can be used with async with.
# It is the same as @app.on_event("startup") and @app.on_event("shutdown") but it is more modern.
@asynccontextmanager

# lifespan is a context manager that is used to start and stop the application.
# replaces the old startup and shutdown events.
# Code before yield runs once at startup and code after it at shutdown,
# like IHostedService.StartAsync / StopAsync in classic ASP.NET.
async def lifespan(app: FastAPI):
    # startup:  NOT-02 adds the DB engine, NOT-09 builds the sender registry
    logger.info("Starting Notifications API in %s mode", settings.app_env)

    # this is the code that will be executed when the application starts,
    # yield is a keyword that is used to return a value from a generator function.
    # example: def my_generator(): yield 1; yield 2; yield 3;
    # my_generator() will return a generator object that can be used to iterate over values 1, 2, 3.
    yield
    # shutdown: close whatever startup opened
    await engine.dispose()  # close every pooled connection
    logger.info("Database connections closed")


app = FastAPI(
    title="Notifications API",
    version="0.1.0",
    description="Notifications for authenticated users, sent by email, SMS or push.",
    lifespan=lifespan,
)

app.include_router(health.router)
