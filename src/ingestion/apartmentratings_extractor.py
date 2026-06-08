import html
import json
import logging

logger = logging.getLogger(__name__)


def _parse_date(date_obj: dict | None) -> str:
    if not date_obj or not isinstance(date_obj, dict):
        return "unknown"
    try:
        year = 1900 + int(date_obj["year"])
        month = int(date_obj["month"]) + 1  # 0-indexed in source
        day = int(date_obj["date"])
        return f"{year}-{month:02d}-{day:02d}"
    except (KeyError, TypeError, ValueError):
        return "unknown"


def _fix_encoding(text: str) -> str:
    # Raw data was scraped with UTF-8 bytes decoded as Windows-1252 (e.g. â€™ → ')
    try:
        return text.encode("windows-1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def _format_rating(rating) -> str:
    if rating is None:
        return "N/A"
    try:
        f = float(rating)
        return str(int(f)) if f == int(f) else str(f)
    except (TypeError, ValueError):
        return str(rating)


def _format_review_block(review: dict, property_name: str, source_url: str) -> str | None:
    strings = review.get("strings", {})
    booleans = review.get("booleans", {})

    if booleans.get("is_review_banished_b", False):
        return None

    raw_text = strings.get("review_text_s", "")
    review_text = _fix_encoding(html.unescape(raw_text)).strip()
    if not review_text:
        return None

    rating = _format_rating(review.get("floats", {}).get("rating_overall_f"))
    review_title = strings.get("review_title_s", "")
    author = strings.get("author_s", "Unknown")
    date = _parse_date(review.get("objectCreateDate"))

    lines = [
        "Source: ApartmentRatings",
        f"Property: {property_name}",
        f"Source URL: {source_url}",
        "",
        f"Rating: {rating}",
        f"Review Title: {review_title}",
        f"Author: {author}",
        f"Date: {date}",
        "",
        "Review Text:",
        review_text,
    ]

    raw_response = strings.get("response_text_s")
    if raw_response:
        response_text = _fix_encoding(html.unescape(raw_response)).strip()
        if response_text:
            lines += [
                "",
                "Management Response:",
                response_text,
            ]

    lines += ["", "---", ""]
    return "\n".join(lines)


def extract_apartmentratings(filepath: str) -> tuple[list[str], dict]:
    with open(filepath, encoding="utf-8") as f:
        raw = json.load(f)

    property_name = raw.get("property_name", raw.get("document_title", ""))
    source_url = raw.get("source_url", "")
    reviews_list = raw.get("raw_data", {}).get("reviews", [])

    blocks = []
    skipped = 0

    for review_wrapper in reviews_list:
        if not review_wrapper:
            continue
        review = review_wrapper[0]
        block = _format_review_block(review, property_name, source_url)
        if block:
            blocks.append(block)
        else:
            skipped += 1

    return blocks, {"total": len(blocks), "skipped": skipped}
