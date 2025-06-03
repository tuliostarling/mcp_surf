from core.agent import get_agent
import uuid

DEFAULT_ERROR = "Desculpe, não consegui entender a sua mensagem."


async def orchestrate_user_prompt(
    user_prompt: str, session_id: str | None = None
) -> str:
    try:
        session_id = session_id or str(uuid.uuid4())
        agent_exec = get_agent(session_id)

        result = await agent_exec.ainvoke({"input": user_prompt})
        return result["output"]
    except Exception as e:
        print(f"[ERROR] Agent failure: {e}")
        return DEFAULT_ERROR
