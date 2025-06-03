from fastapi import FastAPI
from config import LOGGING_CONFIG
from services.web.api.router import api_router
from services.web.lifetime import register_lifespan
import logging


def get_app() -> FastAPI:
    logging.basicConfig(**LOGGING_CONFIG)
    app = FastAPI(title="MCP Surf API")
    register_lifespan(app)
    app.include_router(api_router, prefix="/api")
    return app
