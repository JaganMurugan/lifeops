import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path

from lifeops.database.connection import get_connection
from lifeops.models.task import Task


class TaskRepository:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = db_path

    def add(self, task: Task) -> None:
        """Persist a task in the database."""
        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO tasks (
                    task_id,
                    title,
                    description,
                    owner,
                    due_date,
                    status,
                    source_email_id,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task.task_id,
                    task.title,
                    task.description,
                    task.owner,
                    task.due_date.isoformat() if task.due_date else None,
                    task.status,
                    task.source_email_id,
                    self._to_db_datetime(task.created_at),
                ),
            )

    def get_by_id(self, task_id: str) -> Task | None:
        """Retrieve a task by its ID."""
        with get_connection(self.db_path) as connection:
            row = connection.execute(
                "SELECT * FROM tasks WHERE task_id = ?",
                (task_id,),
            ).fetchone()

        if row is None:
            return None

        return self._to_model(row)

    def list_by_status(self, status: str) -> list[Task]:
        """Retrieve tasks with the specified status."""
        with get_connection(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM tasks
                WHERE status = ?
                ORDER BY created_at DESC
                """,
                (status,),
            ).fetchall()

        return [self._to_model(row) for row in rows]

    def list_open_due_by(self, cutoff_date: date) -> list[Task]:
        """Retrieve pending or in-progress tasks due on or before a date."""
        with get_connection(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM tasks
                WHERE status IN ('pending', 'in_progress')
                  AND due_date IS NOT NULL
                  AND due_date <= ?
                ORDER BY due_date ASC
                """,
                (cutoff_date.isoformat(),),
            ).fetchall()

        return [self._to_model(row) for row in rows]

    @staticmethod
    def _to_db_datetime(value: datetime) -> str:
        """Normalize a timezone-aware datetime to UTC before storing it."""
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must include timezone information")

        return value.astimezone(timezone.utc).isoformat()

    @staticmethod
    def _to_model(row: sqlite3.Row) -> Task:
        """Convert a SQLite row into a validated Task object."""
        return Task(
            task_id=row["task_id"],
            title=row["title"],
            description=row["description"],
            owner=row["owner"],
            due_date=date.fromisoformat(row["due_date"])
            if row["due_date"]
            else None,
            status=row["status"],
            source_email_id=row["source_email_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )