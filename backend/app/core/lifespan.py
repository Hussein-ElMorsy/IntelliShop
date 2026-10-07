from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIteratorprint("Starting IntelliShop🔛")
    yield
    engine.dispose()
    print("Stopping IntelliShop🔚")