
from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class Meeting(BaseModel):
    """Represents a calendar meeting."""

    meeting_id: str
    title: str = Field(min_length=1)

    start_time: datetime
    end_time: datetime

    attendees: list[str] = Field(default_factory=list)

    description: str | None = None
    location: str | None = None
    meeting_url: str | None = None

    @model_validator(mode="after")
    def validate_meeting_times(self):
        if self.start_time.tzinfo is None or self.start_time.utcoffset() is None:
            raise ValueError("start_time must include timezone information")

        if self.end_time.tzinfo is None or self.end_time.utcoffset() is None:
            raise ValueError("end_time must include timezone information")

        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")

        return self
