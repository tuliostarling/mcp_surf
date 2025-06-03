import redis.asyncio as redis
import json
from config.settings import AppSettings

REDIS_URL = AppSettings().redis_url
SESSION_TTL = 86400


class ContextManager:
    def __init__(self):
        self.redis = redis.from_url(
            REDIS_URL, encoding="utf-8", decode_responses=True
        )

    async def save_message(
        self, session_id: str, user_message: str, assistant_response: str
    ):
        """
        Appends a new user/assistant interaction to the session history keeping latests messages at the head.
        """
        history_key = f"session:{session_id}"
        message = {"user": user_message, "response": assistant_response}

        await self.redis.lpush(history_key, json.dumps(message))
        await self.redis.expire(history_key, SESSION_TTL)

    async def load_history(self, session_id: str) -> list[dict]:
        """
        Loads the full conversation history for a session and reverse back to chronological order.
        """
        history_key = f"session:{session_id}"

        messages = await self.redis.lrange(history_key, 0, -1)
        return [json.loads(msg) for msg in reversed(messages)] if messages else []

    async def clear_context(self, session_id: str):
        """
        Clears the session context for the given session_id.
        """
        history_key = f"session:{session_id}"
        await self.redis.delete(history_key)
