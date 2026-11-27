from datetime import datetime, timezone

from lifeops.models.meeting import Meeting
from lifeops.repositories.document_repository import DocumentRepository
from lifeops.repositories.email_repository import EmailRepository
from lifeops.repositories.factory import (
    RepositoryContainer,
    create_repositories,
)
from lifeops.repositories.meeting_repository import MeetingRepository
from lifeops.repositories.task_repository import TaskRepository


def test_create_repositories_returns_all_repositories(tmp_path):
    db_path = tmp_path / "lifeops.db"

    repositories = create_repositories(db_path)

    assert isinstance(repositories, RepositoryContainer)
    assert isinstance(repositories.meetings, MeetingRepository)
    assert isinstance(repositories.emails, EmailRepository)
    assert isinstance(repositories.documents, DocumentRepository)
    assert isinstance(repositories.tasks, TaskRepository)
    assert db_path.exists()


def test_repositories_share_the_same_database(tmp_path):
    db_path = tmp_path / "lifeops.db"

    repositories = create_repositories(db_path)

    meeting = Meeting(
        meeting_id="meeting-001",
        title="Project Review",
        start_time=datetime(
            2026, 11, 27, 10, 0, tzinfo=timezone.utc
        ),
        end_time=datetime(
            2026, 11, 27, 11, 0, tzinfo=timezone.utc
        ),
        attendees=["alex@example.com"],
    )

    repositories.meetings.add(meeting)

    # Create another container using the same database.
    another_container = create_repositories(db_path)

    retrieved = another_container.meetings.get_by_id("meeting-001")

    assert retrieved is not None
    assert retrieved.title == "Project Review"