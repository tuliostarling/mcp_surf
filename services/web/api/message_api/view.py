from fastapi import APIRouter, Header
from core import orchestrate_user_prompt
from services.web.api.message_api.schema import UserMessage, MessageResponse

router = APIRouter()


@router.post("/message", response_model=MessageResponse)
async def handle_message(
    user_message: UserMessage,
    session_id: str = Header(None),
) -> MessageResponse:
    response_text = await orchestrate_user_prompt(user_message.prompt, session_id)
    return MessageResponse(response=response_text)
