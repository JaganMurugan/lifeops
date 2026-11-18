
from datetime import datetime, timezone, timedelta

import pytest
from pydantic import ValidationError

from lifeops.models.meeting import Meeting


def test_create_valid_meeting():
    meeting = Meeting(
        meeting_id="meeting-001",
        title="Project Review",
        start_time=datetime(2026, 11, 19, 10, 0, tzinfo=timezone.utc),
        end_time=datetime(2026, 11, 19, 11, 0, tzinfo=timezone.utc),
        attendees=["alex@example.com"],
    )

    assert meeting.meeting_id == "meeting-001"
    assert meeting.title == "Project Review"
    assert len(meeting.attendees) == 1


def test_meeting_end_time_must_be_after_start_time():
    with pytest.raises(ValidationError):
        Meeting(
            meeting_id="meeting-002",
            title="Invalid Meeting",
            start_time=datetime(2026, 11, 19, 11, 0, tzinfo=timezone.utc),
            end_time=datetime(2026, 11, 19, 10, 0, tzinfo=timezone.utc),
        )


def test_meeting_requires_timezone_aware_datetimes():
    with pytest.raises(ValidationError):
        Meeting(
            meeting_id="meeting-003",
            title="Invalid Meeting",
            start_time=datetime(2026, 11, 19, 10, 0),
            end_time=datetime(2026, 11, 19, 11, 0),
        )


def test_meeting_attendees_default_to_empty_list():
    meeting = Meeting(
        meeting_id="meeting-004",
        title="Team Meeting",
        start_time=datetime(2026, 11, 19, 10, 0, tzinfo=timezone.utc),
        end_time=datetime(2026, 11, 19, 11, 0, tzinfo=timezone.utc),
    )

    assert meeting.attendees == []

    another_meeting = Meeting(
        meeting_id="meeting-005",
        title="Planning Meeting",
        start_time=datetime(2026, 11, 19, 12, 0, tzinfo=timezone.utc),
        end_time=datetime(2026, 11, 19, 13, 0, tzinfo=timezone.utc),
    )

    assert another_meeting.attendees is not meeting.attendees
