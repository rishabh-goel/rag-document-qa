from __future__ import annotations

from openai import OpenAI

from app.config import settings


def answer_question(question: str, chunks: list[dict]) -> str:
    if not chunks:
        return "I couldn’t find anything relevant in the indexed documents."
    if settings.llm_provider.lower() == "none":
        return "LLM generation is disabled. The most relevant passage is:\n\n" + chunks[0]["text"]
    if settings.llm_provider.lower() != "openai":
        raise ValueError("LLM_PROVIDER must be 'openai' or 'none'.")
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured. Set it in .env, or use LLM_PROVIDER=none.")

    context = "\n\n".join(
        f"[Source {index + 1}: {chunk['metadata']['filename']}, page {chunk['metadata'].get('page') or 'n/a'}]\n{chunk['text']}"
        for index, chunk in enumerate(chunks)
    )
    instructions = (
        "You answer questions using only the supplied document context. "
        "If the context is insufficient, say exactly that you could not find the answer in the indexed documents. "
        "Be concise. Cite factual claims with [Source N]. Do not invent citations."
    )
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.create(
        model=settings.openai_model,
        instructions=instructions,
        input=f"Question: {question}\n\nDocument context:\n{context}",
    )
    return response.output_text.strip()
