from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class IngestedDocument:
    external_id: str
    title: str | None
    doc_type: str
    content: str
    metadata: dict


class BaseIngestor(ABC):
    @abstractmethod
    async def validate_config(self, config: dict) -> bool:
        """Validate source configuration before ingestion."""
        ...

    @abstractmethod
    async def ingest(self, config: dict) -> list[IngestedDocument]:
        """Extract documents from the source. Returns a list of IngestedDocument."""
        ...
