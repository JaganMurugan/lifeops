
from collections.abc import Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


def build_agent_graph(
    model: BaseChatModel,
    tools: Sequence[BaseTool],
):
    """Build a tool-calling agent workflow."""

    model_with_tools = model.bind_tools(tools)

    def call_model(state: MessagesState):
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(MessagesState)

    builder.add_node("llm", call_model)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "llm")

    builder.add_conditional_edges(
        "llm",
        tools_condition,
    )

    builder.add_edge("tools", "llm")

    return builder.compile()
