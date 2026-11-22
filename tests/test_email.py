from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from lifeops.models.email import Email

def test_create_valid_email():
    email = Email(
        email_id="email-001",
        thread_id="thread-001",
        subject="Project Review",
        sender="alex@example.com",
        recipients=["jagan@example.com"],
        sent_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
        body="Please review the project updates"
    )

    assert email.email_id == "email-001"
    assert email.thread_id == "thread-001"
    assert email.subject == "Project Review"

def test_email_requires_timezone_aware_sent_at():
    with pytest.raises(ValidationError):
        Email(
            email_id="email-002",
            thread_id="thread-001",
            subject="Project Review",
            sender="alex@example.com",
            sent_at=datetime(2026, 11, 22, 10, 0),
            body="Project update.",
        )

def test_email_subject_cannot_be_empty():
    with pytest.raises(ValidationError):
        Email(
            email_id="email-003",
            thread_id="thread-001",
            subject="",
            sender="alex@example.com",
            sent_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
            body="Project update.",
        )

def test_email_recipients_default_to_empty_list():
    email = Email(
        email_id="email-004",
        thread_id="thread-001",
        subject="Project Review",
        sender="alex@example.com",
        sent_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
        body="Project update.",
    )

    assert email.recipients == []