import logging
from pathlib import Path

from src.ingestion.reddit_extractor import extract_reddit
from src.ingestion.apartmentratings_extractor import extract_apartmentratings

RAW_BASE = Path(__file__).resolve().parents[2] / "documents" / "raw"
CLEANED_BASE = Path(__file__).resolve().parents[2] / "documents" / "cleaned"

logger = logging.getLogger(__name__)

_EXTRACTORS = {
    "reddit": extract_reddit,
    "apartmentratings": extract_apartmentratings,
}


def _discover_files() -> list[tuple[Path, str]]:
    found = []
    for json_file in sorted(RAW_BASE.rglob("*.json")):
        source_type = json_file.parent.name
        found.append((json_file, source_type))
    return found


def _get_output_path(raw_path: Path) -> Path:
    relative = raw_path.relative_to(RAW_BASE)
    return CLEANED_BASE / relative.with_suffix(".txt")


def _write_output(output_path: Path, blocks: list[str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(blocks), encoding="utf-8")


def run_pipeline() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    files = _discover_files()
    if not files:
        logger.warning("No JSON files found under %s", RAW_BASE)
        return

    for raw_path, source_type in files:
        extractor = _EXTRACTORS.get(source_type)
        if extractor is None:
            logger.warning("No extractor for source type '%s' — skipping %s", source_type, raw_path.name)
            continue

        try:
            blocks, stats = extractor(str(raw_path))
        except Exception as e:
            logger.error("Failed to process %s: %s", raw_path.name, e)
            continue

        output_path = _get_output_path(raw_path)
        _write_output(output_path, blocks)

        skipped_msg = f", skipped {stats['skipped']}" if "skipped" in stats else ""
        logger.info(
            "%s: extracted %d blocks%s → %s",
            raw_path.name,
            stats["total"],
            skipped_msg,
            output_path,
        )


if __name__ == "__main__":
    run_pipeline()
