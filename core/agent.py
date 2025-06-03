from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from datetime import date
from config.settings import AppSettings
from core.functions import functions as tools
from core.prompts import ANSWER_PROMPT, SURF_SLANG_PT_BR

OPENAI_API_KEY = AppSettings().openai_api_key
REDIS_URL = AppSettings().redis_url

llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)


def get_agent(session_id: str) -> AgentExecutor:
    chat_history = RedisChatMessageHistory(url=REDIS_URL, session_id=session_id)

    memory = ConversationBufferMemory(
        memory_key="conversation_history",
        chat_memory=chat_history,
        return_messages=True,
    )

    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=ANSWER_PROMPT.partial(
            current_date=date.today().isoformat(),
            surf_slang=SURF_SLANG_PT_BR,
        ),
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        max_iterations=5,
        early_stopping_method="force",
        verbose=False,
    )
