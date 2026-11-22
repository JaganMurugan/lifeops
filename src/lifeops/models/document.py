
from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class Document(BaseModel):
    """Represents a document available to LifeOps."""

    document_id: str
    title: str = Field(min_length=1)

    content: str = Field(min_length=1)
    source: str = Field(min_length=1)

    tags: list[str] = Field(default_factory=list)
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
