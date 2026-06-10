import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.generation.generator import generate


EVAL_QUERIES = [
    (
        "V1 (ApartmentRatings)",
        "What concerns do residents raise about management at Sentry Tempe?",
    ),
    (
        "V2 (Reddit)",
        "What do ASU students on Reddit say about apartments to avoid near campus?",
    ),
    (
        "V3 (Out-of-scope)",
        "What is the average rent for a one-bedroom apartment in downtown Phoenix?",
    ),
]


def main():
    for label, query in EVAL_QUERIES:
        print("=" * 72)
        print(f"TEST {label}")
        print(f"QUERY: {query}")
        print("=" * 72)

        result = generate(query)

        print("\n--- Retrieved Chunks ---")
        for i, chunk in enumerate(result["retrieved_chunks"], 1):
            meta = chunk["metadata"]
            source = meta.get("apartment_name") or meta.get("document_title") or "Unknown"
            platform = meta.get("source_platform", "")
            boosted = " [BOOSTED]" if chunk.get("boosted") else ""
            print(f"  {i}. dist={chunk['distance']:.4f}{boosted}  {platform} — {source}")
            print(f"     {chunk['text'][:120].replace(chr(10), ' ')}")

        print("\n--- Answer ---")
        print(result["answer"])

        print("\n--- Sources ---")
        for s in result["sources"]:
            print(f"  • {s}")

        print()


if __name__ == "__main__":
    main()
