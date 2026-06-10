import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.embedding.retriever import retrieve, _semantic_retrieve, _detect_property, _property_matches


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


def _source_label(result: dict) -> str:
    meta = result["metadata"]
    name = meta.get("apartment_name") or meta.get("document_title") or ""
    platform = meta.get("source_platform", "")
    return f"{platform} — {name}"


def main():
    for qid, query, expected in EVAL_QUESTIONS:
        print("=" * 72)
        print(f"QUERY {qid}: {query}")
        print(f"Expected: {expected}")
        print("=" * 72)

        # --- Stage 1: top-10 semantic results ---
        semantic_top10 = _semantic_retrieve(query, k=10)
        detected = _detect_property(query)

        print(f"\nDetected property: {detected!r}")
        print(f"\nStage 1 — Top 10 semantic results:")
        for i, r in enumerate(semantic_top10, 1):
            boost_flag = ""
            if detected and _property_matches(r, detected):
                boost_flag = "  [WILL BOOST]"
            print(f"  {i:2d}. dist={r['distance']:.4f}{boost_flag}  {_source_label(r)}")
            print(f"      {r['text'][:100].replace(chr(10), ' ')}")

        # --- Stage 2: reranked top-5 ---
        final = retrieve(query, k=5)

        # Determine before/after property match counts
        prop_before = sum(
            1 for r in semantic_top10[:5]
            if detected and _property_matches(r, detected)
        )
        prop_after = sum(
            1 for r in final
            if detected and _property_matches(r, detected)
        )

        print(f"\nStage 2 — Final top 5 after reranking (property matches: {prop_before}/5 → {prop_after}/5):")
        for rank, r in enumerate(final, 1):
            boost_tag = " [BOOSTED]" if r["boosted"] else ""
            meta = r["metadata"]
            print(f"\n  Result {rank}  |  dist={r['distance']:.4f}{boost_tag}")
            print(f"  Source    : {_source_label(r)}")
            print(f"  Author    : {meta.get('author')}  |  Date: {meta.get('date')}  |  Rating: {meta.get('rating') or 'n/a'}")
            if meta.get("review_title"):
                print(f"  Review    : {meta.get('review_title')}")
            print(f"  Chunk idx : {meta.get('chunk_index')}")
            print(f"  Text      :\n    {r['text']}")

        # Per-query comparison commentary
        print()
        if prop_after > prop_before:
            print(f"  >> Improvement: {prop_before}/5 → {prop_after}/5 on-property chunks in final results.")
        elif prop_after == prop_before:
            print(f"  >> No change in on-property count ({prop_before}/5). Reranking did not alter top-5 for this query.")
        else:
            print(f"  >> Regression: {prop_before}/5 → {prop_after}/5. Check PROPERTY_BOOST value.")
        print()


if __name__ == "__main__":
    main()
