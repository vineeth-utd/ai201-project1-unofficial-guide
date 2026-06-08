import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = ROOT / "documents" / "chroma_db"
COLLECTION_NAME = "apartment_reviews"

_model = None
_collection = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        _collection = client.get_collection(name=COLLECTION_NAME)
    return _collection


def retrieve(query: str, k: int = 5) -> list:
    embedding = _get_model().encode([query])
    results = _get_collection().query(
        query_embeddings=embedding.tolist(),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        }
        for i in range(len(results["documents"][0]))
    ]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

EVAL_QUESTIONS = [
    (
        "Q1",
        "What concerns do residents raise about management at Sentry Tempe?",
        "Expected: poor communication, ignored complaints, slow responses, "
        "unresolved maintenance, lack of urgency.",
    ),
    (
        "Q2",
        "Why do multiple residents recommend avoiding Paseo on University?",
        "Expected: water shutoffs, roach infestations, maintenance problems, "
        "plumbing issues, noisy neighbors, safety concerns, poor management communication.",
    ),
    (
        "Q3",
        "What positive experiences do residents mention about IMT Desert Palm Village?",
        "Expected: quick maintenance responses, helpful leasing staff, smooth move-in, "
        "affordability, friendly customer service.",
    ),
]

RELEVANCE_HINTS = {
    "Q1": ["sentry", "management", "communication", "complaint", "maintenance", "response"],
    "Q2": ["paseo", "water", "roach", "pest", "plumbing", "noise", "unsafe", "avoid"],
    "Q3": ["imt", "desert palm", "maintenance", "leasing", "staff", "move-in", "friendly", "affordable"],
}


def _relevance_label(qid: str, text: str, metadata: dict) -> str:
    hints = RELEVANCE_HINTS[qid]
    combined = (text + " " + metadata.get("apartment_name", "") + " " + metadata.get("thread_title", "")).lower()
    matches = [h for h in hints if h in combined]
    if len(matches) >= 3:
        return "RELEVANT"
    if len(matches) >= 1:
        return "PARTIALLY RELEVANT"
    return "WEAK / OFF-TOPIC"


def main():
    for qid, query, expected in EVAL_QUESTIONS:
        print("=" * 72)
        print(f"QUERY {qid}: {query}")
        print(f"Expected answer: {expected}")
        print("=" * 72)

        results = retrieve(query, k=5)

        for rank, r in enumerate(results, start=1):
            meta = r["metadata"]
            label = _relevance_label(qid, r["text"], meta)
            print(f"\n  Result {rank}  |  distance={r['distance']:.4f}  |  {label}")
            print(f"  Source    : {meta.get('source_platform')} — {meta.get('apartment_name') or meta.get('thread_title') or meta.get('document_title')}")
            print(f"  Author    : {meta.get('author')}  |  Date: {meta.get('date')}  |  Rating: {meta.get('rating') or 'n/a'}")
            print(f"  URL       : {meta.get('source_url')}")
            if meta.get("review_title"):
                print(f"  Review    : {meta.get('review_title')}")
            print(f"  Chunk idx : {meta.get('chunk_index')}")
            print(f"  Text      :\n    {r['text']}")

        print()

    # -------------------------------------------------------------------
    # Retrieval analysis
    # -------------------------------------------------------------------
    print("=" * 72)
    print("RETRIEVAL ANALYSIS")
    print("=" * 72)

    all_results = {qid: retrieve(query, k=5) for qid, query, _ in EVAL_QUESTIONS}

    print("""
Q1 — Management concerns at Sentry Tempe
  Analysis: Chunks should reference Sentry Tempe residents describing management
  failures. If top results are from Sentry Tempe reviews with distance < 0.5,
  retrieval is working. Watch for Reddit chunks that mention Sentry generically
  vs. ApartmentRatings reviews with specific complaints — both are useful.

Q2 — Why avoid Paseo on University
  Analysis: Paseo reviews are complaint-heavy, so distinctive keywords (water
  shutoff, roach, plumbing) should produce tight semantic clusters. Results
  from other apartments mentioning similar problems are partially relevant but
  weaker — check whether apartment_name in metadata confirms the right property.

Q3 — Positive experiences at IMT Desert Palm Village
  Analysis: IMT reviews skew positive in the corpus. If retrieval surface these
  correctly, distances should be the tightest of the three queries since the
  query sentiment matches the review sentiment closely.

Distance score summary:""")

    for qid, query, _ in EVAL_QUESTIONS:
        dists = [r["distance"] for r in all_results[qid]]
        below_half = sum(1 for d in dists if d < 0.5)
        print(f"  {qid}: min={min(dists):.4f}  max={max(dists):.4f}  "
              f"median={sorted(dists)[2]:.4f}  below_0.5={below_half}/5")

    print("""
Top-k = 5 assessment:
  For a corpus of 3213 chunks across 10 sources (5 apartment properties + 5
  Reddit threads), k=5 provides enough diversity to cover multiple reviewers'
  perspectives on the same property without overwhelming the LLM context in
  Milestone 5. k=5 appears appropriate.

Potential failure modes:
  - Chunking: long reviews split at arbitrary boundaries may surface a chunk
    that mentions a property name but lacks the specific complaint — the
    surrounding chunks with the actual details are ranked lower.
  - Embedding quality: all-MiniLM-L6-v2 is a general-purpose model not
    fine-tuned on housing reviews. Highly specific terms (property names,
    local slang) may not cluster as tightly as domain-adapted models would.
  - Top-k: if a property has few reviews, k=5 may pull in off-topic chunks
    from other apartments to fill the result set.

Milestone 5 readiness:
  If Q1/Q2/Q3 each return at least 3 of 5 results from the correct property
  with distances below 0.5, retrieval quality is sufficient to proceed. The
  LLM generation step can discard weakly relevant chunks by grounding answers
  strictly in the retrieved text.""")


if __name__ == "__main__":
    main()
