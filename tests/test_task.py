
from datetime import date, datetime, timezone

import pytest
from pydantic import ValidationError

from lifeops.models.task import Task


def test_create_valid_task():
    task = Task(
        task_id="task-001",
        title="Complete API integration",
        description="Integrate the project APIs.",
        owner="alex@example.com",
        due_date=date(2026, 11, 25),
        status="in_progress",
        source_email_id="email-001",
        created_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
      )

    assert task.task_id == "task-001"
    assert task.title == "Complete API integration"
    assert task.status == "in_progress"
    assert task.source_email_id == "email-001"


def test_task_status_defaults_to_pending():
    task = Task(
        task_id="task-002",
        title="Review project documentation",
        created_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
    )

    assert task.status == "pending"


def test_invalid_task_status_is_rejected():
    with pytest.raises(ValidationError):
        Task(
            task_id="task-003",
            title="Review project documentation",
            status="started",
            created_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
        )


def test_task_title_cannot_be_empty():
    with pytest.raises(ValidationError):
        Task(
            task_id="task-004",
            title="",
            created_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
        )


def test_task_requires_timezone_aware_created_at():
    with pytest.raises(ValidationError):
        Task(
            task_id="task-005",
            title="Complete API integration",
            created_at=datetime(2026, 11, 22, 10, 0),
        )
