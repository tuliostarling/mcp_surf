from fastapi import FastAPI
from config.loggin_params import LOGGING_CONFIG
import logging
from web.api.router import api_router
from web.lifetime import register_lifespan

def get_app() -> FastAPI:
    logging.basicConfig(**LOGGING_CONFIG)
    app = FastAPI(title="MCP Surf API")
    register_lifespan(app)
    app.include_router(api_router)
    return app
