from fastapi import FastAPI
from contextlib import asynccontextmanager


def register_lifespan(app: FastAPI) -> None:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        print("🚀 Chat API starting up...")
        yield
        print("🛑 Chat API shutting down...")

    app.router.lifespan_context = lifespan
