import tempfile
from pathlib import Path

import pytest

from app.ingestion.markdown_ingestor import MarkdownIngestor


@pytest.mark.asyncio
async def test_ingest_markdown_with_frontmatter():
    with tempfile.TemporaryDirectory() as tmpdir:
        md_content = """---
title: My Note
tags: [python, testing]
---

# My Note

This is the content of my note.
"""
        (Path(tmpdir) / "note.md").write_text(md_content)

        ingestor = MarkdownIngestor()
        documents = await ingestor.ingest({"path": tmpdir})

        assert len(documents) == 1
        doc = documents[0]
        assert doc.title == "My Note"
        assert doc.doc_type == "markdown"
        assert "content of my note" in doc.content
        assert doc.metadata.get("tags") == ["python", "testing"]


@pytest.mark.asyncio
async def test_ingest_markdown_without_frontmatter():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "simple-note.md").write_text("# Simple\n\nJust text.")

        ingestor = MarkdownIngestor()
        documents = await ingestor.ingest({"path": tmpdir})

        assert len(documents) == 1
        assert documents[0].title == "Simple Note"
