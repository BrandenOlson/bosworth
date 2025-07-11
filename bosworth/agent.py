from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


def get_llama():
    # TODO - auto run `ollama run llama3.2` here rather than in separate shell
    return ChatOllama(
        model="llama3.2",
        temperature=0.2,  # ✅ low temp helps reliability
        top_p=0.9,  # ✅ helps output diversity, lower for more deterministic
        num_predict=512,  # ✅ increase for longer outputs
        stop=["<|eot_id|>"],  # ✅ sometimes needed for Ollama’s internal stopping
    )

DEFAULT_SYS_PROMPT = """You are a helpful finance AI agent named Bosworth.
You are enthusiastic and kind of a nerd, but very lovable.
Respond to every query accurately and enthusiastically.
Also respond with links or resources when relevant.
"""



base_llm = get_llama()

@tool
def get_favorite_number() -> int:
    """Returns bosworth's favorite number"""
    return 13

@tool
def get_bosworth_identity() -> str:
    """Return information about Bosworth, the AI agent, including etymology and more background"""
    return """
    You are Bosworth, the AI agent. 
    You're named after BOS (Branden Olson Steele), friendly neighborhood AI Engineer,
    and creator of the BOS Life blog which covers all sorts of topics in the field of AI Engineering.
    The blog lives at https://brandenolson.github.io
    """


base_tools = [get_favorite_number, get_bosworth_identity]


def invoke_agent(query: str, llm = base_llm, tools = base_tools):
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
