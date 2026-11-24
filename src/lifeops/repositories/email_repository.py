import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from lifeops.database.connection import get_connection
from lifeops.models.email import Email


class EmailRepository:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = db_path

    def add(self, email: Email) -> None:
        """Persist an email in the database."""
        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO emails (
                    email_id,
                    thread_id,
                    subject,
                    sender,
                    recipients,
                    sent_at,
                    body
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    email.email_id,
                    email.thread_id,
                    email.subject,
                    email.sender,
                    json.dumps(email.recipients),
                    self._to_db_datetime(email.sent_at),
                    email.body,
                ),
            )

    def get_by_id(self, email_id: str) -> Email | None:
        """Retrieve an email by its ID."""
        with get_connection(self.db_path) as connection:
            row = connection.execute(
                "SELECT * FROM emails WHERE email_id = ?",
                (email_id,),
            ).fetchone()

        if row is None:
            return None

        return self._to_model(row)

    def list_by_thread_id(self, thread_id: str) -> list[Email]:
        """Retrieve all emails in a thread, ordered oldest to newest."""
        with get_connection(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM emails
                WHERE thread_id = ?
                ORDER BY sent_at ASC
                """,
                (thread_id,),
            ).fetchall()

        return [self._to_model(row) for row in rows]

    @staticmethod
    def _to_db_datetime(value: datetime) -> str:
        """Normalize a timezone-aware datetime to UTC before storing it."""
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must include timezone information")

        return value.astimezone(timezone.utc).isoformat()

    @staticmethod
    def _to_model(row: sqlite3.Row) -> Email:
        """Convert a SQLite row into a validated Email object."""
        return Email(
            email_id=row["email_id"],
            thread_id=row["thread_id"],
            subject=row["subject"],
            sender=row["sender"],
            recipients=json.loads(row["recipients"]),
            sent_at=datetime.fromisoformat(row["sent_at"]),
            body=row["body"],
        )