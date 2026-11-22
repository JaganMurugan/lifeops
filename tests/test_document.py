
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from lifeops.models.document import Document


def test_create_valid_document():
    document = Document(
        document_id="doc-001",
        title="Project Architecture",
        content="This document describes the project architecture.",
        source="project_architecture.md",
        tags=["architecture", "project"],
        created_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
    )

    assert document.document_id == "doc-001"
    assert document.title == "Project Architecture"
    assert document.source == "project_architecture.md"
    assert "architecture" in document.tags


def test_document_requires_timezone_aware_created_at():
    with pytest.raises(ValidationError):
        Document(
            document_id="doc-002",
            title="Project Plan",
            content="Project plan details.",
            source="project_plan.md",
            created_at=datetime(2026, 11, 22, 10, 0),
        )


def test_document_title_cannot_be_empty():
    with pytest.raises(ValidationError):
        Document(
            document_id="doc-003",
            title="",
            content="Some content.",
            source="notes.md",
            created_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
        )


def test_document_tags_default_to_empty_list():
    document = Document(
        document_id="doc-004",
        title="Meeting Notes",
        content="Discussion about project progress.",
        source="meeting_notes.md",
        created_at=datetime(2026, 11, 22, 10, 0, tzinfo=timezone.utc),
    )

    assert document.tags == []

    another_document = Document(
        document_id="doc-005",
        title="Technical Notes",
        content="Technical implementation details.",
        source="technical_notes.md",
        created_at=datetime(2026, 11, 22, 11, 0, tzinfo=timezone.utc),
    )

    assert document.tags is not another_document.tags
