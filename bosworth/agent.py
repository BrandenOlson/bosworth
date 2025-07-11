from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseLLM

from bosworth.llm import DEFAULT_LLM
from bosworth.tools import DEFAULT_TOOLS

DEFAULT_SYS_PROMPT = """You are a helpful finance AI agent named Bosworth.
You are enthusiastic and kind of a nerd, but very lovable.
Respond to every query accurately and enthusiastically.
Also respond with links or resources when relevant.
"""


def invoke_agent(query: str, llm: BaseLLM = DEFAULT_LLM, tools: list[BaseTool] = DEFAULT_TOOLS):
    llm_with_tool = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=DEFAULT_SYS_PROMPT),
        HumanMessage(query)
    ]

    ai_msg = llm_with_tool.invoke(messages)

    print(ai_msg.tool_calls)

    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {t.name: t for t in tools}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    return llm_with_tool.invoke(messages).content
