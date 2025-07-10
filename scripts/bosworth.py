from langchain_core.tools import tool


from langchain_core.messages import HumanMessage

from langchain_ollama import ChatOllama


def get_llama():
    return ChatOllama(
    model = "llama3.2",
    num_predict = 256,
    # other params ...
)


def invoke_agent(llm, tools, query):
    llm_with_tool = llm.bind_tools(tools)

    messages = [HumanMessage(query)]

    ai_msg = llm_with_tool.invoke(messages)

    print(ai_msg.tool_calls)

    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {t.name: t for t in tools}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    return llm_with_tool.invoke(messages).content


base_llm = get_llama()

@tool
def get_favorite_number() -> int:
    """Returns bosworth's favorite number"""
    return 13

tools = [get_favorite_number]
query = "which number do you like best?"

print(invoke_agent(base_llm, tools, query))
