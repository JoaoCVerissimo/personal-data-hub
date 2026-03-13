import pytest
from unittest.mock import MagicMock, patch
from httpx import ASGITransport, AsyncClient

from app.main import app


class MockEmbeddingService:
    """Returns deterministic vectors for testing without loading the real model."""

    def embed_text(self, text: str) -> list[float]:
        return [0.1] * 768

    def embed_batch(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        return [[0.1] * 768 for _ in texts]


@pytest.fixture
def mock_embedding_service():
    service = MockEmbeddingService()
    with patch("app.services.embedding.get_embedding_service", return_value=service):
        yield service


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
