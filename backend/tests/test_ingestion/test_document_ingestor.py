import tempfile
from pathlib import Path

import pytest

from app.ingestion.document_ingestor import DocumentIngestor


@pytest.mark.asyncio
async def test_validate_config_missing_path():
    ingestor = DocumentIngestor()
    assert await ingestor.validate_config({}) is False


@pytest.mark.asyncio
async def test_validate_config_valid():
    with tempfile.TemporaryDirectory() as tmpdir:
        ingestor = DocumentIngestor()
        assert await ingestor.validate_config({"path": tmpdir}) is True


@pytest.mark.asyncio
async def test_ingest_text_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        (Path(tmpdir) / "test1.txt").write_text("Hello world content")
        (Path(tmpdir) / "test2.md").write_text("# Markdown\n\nSome content here")
        (Path(tmpdir) / "ignored.bin").write_bytes(b"\x00\x01\x02")

        ingestor = DocumentIngestor()
        documents = await ingestor.ingest({"path": tmpdir})

        assert len(documents) == 2
        titles = {d.title for d in documents}
        assert "test1.txt" in titles
        assert "test2.md" in titles


@pytest.mark.asyncio
async def test_ingest_empty_file_skipped():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "empty.txt").write_text("")
        ingestor = DocumentIngestor()
        documents = await ingestor.ingest({"path": tmpdir})
        assert len(documents) == 0
