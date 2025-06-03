from fastapi import APIRouter, Header, HTTPException
from core.orchestrator import orchestrate_user_prompt
from web.api.message_api.schema import UserMessage, MessageResponse
import uuid

router = APIRouter()


@router.post("/message", response_model=MessageResponse)
async def handle_message(
    user_message: UserMessage,
    session_id: str = Header(None),
) -> MessageResponse:
    response_text = await orchestrate_user_prompt(user_message.prompt, session_id)
    return MessageResponse(response=response_text)
