"""Exact English counting and deterministic lexical normalization."""

from __future__ import annotations

import re
from collections.abc import Iterable


_FENCE_OPEN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")
_ATX_HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+|$)")
_SETEXT_HEADING = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
_TABLE_DELIMITER_CELL = re.compile(r"^:?-{3,}:?$")
_INLINE_LINK = re.compile(
    r"(?<!!)\[([^\]\n]+)\]\("
    r"(?:<[^>\n]*>|[^()\s\n]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\)"
)
_REFERENCE_LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\[[^\]\n]*\]")
_REFERENCE_DEFINITION = re.compile(
    r"^ {0,3}\[(?!\^)[^\]\n]+\]:[ \t]*(?:<[^>\n]*>|\S+)"
    r"(?:[ \t]+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?[ \t]*$"
)
_IMAGE = re.compile(
    r"!\[[^\]\n]*\]\((?:<[^>\n]*>|[^()\s\n]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\)"
)
_REFERENCE_IMAGE = re.compile(r"!\[[^\]\n]*\]\[[^\]\n]*\]")
_AUTOLINK = re.compile(r"<(?:https?://|mailto:)[^>\s]+>", re.IGNORECASE)
_BARE_URL = re.compile(
    r"(?<![\w@])(?:https?://|www\.)[^\s<>\])}]+",
    re.IGNORECASE,
)
_FOOTNOTE_REFERENCE = re.compile(r"\[\^[^\]\n]+\]")
_BRACKET_CITATION = re.compile(
    r"\[(?:\d+(?:\s*[,–-]\s*\d+)*|[^\]\n]*[A-Za-z][^\]\n]*\s\d{1,4})\]"
)
_AUTHOR_DATE_CITATION = re.compile(
    r"\([^()\n]*[A-Za-z][^()\n]*,\s*(?:19|20)\d{2}[a-z]?"
    r"(?:,\s*[^()\n]+)?\)"
)
_FOOTNOTE_DEFINITION = re.compile(r"^ {0,3}\[\^[^\]\n]+]:[ \t]*")
_HTML_TAG = re.compile(r"</?[A-Za-z][^>\n]*>")
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_ENGLISH_TOKEN = re.compile(r"[A-Za-z0-9]")
_LEXICAL_TOKEN = re.compile(r"[A-Za-z0-9]+(?:['’_-][A-Za-z0-9]+)*")
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")
_LINE_MARKER = re.compile(
    r"^\s*(?:>{1,3}\s*)?(?:(?:[-+*]|\d+[.)])\s+)?"
)
_TASK_BOX = re.compile(r"^\[(?: |x|X)\][ \t]+")
_MARKDOWN_PUNCTUATION = str.maketrans(
    "",
    "",
    r"\`*_{}[]()#+.!>|~-",
)


def _without_fences(lines: list[str]) -> list[str | None]:
    kept: list[str | None] = []
    fence_character: str | None = None
    fence_length = 0
    for line in lines:
        if fence_character is None:
            match = _FENCE_OPEN.match(line)
            if match is None:
                kept.append(line)
                continue
            marker = match.group("marker")
            fence_character = marker[0]
            fence_length = len(marker)
            kept.append(None)
            continue
        stripped = line.lstrip(" ")
        closing = re.match(
            rf"^{re.escape(fence_character)}{{{fence_length},}}[ \t]*$", stripped
        )
        kept.append(None)
        if closing is not None and len(line) - len(stripped) <= 3:
            fence_character = None
            fence_length = 0
    return kept


def _table_delimiter(line: str) -> bool:
    stripped = line.strip()
    if "|" not in stripped:
        return False
    cells = stripped.strip("|").split("|")
    return len(cells) >= 2 and all(
        _TABLE_DELIMITER_CELL.fullmatch(cell.strip()) is not None for cell in cells
    )


def _table_line_indices(
    lines: list[str | None],
    excluded_headings: set[int],
) -> set[int]:
    excluded: set[int] = set()
    for index, line in enumerate(lines):
        if line is None or not _table_delimiter(line) or index == 0:
            continue
        header = lines[index - 1]
        if header is None or index - 1 in excluded_headings or "|" not in header:
            continue
        excluded.update({index - 1, index})
        following = index + 1
        while following < len(lines):
            candidate = lines[following]
            if candidate is None or "|" not in candidate or not candidate.strip():
                break
            excluded.add(following)
            following += 1
    return excluded


def _without_html_comments(lines: list[str | None]) -> list[str | None]:
    joined = "\n".join("" if line is None else line for line in lines)
    cleaned = _HTML_COMMENT.sub(
        lambda match: "\n" * match.group(0).count("\n"),
        joined,
    ).split("\n")
    return [
        None if original is None else cleaned[index]
        for index, original in enumerate(lines)
    ]


def _included_lines(markdown: str) -> list[str]:
    normalized = markdown.replace("\r\n", "\n").replace("\r", "\n")
    lines = _without_fences(normalized.split("\n"))
    excluded_headings: set[int] = set()
    for index, line in enumerate(lines):
        if line is None:
            continue
        if _ATX_HEADING.match(line):
            excluded_headings.add(index)
        if (
            index + 1 < len(lines)
            and lines[index + 1] is not None
            and line.strip()
            and _SETEXT_HEADING.fullmatch(lines[index + 1]) is not None
        ):
            excluded_headings.update({index, index + 1})
    table_lines = _table_line_indices(lines, excluded_headings)

    transformed: list[str | None] = []
    for index, line in enumerate(lines):
        if line is None or index in table_lines or index in excluded_headings:
            transformed.append(None)
            continue
        if _REFERENCE_DEFINITION.fullmatch(line) is not None:
            transformed.append("")
            continue
        text = line
        text = _IMAGE.sub("", text)
        text = _REFERENCE_IMAGE.sub("", text)
        text = _INLINE_LINK.sub(r"\1", text)
        text = _REFERENCE_LINK.sub(r"\1", text)
        text = _AUTOLINK.sub("", text)
        text = _BARE_URL.sub("", text)
        text = _FOOTNOTE_DEFINITION.sub("", text)
        text = _FOOTNOTE_REFERENCE.sub("", text)
        text = text.replace("↩", "")
        text = _BRACKET_CITATION.sub("", text)
        text = _AUTHOR_DATE_CITATION.sub("", text)
        transformed.append(text)

    prose_lines: list[str] = []
    for line in _without_html_comments(transformed):
        if line is None:
            continue
        text = line
        text = _HTML_TAG.sub("", text)
        text = _LINE_MARKER.sub("", text)
        text = _TASK_BOX.sub("", text)
        prose_lines.append(text)
    return prose_lines


def counted_prose(markdown: str) -> str:
    """Return exactly the prose included by the protocol's English algorithm."""
    return "\n".join(
        line.translate(_MARKDOWN_PUNCTUATION) for line in _included_lines(markdown)
    )


def english_word_tokens(markdown: str) -> tuple[str, ...]:
    """Return counted whitespace tokens containing an English letter or digit."""
    return tuple(
        token
        for token in counted_prose(markdown).split()
        if _ENGLISH_TOKEN.search(token) is not None
    )


def count_english_words(markdown: str) -> int:
    """Count English words using the normative pc-core algorithm."""
    return len(english_word_tokens(markdown))


def normalize_lexical_text(text: str) -> str:
    """Normalize visible prose for exact lexical duplicate comparison."""
    return " ".join(
        token.lower() for token in _LEXICAL_TOKEN.findall(counted_prose(text))
    )


def lexical_units(text: str) -> tuple[str, ...]:
    """Split prose into stable line/sentence units and normalize each unit."""
    units: list[str] = []
    for line in _included_lines(text):
        unmarked = _LINE_MARKER.sub("", line).strip()
        if not unmarked:
            continue
        for sentence in _SENTENCE_BOUNDARY.split(unmarked):
            normalized = normalize_lexical_text(sentence)
            if normalized:
                units.append(normalized)
    return tuple(units)


def lexical_similarity(left: str, right: str) -> float:
    """Return deterministic token-set Jaccard similarity from zero to one."""
    left_tokens = set(left.split())
    right_tokens = set(right.split())
    if not left_tokens and not right_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def unique_in_order(values: Iterable[str]) -> tuple[str, ...]:
    """Return first occurrences while preserving deterministic order."""
    return tuple(dict.fromkeys(values))
