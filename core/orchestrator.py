from core import get_agent_executor
from langchain_core.messages import HumanMessage
import uuid

DEFAULT_ERROR = "Desculpe, não consegui entender a sua mensagem."


async def orchestrate_user_prompt(
    user_prompt: str, session_id: str | None = None
) -> str:
    try:
        session_id = session_id or str(uuid.uuid4())
        app, config = await get_agent_executor(session_id)

        input_message = HumanMessage(content=user_prompt)

        response_text = ""
        async for event in app.astream(
            {"messages": [input_message]},
            config=config,
            stream_mode="values",
        ):
            response_text = event["messages"][-1].content

        return response_text
    except Exception as e:
        print(f"[ERROR] Agent failure: {e}")
        return DEFAULT_ERROR
