import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from src.embedding.retriever import retrieve

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

SYSTEM_PROMPT = """You are a housing information assistant for students searching for off-campus apartments near Arizona State University (Tempe campus).

You must follow these rules without exception:
1. Answer ONLY from the retrieved context provided in the user message. Do not use your general training knowledge.
2. Do not invent apartments, facts, prices, or explanations that are not present in the context.
3. If the retrieved context does not contain enough information to answer the question, respond with exactly: "I don't have enough information on that."
4. Keep your answer concise and evidence-based. Reference specific details from the context when possible.
5. Do not speculate or fill in gaps with assumptions."""


def _build_context(chunks: list) -> str:
    lines = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk["metadata"]
        source = meta.get("apartment_name") or meta.get("document_title") or "Unknown"
        platform = meta.get("source_platform", "Unknown")
        author = meta.get("author", "Unknown")
        date = meta.get("date", "Unknown")
        rating = meta.get("rating")
        header = f"[{i}] Source: {platform} — {source} | Author: {author} | Date: {date}"
        if rating:
            header += f" | Rating: {rating}"
        lines.append(header)
        lines.append(chunk["text"])
        lines.append("")
    return "\n".join(lines)


def _build_sources(chunks: list) -> list:
    sources = []
    seen = set()
    for chunk in chunks:
        meta = chunk["metadata"]
        name = meta.get("apartment_name") or meta.get("document_title") or ""
        platform = meta.get("source_platform", "")
        url = meta.get("source_url", "")
        chunk_idx = meta.get("chunk_index")
        label = f"{platform} — {name}"
        if url:
            label += f" ({url})"
        if chunk_idx is not None:
            label += f" [chunk {chunk_idx}]"
        if label not in seen:
            sources.append(label)
            seen.add(label)
    return sources


def generate(query: str) -> dict:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY is not set.", file=sys.stderr)
        return {
            "answer": "Configuration error: GROQ_API_KEY is not set. Please check your .env file.",
            "sources": [],
            "retrieved_chunks": [],
        }

    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}", file=sys.stderr)
        return {
            "answer": "Failed to initialize the language model client. Please check your API key.",
            "sources": [],
            "retrieved_chunks": [],
        }

    try:
        chunks = retrieve(query, k=5)
    except RuntimeError as e:
        print(f"Retrieval error: {e}", file=sys.stderr)
        return {
            "answer": str(e),
            "sources": [],
            "retrieved_chunks": [],
        }

    context = _build_context(chunks)
    sources = _build_sources(chunks)
    user_message = f"Retrieved context:\n{context}\nQuestion: {query}"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0,
        )
        answer = response.choices[0].message.content
    except Exception as e:
        print(f"Groq API error: {e}", file=sys.stderr)
        return {
            "answer": "The language model request failed. Please try again.",
            "sources": sources,
            "retrieved_chunks": chunks,
        }

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": chunks,
    }
