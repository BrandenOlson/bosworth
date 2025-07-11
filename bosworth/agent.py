from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel

from bosworth.llm import DEFAULT_LLM
from bosworth.tools import DEFAULT_TOOLS

DEFAULT_SYS_PROMPT = """You are a helpful finance AI agent named Bosworth.
You are enthusiastic and kind of a nerd, but very lovable.
Respond to every query accurately and enthusiastically.
Also respond with links or resources when relevant.
"""


# TODO - more explicit return type
def invoke_agent(query: str, llm: BaseChatModel = DEFAULT_LLM, tools: list[BaseTool] = DEFAULT_TOOLS) -> Any:
    llm_with_tool = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=DEFAULT_SYS_PROMPT),
        HumanMessage(query)
    ]

    ai_msg = llm_with_tool.invoke(messages)

    if not isinstance(ai_msg, AIMessage):
        raise ValueError("Expected AIMessage, got something else")

    print(ai_msg.tool_calls)

    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {t.name: t for t in tools}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    return llm_with_tool.invoke(messages).content
