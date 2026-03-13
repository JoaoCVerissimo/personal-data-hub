import logging
from pathlib import Path

from app.ingestion.base import BaseIngestor, IngestedDocument

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".md", ".rst", ".csv"}


class DocumentIngestor(BaseIngestor):
    async def validate_config(self, config: dict) -> bool:
        path = config.get("path", "")
        return bool(path) and Path(path).exists()

    async def ingest(self, config: dict) -> list[IngestedDocument]:
        root = Path(config["path"])
        extensions = config.get("extensions", list(SUPPORTED_EXTENSIONS))
        recursive = config.get("recursive", True)
        documents: list[IngestedDocument] = []

        if root.is_file():
            doc = self._process_file(root)
            if doc:
                documents.append(doc)
        elif root.is_dir():
            pattern = "**/*" if recursive else "*"
            for file_path in root.glob(pattern):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    doc = self._process_file(file_path)
                    if doc:
                        documents.append(doc)

        return documents

    def _process_file(self, path: Path) -> IngestedDocument | None:
        try:
            if path.suffix.lower() == ".pdf":
                return self._read_pdf(path)
            else:
                return self._read_text(path)
        except Exception:
            logger.warning("Failed to read %s", path)
            return None

    def _read_text(self, path: Path) -> IngestedDocument | None:
        content = path.read_text(encoding="utf-8", errors="replace")
        if not content.strip():
            return None
        return IngestedDocument(
            external_id=f"file:{path}",
            title=path.name,
            doc_type="text" if path.suffix != ".md" else "markdown",
            content=content,
            metadata={
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "extension": path.suffix,
            },
        )

    def _read_pdf(self, path: Path) -> IngestedDocument | None:
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(str(path))
            pages: list[str] = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
            content = "\n\n".join(pages)
            if not content.strip():
                return None
            return IngestedDocument(
                external_id=f"pdf:{path}",
                title=path.name,
                doc_type="pdf",
                content=content,
                metadata={
                    "path": str(path),
                    "size_bytes": path.stat().st_size,
                    "page_count": len(reader.pages),
                },
            )
        except ImportError:
            logger.warning("PyPDF2 not installed, skipping PDF %s", path)
            return None
