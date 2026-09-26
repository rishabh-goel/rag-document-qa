from app.documents import chunk_text


def test_chunking_preserves_all_text() -> None:
    text = "alpha " * 200
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert chunks[0].startswith("alpha")
    assert chunks[-1].endswith("alpha")


def test_empty_text_has_no_chunks() -> None:
    assert chunk_text("  \n\t", 100, 20) == []
