from pydantic import BaseModel


class UserMessage(BaseModel):
    prompt: str


class MessageResponse(BaseModel):
    response: str
