from datetime import datetime

from pydantic import BaseModel, Field, model_validator

class Email(BaseModel):
    """Represents an individual email message."""

    email_id: str
    thread_id: str

    subject: str = Field(min_length=1)
    sender: str = Field(min_length=1)
    recipients: list[str] = Field(default_factory=list)

    sent_at: datetime

    body: str

    @model_validator(mode="after")
    def validate_sent_at(self):
        if self.sent_at.tzinfo is None or self.sent_at.utcoffset() is None:
            raise ValueError("sent_at must include timezone information")

        return self
    
