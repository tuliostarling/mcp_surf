from fastapi import FastAPI
from contextlib import asynccontextmanager


def register_lifespan(app: FastAPI) -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("🚀 App starting up...")
        yield
        print("🛑 App shutting down...")

    app.router.lifespan_context = lifespan
