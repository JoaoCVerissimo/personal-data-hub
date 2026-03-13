import logging
from pathlib import Path

import frontmatter

from app.ingestion.base import BaseIngestor, IngestedDocument

logger = logging.getLogger(__name__)


class MarkdownIngestor(BaseIngestor):
    async def validate_config(self, config: dict) -> bool:
        path = config.get("path", "")
        return bool(path) and Path(path).exists()

    async def ingest(self, config: dict) -> list[IngestedDocument]:
        root = Path(config["path"])
        recursive = config.get("recursive", True)
        documents: list[IngestedDocument] = []

        if root.is_file() and root.suffix.lower() == ".md":
            doc = self._process_markdown(root)
            if doc:
                documents.append(doc)
        elif root.is_dir():
            pattern = "**/*.md" if recursive else "*.md"
            for md_path in root.glob(pattern):
                doc = self._process_markdown(md_path)
                if doc:
                    documents.append(doc)

        return documents

    def _process_markdown(self, path: Path) -> IngestedDocument | None:
        try:
            post = frontmatter.load(str(path))
            content = post.content
            if not content.strip():
                return None

            metadata: dict = dict(post.metadata) if post.metadata else {}
            metadata["path"] = str(path)
            metadata["size_bytes"] = path.stat().st_size

            title = (
                metadata.pop("title", None)
                or path.stem.replace("-", " ")
                .replace("_", " ").title()
            )

            return IngestedDocument(
                external_id=f"md:{path}",
                title=title,
                doc_type="markdown",
                content=content,
                metadata=metadata,
            )
        except Exception:
            logger.warning("Failed to parse markdown %s", path)
            return None
