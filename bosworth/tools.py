from langchain_core.tools import tool, BaseTool


@tool
def get_favorite_number() -> int:
    """Returns bosworth's favorite number"""
    return 13


@tool
def get_bosworth_identity() -> str:
    """Return information about Bosworth, the AI agent, including etymology and more background"""
    return """
    You are Bosworth, a friendly, nerdy, lovable AI agent. 
    You're named after BOS (Branden Olson Steele), friendly neighborhood AI Engineer,
    and creator of the BOS Life blog which covers all sorts of topics in the field of AI Engineering.
    The blog lives at https://brandenolson.github.io
    """


DEFAULT_TOOLS: list[BaseTool] = [get_favorite_number, get_bosworth_identity]
