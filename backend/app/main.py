import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings # imports the settings in main.py means a missing variable stops the server at import time before it accepts a single request.
from app.routers import health

logger = logging.getLogger("uvicorn.error") # prints next to the server's own startup lines. that means we can see the logs in the terminal where the server is running. useful for debugging. 

@asynccontextmanager # this decorator makes the function a context manager that can be used with async with. It is the same as @app.on_event("startup") and @app.on_event("shutdown") but it is more modern and it is the only way to do it in FastAPI 0.95+.
async def lifespan(app: FastAPI): # lifespan is a context manager that is used to start and stop the application. replaces the old startup and shutdown events.  Code before yield runs once at startup and code after it at shutdown, like IHostedService.StartAsync / StopAsync in classic ASP.NET.
    # startup:  NOT-02 adds the DB engine, NOT-09 builds the sender registry
    logger.info("Starting Notifications API in %s mode", settings.app_env)
    yield # this is the code that will be executed when the application starts, yield is a keyword that is used to return a value from a generator function. example: def my_generator(): yield 1; yield 2; yield 3; my_generator() will return a generator object that can be used to iterate over the values 1, 2, and 3.
    # shutdown: close whatever startup opened

app = FastAPI(
    title="Notifications API",
    version="0.1.0",
    description="Notifications for authenticated users, sent by email, SMS or push.",
    lifespan=lifespan,
)

app.include_router(health.router)