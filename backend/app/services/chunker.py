import re
from dataclasses import dataclass

from app.config import settings


@dataclass
class TextChunk:
    content: str
    chunk_index: int
    token_count: int


class TextChunker:
    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> None:
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return len(text.split())

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    def chunk_text(self, text: str) -> list[TextChunk]:
        if not text.strip():
            return []

        sentences = self._split_sentences(text)
        chunks: list[TextChunk] = []
        current_sentences: list[str] = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = self._estimate_tokens(sentence)

            if current_tokens + sentence_tokens > self.chunk_size and current_sentences:
                chunk_text = " ".join(current_sentences)
                chunks.append(
                    TextChunk(
                        content=chunk_text,
                        chunk_index=len(chunks),
                        token_count=current_tokens,
                    )
                )
                # Keep overlap sentences
                overlap_tokens = 0
                overlap_start = len(current_sentences)
                for i in range(len(current_sentences) - 1, -1, -1):
                    st = self._estimate_tokens(current_sentences[i])
                    if overlap_tokens + st > self.chunk_overlap:
                        break
                    overlap_tokens += st
                    overlap_start = i

                current_sentences = current_sentences[overlap_start:]
                current_tokens = sum(self._estimate_tokens(s) for s in current_sentences)

            current_sentences.append(sentence)
            current_tokens += sentence_tokens

        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunks.append(
                TextChunk(
                    content=chunk_text,
                    chunk_index=len(chunks),
                    token_count=current_tokens,
                )
            )

        return chunks
