from fastapi import APIRouter
from services.web.api import health_api, message_api

api_router = APIRouter()
api_router.include_router(health_api.router)
api_router.include_router(message_api.router)
