import argparse
import json
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHUNKS_PATH = ROOT / "documents" / "chunks.json"
CHROMA_PATH = ROOT / "documents" / "chroma_db"
COLLECTION_NAME = "apartment_reviews"
BATCH_SIZE = 500

METADATA_FIELDS = [
    "source_platform",
    "source_url",
    "author",
    "record_type",
    "document_title",
    "apartment_name",
    "thread_title",
    "rating",
    "review_title",
    "date",
    "chunk_index",
]


def load_chunks():
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        return json.load(f)


def build_metadata(chunk):
    meta = {}
    for field in METADATA_FIELDS:
        val = chunk.get(field)
        if val is None:
            meta[field] = ""
        else:
            meta[field] = val
    return meta


def run():
    chunks = load_chunks()
    print(f"Total chunks loaded: {len(chunks)}")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)
    print(f"Total embeddings generated: {len(embeddings)}")

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    # Delete existing collection to ensure a clean rebuild
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(name=COLLECTION_NAME)

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [build_metadata(c) for c in chunks]

    for start in range(0, len(chunks), BATCH_SIZE):
        end = min(start + BATCH_SIZE, len(chunks))
        collection.add(
            ids=ids[start:end],
            embeddings=embeddings[start:end].tolist(),
            documents=texts[start:end],
            metadatas=metadatas[start:end],
        )

    total = collection.count()
    print(f"Total records inserted into ChromaDB: {total}")

    print("\n--- ChromaDB folder structure ---")
    print(f"  {CHROMA_PATH}/")
    for p in sorted(CHROMA_PATH.rglob("*")):
        print(f"    {p.relative_to(CHROMA_PATH)}")

    print("\n--- Sample record (chunk_0) ---")
    sample = collection.get(ids=["chunk_0"], include=["documents", "metadatas"])
    print(f"Text:\n  {sample['documents'][0]}")
    print("Metadata:")
    for k, v in sample["metadatas"][0].items():
        print(f"  {k}: {v!r}")


if __name__ == "__main__":
    run()
