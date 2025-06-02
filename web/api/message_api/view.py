from fastapi import APIRouter
from core.orchestrator import orchestrate_user_prompt
from web.api.message_api.schema import UserMessage, MessageResponse

router = APIRouter()


@router.post("/message", response_model=MessageResponse)
async def handle_message(user_message: UserMessage) -> MessageResponse:
    response_text = await orchestrate_user_prompt(user_message.prompt)
    return MessageResponse(response=response_text)
