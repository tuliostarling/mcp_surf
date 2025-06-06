from datetime import date
from langchain_core.messages import SystemMessage, HumanMessage
from core.agent import get_agent_executor
from core.prompts import ANSWER_PROMPT, SURF_SLANG_PT_BR
import uuid

DEFAULT_ERROR = "Desculpe, não consegui entender a sua mensagem."


async def orchestrate_user_prompt(
    user_prompt: str, session_id: str | None = None
) -> str:
    try:
        session_id = session_id or str(uuid.uuid4())
        agent, config = await get_agent_executor(session_id)

        prompt_template = ANSWER_PROMPT.partial(
            current_date=date.today().isoformat(),
            surf_slang=SURF_SLANG_PT_BR,
        )

        prompt_with_user = prompt_template.format_prompt(
            messages=[HumanMessage(content=user_prompt)]
        )

        full_message_list = prompt_with_user.to_messages()

        payload_messages = [
            {
                "role": "system" if isinstance(msg, SystemMessage) else "user",
                "content": msg.content,
            }
            for msg in full_message_list
        ]

        result = agent.invoke({"messages": payload_messages}, config=config)
        return result["messages"][-1].content

    except Exception as e:
        print(f"[ERROR] Agent failure: {e}")
        return DEFAULT_ERROR
