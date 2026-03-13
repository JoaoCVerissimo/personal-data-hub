from app.services.chunker import TextChunker


def test_chunk_empty_text():
    chunker = TextChunker(chunk_size=100, chunk_overlap=10)
    result = chunker.chunk_text("")
    assert result == []


def test_chunk_short_text():
    chunker = TextChunker(chunk_size=100, chunk_overlap=10)
    result = chunker.chunk_text("Hello world. This is a test.")
    assert len(result) == 1
    assert result[0].chunk_index == 0
    assert "Hello world" in result[0].content


def test_chunk_splits_long_text():
    chunker = TextChunker(chunk_size=10, chunk_overlap=2)
    text = ". ".join(f"Sentence number {i}" for i in range(20))
    result = chunker.chunk_text(text)
    assert len(result) > 1
    for i, chunk in enumerate(result):
        assert chunk.chunk_index == i
        assert chunk.token_count > 0


def test_chunk_indices_sequential():
    chunker = TextChunker(chunk_size=5, chunk_overlap=1)
    text = "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence."
    result = chunker.chunk_text(text)
    for i, chunk in enumerate(result):
        assert chunk.chunk_index == i
