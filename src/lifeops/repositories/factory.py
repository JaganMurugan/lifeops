from dataclasses import dataclass
from pathlib import Path

from lifeops.database.connection import initialize_database
from lifeops.repositories.document_repository import DocumentRepository
from lifeops.repositories.email_repository import EmailRepository
from lifeops.repositories.meeting_repository import MeetingRepository
from lifeops.repositories.task_repository import TaskRepository


@dataclass(frozen=True)
class RepositoryContainer:
    meetings: MeetingRepository
    emails: EmailRepository
    documents: DocumentRepository
    tasks: TaskRepository


def create_repositories(db_path: str | Path) -> RepositoryContainer:
    """Initialize the database and create all repositories."""
    initialize_database(db_path)

    return RepositoryContainer(
        meetings=MeetingRepository(db_path),
        emails=EmailRepository(db_path),
        documents=DocumentRepository(db_path),
        tasks=TaskRepository(db_path),
    )