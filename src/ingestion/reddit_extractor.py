import json
import datetime
import logging

logger = logging.getLogger(__name__)


def _is_deleted(comment_data: dict) -> bool:
    body = comment_data.get("body", "")
    author = comment_data.get("author", "")
    if body in ("[deleted]", "[removed]"):
        return True
    if author in ("[deleted]", "AutoModerator"):
        return True
    if comment_data.get("collapsed_reason_code") == "DELETED":
        return True
    return False


def _format_timestamp(created_utc) -> str | None:
    if created_utc is None:
        return None
    try:
        dt = datetime.datetime.fromtimestamp(float(created_utc), tz=datetime.timezone.utc)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, OSError, OverflowError):
        return None


def _format_post_block(post_data: dict, source_url: str) -> str | None:
    selftext = post_data.get("selftext", "").strip()
    if not selftext or selftext == "[deleted]":
        return None

    title = post_data.get("title", "")
    subreddit = post_data.get("subreddit", "")
    author = post_data.get("author", "[unknown]")
    score = post_data.get("score", 0)
    created = _format_timestamp(post_data.get("created_utc"))

    lines = [
        "Source: Reddit",
        f"Thread Title: {title}",
        f"Subreddit: {subreddit}",
        f"Source URL: {source_url}",
        "",
        f"Author: {author}",
        f"Score: {score}",
    ]
    if created:
        lines.append(f"Created: {created}")
    lines += [
        "",
        "Comment Text:",
        selftext,
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def _format_comment_block(
    comment_data: dict, thread_title: str, subreddit: str, source_url: str
) -> str:
    author = comment_data.get("author", "[unknown]")
    score = comment_data.get("score", 0)
    body = comment_data.get("body", "").strip()
    created = _format_timestamp(comment_data.get("created_utc"))

    lines = [
        "Source: Reddit",
        f"Thread Title: {thread_title}",
        f"Subreddit: {subreddit}",
        f"Source URL: {source_url}",
        "",
        f"Author: {author}",
        f"Score: {score}",
    ]
    if created:
        lines.append(f"Created: {created}")
    lines += [
        "",
        "Comment Text:",
        body,
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def _extract_comments(
    children: list, thread_title: str, subreddit: str, source_url: str
) -> list[str]:
    blocks = []
    for child in children:
        if child.get("kind") != "t1":
            continue
        data = child.get("data", {})
        if _is_deleted(data):
            continue
        blocks.append(_format_comment_block(data, thread_title, subreddit, source_url))
        replies = data.get("replies")
        if isinstance(replies, dict):
            nested = replies.get("data", {}).get("children", [])
            blocks.extend(_extract_comments(nested, thread_title, subreddit, source_url))
    return blocks


def extract_reddit(filepath: str) -> tuple[list[str], dict]:
    with open(filepath, encoding="utf-8") as f:
        raw = json.load(f)

    source_url = raw.get("source_url", "")
    thread_title = raw.get("document_title", "")
    raw_data = raw.get("raw_data", [])

    blocks = []

    # Post body
    try:
        post_data = raw_data[0]["data"]["children"][0]["data"]
        subreddit = post_data.get("subreddit", "")
        post_block = _format_post_block(post_data, source_url)
        if post_block:
            blocks.append(post_block)
    except (IndexError, KeyError) as e:
        logger.warning("Could not extract post data from %s: %s", filepath, e)
        subreddit = ""

    # Comments (raw_data[1+])
    for listing in raw_data[1:]:
        children = listing.get("data", {}).get("children", [])
        blocks.extend(_extract_comments(children, thread_title, subreddit, source_url))

    return blocks, {"total": len(blocks)}
