
import sqlite3

import pytest

from lifeops.database.connection import (
    get_connection,
    initialize_database,
)


def test_initialize_database_creates_tables(tmp_path):
    db_path = tmp_path / "lifeops.db"

    initialize_database(db_path)

    with get_connection(db_path) as connection:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    table_names = {row["name"] for row in rows}

    assert {
        "meetings",
        "emails",
        "documents",
        "tasks",
    }.issubset(table_names)


def test_initialize_database_is_idempotent(tmp_path):
    db_path = tmp_path / "lifeops.db"

    initialize_database(db_path)
    initialize_database(db_path)

    with get_connection(db_path) as connection:
        result = connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'"
        ).fetchone()

    assert result[0] == 4


def test_connection_returns_rows_by_column_name(tmp_path):
    db_path = tmp_path / "lifeops.db"
    initialize_database(db_path)

    with get_connection(db_path) as connection:
        connection.execute(
            """
            INSERT INTO meetings (
                meeting_id, title, start_time, end_time
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "meeting-001",
                "Project Review",
                "2026-11-23T10:00:00+00:00",
                "2026-11-23T11:00:00+00:00",
            ),
        )

        row = connection.execute(
            "SELECT * FROM meetings WHERE meeting_id = ?",
            ("meeting-001",),
        ).fetchone()

    assert row["title"] == "Project Review"


def test_foreign_key_constraint_is_enforced(tmp_path):
    db_path = tmp_path / "lifeops.db"
    initialize_database(db_path)

    with pytest.raises(sqlite3.IntegrityError):
        with get_connection(db_path) as connection:
            connection.execute(
                """
                INSERT INTO tasks (
                    task_id, title, source_email_id, created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    "task-001",
                    "Complete API integration",
                    "nonexistent-email",
                    "2026-11-23T10:00:00+00:00",
                ),
            )
