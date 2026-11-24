
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from collections.abc import Iterator


@contextmanager
def get_connection(
    db_path: str | Path,
) -> Iterator[sqlite3.Connection]:
    """Create and manage a SQLite database connection."""

    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database(db_path: str | Path) -> None:
    """Create database tables and indexes if they don't exist."""

    schema_path = Path(__file__).with_name("schema.sql")
    schema = schema_path.read_text(encoding="utf-8")

    with get_connection(db_path) as connection:
        connection.executescript(schema)
