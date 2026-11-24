from datetime import datetime, timezone

import pytest

from lifeops.database.connection import initialize_database
from lifeops.models.meeting import Meeting
from lifeops.repositories.meeting_repository import MeetingRepository


@pytest.fixture
def repository(tmp_path):
    db_path = tmp_path / "lifeops.db"
    initialize_database(db_path)
    return MeetingRepository(db_path)


def make_meeting(
    meeting_id: str,
    title: str,
    start_time: datetime,
) -> Meeting:
    return Meeting(
        meeting_id=meeting_id,
        title=title,
        start_time=start_time,
        end_time=datetime.fromtimestamp(
            start_time.timestamp() + 3600,
            tz=timezone.utc,
        ),
        attendees=["alex@example.com", "sam@example.com"],
        description="Project discussion",
        location="Meeting Room A",
        meeting_url="https://example.com/meeting",
    )


def test_add_and_get_meeting(repository):
    start = datetime(2026, 11, 24, 10, 0, tzinfo=timezone.utc)
    meeting = make_meeting("meeting-001", "Project Review", start)

    repository.add(meeting)
    retrieved = repository.get_by_id("meeting-001")

    assert retrieved is not None
    assert retrieved.meeting_id == meeting.meeting_id
    assert retrieved.title == meeting.title
    assert retrieved.attendees == meeting.attendees
    assert retrieved.start_time == meeting.start_time
    assert retrieved.end_time == meeting.end_time


def test_get_by_id_returns_none_for_missing_meeting(repository):
    result = repository.get_by_id("does-not-exist")

    assert result is None


def test_list_between_returns_meetings_in_time_range(repository):
    meeting_1 = make_meeting(
        "meeting-001",
        "Morning Review",
        datetime(2026, 11, 24, 9, 0, tzinfo=timezone.utc),
    )
    meeting_2 = make_meeting(
        "meeting-002",
        "Afternoon Review",
        datetime(2026, 11, 24, 14, 0, tzinfo=timezone.utc),
    )
    meeting_3 = make_meeting(
        "meeting-003",
        "Next Day Review",
        datetime(2026, 11, 25, 9, 0, tzinfo=timezone.utc),
    )

    repository.add(meeting_1)
    repository.add(meeting_2)
    repository.add(meeting_3)

    results = repository.list_between(
        start=datetime(2026, 11, 24, 8, 0, tzinfo=timezone.utc),
        end=datetime(2026, 11, 25, 0, 0, tzinfo=timezone.utc),
    )

    assert len(results) == 2
    assert [meeting.meeting_id for meeting in results] == [
        "meeting-001",
        "meeting-002",
    ]


def test_list_between_rejects_invalid_time_range(repository):
    with pytest.raises(ValueError, match="end must be after start"):
        repository.list_between(
            start=datetime(2026, 11, 25, 10, 0, tzinfo=timezone.utc),
            end=datetime(2026, 11, 24, 10, 0, tzinfo=timezone.utc),
        )