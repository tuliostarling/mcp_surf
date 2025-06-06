from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from config import AppSettings
from core.mcp_client import MCPToolAdapter

OPENAI_API_KEY = AppSettings().openai_api_key

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)

tool_adapter = MCPToolAdapter()
memory = MemorySaver()


async def get_agent_executor(session_id: str):
    tools = await tool_adapter.load()
    agent = create_react_agent(llm, tools=tools, checkpointer=memory)
    config = {"configurable": {"thread_id": session_id}}

    return agent, config
