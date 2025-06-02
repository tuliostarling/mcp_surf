from langchain_openai import ChatOpenAI
from langchain.prompts import BasePromptTemplate
from config.settings import AppSettings

OPENAI_API_KEY = AppSettings().openai_api_key
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0)


async def run_llm_chain(prompt_template: BasePromptTemplate, vars: dict) -> str:
    """
    Run a LangChain RunnableSequence with the centralized llm and a provided prompt_template.

    Args:
        prompt_template (BasePromptTemplate): the LangChain prompt template.
        vars (dict): dictionary of variables to fill in the prompt.

    Returns:
        str: the output from the LLM.
    """
    chain = prompt_template | llm
    response = await chain.ainvoke(vars)
    raw_text = response.content if hasattr(response, "content") else str(response)
    cleaned_response = raw_text.strip().strip("```").replace("json", "").strip()
    return cleaned_response