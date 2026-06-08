import json
import logging
import re
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

CHUNK_SIZE = 500
OVERLAP = 100
# Separators tried in order: paragraph → line → sentence → word → character
SEPARATORS = ["\n\n", "\n", ". ", "? ", "! ", " ", ""]

CLEANED_BASE = Path(__file__).resolve().parents[2] / "documents" / "cleaned"
CHUNKS_OUTPUT = Path(__file__).resolve().parents[2] / "documents" / "chunks.json"


# ---------------------------------------------------------------------------
# Block parsing helpers
# ---------------------------------------------------------------------------

def _field(block: str, name: str) -> Optional[str]:
    for line in block.splitlines():
        prefix = f"{name}: "
        if line.startswith(prefix):
            return line[len(prefix):].strip() or None
    return None


def _extract_content(block: str) -> str:
    """Return the main content text from a cleaned block."""
    # Reddit
    m = re.search(r"\nComment Text:\n(.+)", block, re.DOTALL)
    if m:
        return m.group(1).strip()

    # ApartmentRatings — review text, then optional management response
    rv = re.search(r"\nReview Text:\n(.*?)(?=\nManagement Response:|\Z)", block, re.DOTALL)
    mr = re.search(r"\nManagement Response:\n(.+)", block, re.DOTALL)

    parts = []
    if rv:
        t = rv.group(1).strip()
        if t:
            parts.append(t)
    if mr:
        t = mr.group(1).strip()
        if t:
            parts.append("Management Response:\n" + t)

    return "\n\n".join(parts)


def _parse_metadata(block: str) -> dict:
    source = _field(block, "Source") or ""
    is_reddit = source == "Reddit"
    meta: dict = {
        "source_platform": source,
        "source_url": _field(block, "Source URL"),
        "author": _field(block, "Author"),
        "record_type": "reddit_comment" if is_reddit else "apartmentratings_review",
    }
    if is_reddit:
        title = _field(block, "Thread Title")
        meta["document_title"] = title
        meta["thread_title"] = title
        meta["apartment_name"] = None
        meta["rating"] = None
        meta["review_title"] = None
        meta["date"] = _field(block, "Created")
    else:
        prop = _field(block, "Property")
        meta["document_title"] = prop
        meta["apartment_name"] = prop
        meta["thread_title"] = None
        meta["rating"] = _field(block, "Rating")
        meta["review_title"] = _field(block, "Review Title")
        meta["date"] = _field(block, "Date")
    return meta


# ---------------------------------------------------------------------------
# Recursive chunker
# ---------------------------------------------------------------------------

def _joined_len(parts: list, sep: str) -> int:
    if not parts:
        return 0
    return sum(len(p) for p in parts) + len(sep) * (len(parts) - 1)


def _merge(splits: list, sep: str, chunk_size: int, overlap: int) -> list:
    """Merge a flat list of splits into chunks ≤ chunk_size with tail overlap."""
    chunks = []
    buf: list = []

    for split in splits:
        new_len = _joined_len(buf, sep) + (len(sep) if buf else 0) + len(split)
        if new_len > chunk_size and buf:
            chunks.append(sep.join(buf))
            # Retain tail so the next chunk starts with ~overlap chars of context
            while buf and _joined_len(buf, sep) > overlap:
                buf.pop(0)
            # If the retained overlap + sep + split would still overflow, discard overlap
            if buf and _joined_len(buf, sep) + len(sep) + len(split) > chunk_size:
                buf = []
        buf.append(split)

    if buf:
        chunks.append(sep.join(buf))

    return [c.strip() for c in chunks if c.strip()]


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
    _seps: Optional[list] = None,
) -> list:
    if _seps is None:
        _seps = SEPARATORS

    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    # Pick the first separator that actually splits this text
    sep = ""
    tail_seps: list = []
    for i, s in enumerate(_seps):
        if s == "":          # character-level fallback
            sep = s
            break
        if s in text:
            sep = s
            tail_seps = _seps[i + 1:]
            break

    # Character-level fallback: simple sliding window
    if sep == "":
        result = []
        step = max(1, chunk_size - overlap)
        for i in range(0, len(text), step):
            result.append(text[i: i + chunk_size])
        return result

    raw_splits = text.split(sep)

    # Recursively reduce any split that is still > chunk_size
    resolved: list = []
    for s in raw_splits:
        if len(s) > chunk_size and tail_seps:
            resolved.extend(chunk_text(s, chunk_size, overlap, tail_seps))
        else:
            resolved.append(s)

    merged = _merge(resolved, sep, chunk_size, overlap)

    # Hard-cap safety: any chunk still > chunk_size gets a char-level split
    safe: list = []
    step = max(1, chunk_size - overlap)
    for c in merged:
        if len(c) > chunk_size:
            for i in range(0, len(c), step):
                piece = c[i: i + chunk_size]
                if piece.strip():
                    safe.append(piece)
        else:
            safe.append(c)
    return safe


# ---------------------------------------------------------------------------
# Corpus chunking
# ---------------------------------------------------------------------------

def chunk_blocks(blocks: list) -> list:
    all_chunks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        meta = _parse_metadata(block)
        content = _extract_content(block)
        if not content:
            continue
        texts = chunk_text(content)
        for i, text in enumerate(texts):
            entry = dict(meta)
            entry["chunk_index"] = i
            entry["text"] = text
            all_chunks.append(entry)
    return all_chunks


def load_cleaned_files() -> dict:
    files = {}
    for txt_file in sorted(CLEANED_BASE.rglob("*.txt")):
        raw = txt_file.read_text(encoding="utf-8")
        blocks = [b.strip() for b in re.split(r"\n---\n", raw) if b.strip()]
        key = str(txt_file.relative_to(CLEANED_BASE))
        files[key] = blocks
    return files


def run_chunker() -> list:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    file_blocks = load_cleaned_files()
    all_chunks: list = []

    for rel_path, blocks in file_blocks.items():
        chunks = chunk_blocks(blocks)
        all_chunks.extend(chunks)
        logger.info("%s: %d blocks → %d chunks", rel_path, len(blocks), len(chunks))

    logger.info("Total: %d chunks across %d files", len(all_chunks), len(file_blocks))

    CHUNKS_OUTPUT.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    logger.info("Saved → %s", CHUNKS_OUTPUT)

    return all_chunks


if __name__ == "__main__":
    run_chunker()
