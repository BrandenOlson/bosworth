from enum import Enum
import sqlite3
from typing import TypedDict, List

from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.messages.tool import ToolCall
from langgraph.graph import StateGraph
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from bosworth.llm import DEFAULT_LLM
from bosworth.tools import DEFAULT_TOOLS


DEFAULT_SYS_PROMPT = """You are a helpful finance AI agent named Bosworth.
You are enthusiastic and kind of a nerd, but very lovable.
Respond to every query accurately and enthusiastically.
Also respond with links or resources when relevant.
"""

tools = DEFAULT_TOOLS
llm = DEFAULT_LLM


class State(TypedDict):
    messages: list[BaseMessage]
    tool_calls: list[ToolCall]


def agent_node(state: State, config: dict) -> State:
    query = config["configurable"]["input"]

    llm_with_tool = llm.bind_tools(tools)

    # Start with existing conversation history (from persisted state)
    messages: list[BaseMessage] = state.get("messages", [])

    if not any(isinstance(m, SystemMessage) for m in messages):
        messages.insert(0, SystemMessage(content=DEFAULT_SYS_PROMPT))

    messages.append(HumanMessage(content=query))
    ai_msg = llm_with_tool.invoke(messages)

    if not isinstance(ai_msg, AIMessage):
        raise ValueError("Expected AIMessage, got something else")

    messages.append(ai_msg)

    # If tool calls are present, handle them
    tool_calls = ai_msg.tool_calls or []
    for tool_call in tool_calls:
        selected_tool = {t.name.lower(): t for t in tools}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    # Final LLM response after tool results
    final_response = llm_with_tool.invoke(messages)
    messages.append(final_response)

    return {"messages": messages, "tool_calls": tool_calls}


class GraphNode(str, Enum):
    AGENT = "agent"


# Build the graph
graph = StateGraph(State)
graph.add_node(GraphNode.AGENT, agent_node)
graph.set_entry_point(GraphNode.AGENT)
graph.set_finish_point(GraphNode.AGENT)


# Create SQLite checkpoint saver
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
checkpointer = SqliteSaver(conn)


# Compile the graph with the checkpoint saver
graph = graph.compile(checkpointer=checkpointer)


class AgentResponse(BaseModel):
    content: str
    tool_calls: list[str]


def invoke_agent(query: str, conversation_id: str) -> AgentResponse:
    config = {
        "configurable": {
            "thread_id": conversation_id,
            "input": query,
        }
    }

    result = graph.invoke(config=config, input={})
    return AgentResponse(
        content=result["messages"][-1].content,
        tool_calls=[tool_call["name"] for tool_call in result["tool_calls"]],
    )
