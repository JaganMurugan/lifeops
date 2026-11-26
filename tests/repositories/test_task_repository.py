from datetime import date, datetime, timezone

import pytest

from lifeops.database.connection import initialize_database
from lifeops.models.task import Task
from lifeops.repositories.task_repository import TaskRepository


@pytest.fixture
def repository(tmp_path):
    db_path = tmp_path / "lifeops.db"
    initialize_database(db_path)
    return TaskRepository(db_path)


def make_task(
    task_id: str,
    title: str,
    status: str = "pending",
    due_date: date | None = None,
) -> Task:
    return Task(
        task_id=task_id,
        title=title,
        description="Project action item",
        owner="alex@example.com",
        due_date=due_date,
        status=status,
        created_at=datetime(
            2026, 11, 23, 10, 0, tzinfo=timezone.utc
        ),
    )


def test_add_and_get_task(repository):
    task = make_task(
        "task-001",
        "Complete API integration",
        status="in_progress",
        due_date=date(2026, 11, 25),
    )

    repository.add(task)
    retrieved = repository.get_by_id("task-001")

    assert retrieved is not None
    assert retrieved.task_id == task.task_id
    assert retrieved.title == task.title
    assert retrieved.status == task.status
    assert retrieved.due_date == task.due_date
    assert retrieved.owner == task.owner


def test_get_by_id_returns_none_for_missing_task(repository):
    result = repository.get_by_id("does-not-exist")

    assert result is None


def test_list_by_status_returns_matching_tasks(repository):
    repository.add(make_task("task-001", "Task one", "pending"))
    repository.add(make_task("task-002", "Task two", "in_progress"))
    repository.add(make_task("task-003", "Task three", "pending"))

    results = repository.list_by_status("pending")

    assert len(results) == 2
    assert {task.task_id for task in results} == {
        "task-001",
        "task-003",
    }


def test_list_open_due_by_returns_outstanding_due_tasks(repository):
    repository.add(
        make_task(
            "task-001",
            "Overdue task",
            "pending",
            date(2026, 11, 24),
        )
    )
    repository.add(
        make_task(
            "task-002",
            "Due today task",
            "in_progress",
            date(2026, 11, 26),
        )
    )
    repository.add(
        make_task(
            "task-003",
            "Future task",
            "pending",
            date(2026, 11, 28),
        )
    )
    repository.add(
        make_task(
            "task-004",
            "Completed task",
            "completed",
            date(2026, 11, 24),
        )
    )
    repository.add(
        make_task(
            "task-005",
            "Task without due date",
            "pending",
        )
    )

    results = repository.list_open_due_by(date(2026, 11, 26))

    assert len(results) == 2
    assert {task.task_id for task in results} == {
        "task-001",
        "task-002",
    }