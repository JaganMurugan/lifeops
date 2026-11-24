import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from lifeops.database.connection import get_connection
from lifeops.models.meeting import Meeting


class MeetingRepository:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = db_path

    def add(self, meeting: Meeting) -> None:
        """Persist a meeting in the database."""
        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO meetings (
                    meeting_id,
                    title,
                    start_time,
                    end_time,
                    attendees,
                    description,
                    location,
                    meeting_url
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    meeting.meeting_id,
                    meeting.title,
                    self._to_db_datetime(meeting.start_time),
                    self._to_db_datetime(meeting.end_time),
                    json.dumps(meeting.attendees),
                    meeting.description,
                    meeting.location,
                    meeting.meeting_url,
                ),
            )

    def get_by_id(self, meeting_id: str) -> Meeting | None:
        """Retrieve a meeting by its ID."""
        with get_connection(self.db_path) as connection:
            row = connection.execute(
                "SELECT * FROM meetings WHERE meeting_id = ?",
                (meeting_id,),
            ).fetchone()

        if row is None:
            return None

        return self._to_model(row)

    def list_between(
        self,
        start: datetime,
        end: datetime,
    ) -> list[Meeting]:
        """Return meetings starting within the given time range."""
        if end <= start:
            raise ValueError("end must be after start")

        with get_connection(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM meetings
                WHERE start_time >= ? AND start_time < ?
                ORDER BY start_time
                """,
                (
                    self._to_db_datetime(start),
                    self._to_db_datetime(end),
                ),
            ).fetchall()

        return [self._to_model(row) for row in rows]

    @staticmethod
    def _to_db_datetime(value: datetime) -> str:
        """Normalize a timezone-aware datetime to UTC before storing it."""
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must include timezone information")

        return value.astimezone(timezone.utc).isoformat()

    @staticmethod
    def _to_model(row: sqlite3.Row) -> Meeting:
        """Convert a SQLite row into a validated Meeting object."""
        return Meeting(
            meeting_id=row["meeting_id"],
            title=row["title"],
            start_time=datetime.fromisoformat(row["start_time"]),
            end_time=datetime.fromisoformat(row["end_time"]),
            attendees=json.loads(row["attendees"]),
            description=row["description"],
            location=row["location"],
            meeting_url=row["meeting_url"],
        )