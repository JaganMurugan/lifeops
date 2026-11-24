from datetime import datetime, timezone

import pytest

from lifeops.database.connection import initialize_database
from lifeops.models.email import Email
from lifeops.repositories.email_repository import EmailRepository


@pytest.fixture
def repository(tmp_path):
    db_path = tmp_path / "lifeops.db"
    initialize_database(db_path)
    return EmailRepository(db_path)


def make_email(
    email_id: str,
    thread_id: str,
    sent_at: datetime,
    subject: str = "Project Alpha",
) -> Email:
    return Email(
        email_id=email_id,
        thread_id=thread_id,
        subject=subject,
        sender="alex@example.com",
        recipients=["sam@example.com"],
        sent_at=sent_at,
        body="Let's discuss the project update.",
    )


def test_add_and_get_email(repository):
    email = make_email(
        "email-001",
        "thread-001",
        datetime(2026, 11, 23, 10, 0, tzinfo=timezone.utc),
    )

    repository.add(email)
    retrieved = repository.get_by_id("email-001")

    assert retrieved is not None
    assert retrieved.email_id == email.email_id
    assert retrieved.thread_id == email.thread_id
    assert retrieved.subject == email.subject
    assert retrieved.recipients == email.recipients
    assert retrieved.sent_at == email.sent_at
    assert retrieved.body == email.body


def test_get_by_id_returns_none_for_missing_email(repository):
    result = repository.get_by_id("does-not-exist")

    assert result is None


def test_list_by_thread_id_returns_emails_in_chronological_order(
    repository,
):
    later_email = make_email(
        "email-002",
        "thread-001",
        datetime(2026, 11, 23, 14, 0, tzinfo=timezone.utc),
    )
    earlier_email = make_email(
        "email-001",
        "thread-001",
        datetime(2026, 11, 23, 10, 0, tzinfo=timezone.utc),
    )
    unrelated_email = make_email(
        "email-003",
        "thread-002",
        datetime(2026, 11, 23, 12, 0, tzinfo=timezone.utc),
    )

    repository.add(later_email)
    repository.add(unrelated_email)
    repository.add(earlier_email)

    results = repository.list_by_thread_id("thread-001")

    assert len(results) == 2
    assert [email.email_id for email in results] == [
        "email-001",
        "email-002",
    ]


def test_list_by_thread_id_returns_empty_list_for_unknown_thread(
    repository,
):
    results = repository.list_by_thread_id("unknown-thread")

    assert results == []