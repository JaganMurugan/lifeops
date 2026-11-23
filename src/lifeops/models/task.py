
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class Task(BaseModel):
    """Represents an actionable task in LifeOps."""

    task_id: str
    title: str = Field(min_length=1)

    description: str | None = None
    owner: str | None = None

    due_date: date | None = None

    status: Literal[
        "pending",
        "in_progress",
        "completed",
        "cancelled",
    ] = "pending"

    source_email_id: str | None = None
    created_at: datetime

    @model_validator(mode="after")
    def validate_created_at(self):
        if (
            self.created_at.tzinfo is None
            or self.created_at.utcoffset() is None
        ):
            raise ValueError(
                "created_at must include timezone information"
            )

        return self
