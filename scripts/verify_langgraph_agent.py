from langchain_core.messages import HumanMessage

from lifeops.agents.graph import build_agent_graph
from lifeops.providers.llm.factory import get_chat_model
from lifeops.tools.diagnostic_tools import get_project_name


model = get_chat_model()

agent = build_agent_graph(
    model=model,
    tools=[get_project_name],
)

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Use the get_project_name tool to find "
                    "the project name. Do not guess."
                )
            )
        ]
    }
)

for message in result["messages"]:
    message.pretty_print()