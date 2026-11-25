import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from lifeops.database.connection import get_connection
from lifeops.models.document import Document

class DocumentRepository:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = db_path

    def add(self, document: Document) -> None:
        """Persist a document in the database."""
        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO documents (
                    document_id,
                    title,
                    content,
                    source,
                    tags,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    document.document_id,
                    document.title,
                    document.content,
                    document.source,
                    json.dumps(document.tags),
                    self._to_db_datetime(document.created_at),
                ),
            )

    def get_by_id(self, document_id: str) -> Document | None:
        """Retrieve a document by its ID."""
        with get_connection(self.db_path) as connection:
            row = connection.execute(
                "SELECT * FROM documents WHERE document_id = ?",
                (document_id,),
            ).fetchone()

        if row is None:
            return None

        return self._to_model(row)

    def search_by_tag(self, tag: str) -> list[Document]:
        """Retrieve documents containing the specified tag."""
        with get_connection(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM documents
                WHERE EXISTS (
                    SELECT 1
                    FROM json_each(documents.tags)
                    WHERE json_each.value = ?
                )
                ORDER BY created_at DESC
                """,
                (tag,),
            ).fetchall()

        return [self._to_model(row) for row in rows]

    @staticmethod
    def _to_db_datetime(value: datetime) -> str:
        """Normalize a timezone-aware datetime to UTC before storing it."""
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must include timezone information")

        return value.astimezone(timezone.utc).isoformat()

    @staticmethod
    def _to_model(row: sqlite3.Row) -> Document:
        """Convert a SQLite row into a validated Document object."""
        return Document(
            document_id=row["document_id"],
            title=row["title"],
            content=row["content"],
            source=row["source"],
            tags=json.loads(row["tags"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )