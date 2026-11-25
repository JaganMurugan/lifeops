from datetime import datetime, timezone

import pytest

from lifeops.database.connection import initialize_database
from lifeops.models.document import Document
from lifeops.repositories.document_repository import DocumentRepository

@pytest.fixture
def repository(tmp_path):
    db_path = tmp_path / "lifeops.db"
    initialize_database(db_path)
    return DocumentRepository(db_path)

def make_document(
    document_id: str,
    title: str,
    tags: list[str],
) -> Document:
    return Document(
        document_id=document_id,
        title=title,
        content="This document contains project information.",
        source="project-alpha/architecture.md",
        tags=tags,
        created_at=datetime(
            2026, 11, 23, 10, 0, tzinfo=timezone.utc
        ),
    )

def test_add_and_get_document(repository):
    document = make_document(
        "doc-001",
        "Project Architecture",
        ["project-alpha", "architecture"],
    )

    repository.add(document)
    retrieved = repository.get_by_id("doc-001")

    assert retrieved is not None
    assert retrieved.document_id == document.document_id
    assert retrieved.title == document.title
    assert retrieved.content == document.content
    assert retrieved.source == document.source
    assert retrieved.tags == document.tags
    assert retrieved.created_at == document.created_at

def test_get_by_id_returns_none_for_missing_document(repository):
    result = repository.get_by_id("does-not-exist")

    assert result is None

def test_search_by_tag_returns_matching_documents(repository):
    document_1 = make_document(
        "doc-001",
        "Project Architecture",
        ["project-alpha", "architecture"],
    )
    document_2 = make_document(
        "doc-002",
        "Project Requirements",
        ["project-alpha", "requirements"],
    )
    document_3 = make_document(
        "doc-003",
        "Personal Notes",
        ["personal", "notes"],
    )

    repository.add(document_1)
    repository.add(document_2)
    repository.add(document_3)

    results = repository.search_by_tag("project-alpha")

    assert len(results) == 2
    assert {document.document_id for document in results} == {
        "doc-001",
        "doc-002",
    }

def test_search_by_tag_returns_empty_list_when_no_match(repository):
    results = repository.search_by_tag("unknown-tag")

    assert results == []