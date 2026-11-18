
from langchain_core.messages import HumanMessage, ToolMessage

from lifeops.providers.llm.factory import get_chat_model
from lifeops.tools.diagnostic_tools import get_project_name


model = get_chat_model()
model_with_tools = model.bind_tools([get_project_name])

# Step 1: Send the user's request
messages = [
    HumanMessage(
        content="Use the get_project_name tool to find the project name. "
        "Do not guess the answer."
    )
]

response = model_with_tools.invoke(messages)

# Step 2: Inspect the requested tool calls
print("Requested tool calls:", response.tool_calls)

# Step 3: Execute the requested tools
messages.append(response)

for tool_call in response.tool_calls:
    if tool_call["name"] == get_project_name.name:
        result = get_project_name.invoke(tool_call["args"])

        print("Tool execution result:", result)

        # Step 4: Return the result to the conversation
        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
                name=tool_call["name"],
            )
        )

# Step 5: Ask the model to produce its final response
final_response = model_with_tools.invoke(messages)

print("\nFinal response:", final_response.content)
