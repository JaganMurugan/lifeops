from langchain_core.messages import AIMessage, ToolMessage

from lifeops.agents.graph import build_agent_graph
from lifeops.tools.diagnostic_tools import get_project_name


class FakeChatModel:
    """A deterministic model for testing agent orchestration."""

    def __init__(self):
        self.call_count = 0

    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        self.call_count += 1

        if self.call_count == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "get_project_name",
                        "args": {},
                        "id": "test-call-1",
                        "type": "tool_call",
                    }
                ],
            )

        return AIMessage(content="The project name is LifeOps.")


def test_agent_executes_tool_and_returns_final_response():
    model = FakeChatModel()

    agent = build_agent_graph(
        model=model,
        tools=[get_project_name],
    )

    result = agent.invoke(
        {
            "messages": [
                ("user", "What is the project name?")
            ]
        }
    )

    messages = result["messages"]

    # The model should be called twice:
    # once to request the tool and once to produce the final answer.
    assert model.call_count == 2

    # Verify that the tool was executed.
    tool_messages = [
        message
        for message in messages
        if isinstance(message, ToolMessage)
    ]

    assert len(tool_messages) == 1
    assert tool_messages[0].content == "LifeOps"

    # Verify the final response.
    assert messages[-1].content == "The project name is LifeOps."