
from langchain.tools import tool


@tool
def get_project_name() -> str:
    """Return the name of the application."""
    return "LifeOps"
