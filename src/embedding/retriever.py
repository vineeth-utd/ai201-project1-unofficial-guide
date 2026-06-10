import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = ROOT / "documents" / "chroma_db"
COLLECTION_NAME = "apartment_reviews"

KNOWN_PROPERTIES = [
    "IMT Desert Palm Village",
    "Murietta at ASU",
    "Onnix",
    "Paseo on University",
    "Sentry Tempe",
    "Park Place",
    "Vertex",
    "Olive",
    "Union Tempe",
    "Redpoint",
    "Emerson",
    "The Hyve",
    "University House",
    "Volta at Broadway",
    "Alight",
    "University Valley",
    "University Pointe",
    "Skye",
    "Agave",
    "Apollo",
    "Canvas"
]
# Subtracted from L2 distance for chunks that match the queried property.
# Chosen to exceed the observed gap (~0.26) between on-property and off-property
# chunks so on-property results reliably rank above off-property ones.
PROPERTY_BOOST = 0.3

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
        if not CHROMA_PATH.exists():
            raise RuntimeError(
                f"ChromaDB not found at {CHROMA_PATH}. "
                "Run `python3 src/embedding/vectorstore.py` to build the vector store."
            )
        try:
            client = chromadb.PersistentClient(path=str(CHROMA_PATH))
            _collection = client.get_collection(name=COLLECTION_NAME)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load ChromaDB collection '{COLLECTION_NAME}': {e}\n"
                "If the collection is missing or corrupted, run `python3 src/embedding/vectorstore.py --rebuild`."
            ) from e
    return _collection


def _semantic_retrieve(query: str, k: int) -> list:
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
            "boosted": False,
        }
        for i in range(len(results["documents"][0]))
    ]


def _detect_property(query: str) -> str | None:
    q = query.lower()
    for name in KNOWN_PROPERTIES:
        if name.lower() in q:
            return name
    return None


def _property_matches(result: dict, property_name: str) -> bool:
    meta = result["metadata"]
    name_lower = property_name.lower()
    if meta.get("source_platform") == "ApartmentRatings":
        return meta.get("apartment_name", "").lower() == name_lower
    # Reddit chunks have no apartment_name metadata; scan the text instead.
    return name_lower in result["text"].lower()


def retrieve(query: str, k: int = 5) -> list:
    """Return top-k chunks for query. Applies property-aware reranking when the
    query names a known apartment property."""
    raw = _semantic_retrieve(query, k=10)

    property_name = _detect_property(query)
    if property_name is None:
        return raw[:k]

    for r in raw:
        if _property_matches(r, property_name):
            r["boosted"] = True
            r["_sort_key"] = r["distance"] - PROPERTY_BOOST
        else:
            r["_sort_key"] = r["distance"]

    reranked = sorted(raw, key=lambda r: r["_sort_key"])
    for r in reranked:
        del r["_sort_key"]
    return reranked[:k]
