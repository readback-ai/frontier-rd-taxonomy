"""Text normalization and quote matching.

A quote is verified when it appears in a snapshot's text after both are normalized the same
way. Normalization removes only differences that carry no meaning: Unicode compatibility
forms, typographic quotes and dashes, invisible characters and runs of whitespace. Case and
wording are kept, so a paraphrase never matches.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata

ELLIPSIS = "[...]"

_TRANSLATE = str.maketrans(
    {
        "‘": "'",
        "’": "'",
        "‚": "'",
        "‛": "'",
        "′": "'",
        "“": '"',
        "”": '"',
        "„": '"',
        "‟": '"',
        "″": '"',
        "‐": "-",
        "‑": "-",
        "‒": "-",
        "–": "-",
        "—": "-",
        "―": "-",
        "−": "-",
        " ": " ",
        " ": " ",
        " ": " ",
        " ": " ",
        "­": None,
        "​": None,
        "‌": None,
        "‍": None,
        "⁠": None,
        "﻿": None,
    }
)
_WHITESPACE = re.compile(r"\s+")
# PDF extraction breaks words at line ends ("evalu- ation"); rejoin them on both sides.
_HYPHEN_BREAK = re.compile(r"(?<=[a-z])- (?=[a-z])")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(_TRANSLATE)
    return _WHITESPACE.sub(" ", text).strip()


def _loose(text: str) -> str:
    """Normalized text with line-end hyphenation removed, for PDF text."""
    return _HYPHEN_BREAK.sub("", normalize(text))


def _squash(text: str) -> str:
    """Loose text with every space removed, for PDFs whose extraction drops word spacing."""
    return _loose(text).replace(" ", "")


def quote_segments(quote: str) -> list[str]:
    """The parts of a quote that must each appear, in order. ``[...]`` marks an omission."""
    return [part for part in (normalize(p) for p in quote.split(ELLIPSIS)) if part]


def find_quote(text: str, quote: str) -> list[tuple[int, int]] | None:
    """Positions of each quote segment in ``text``, or None if the quote is not there.

    Segments must appear in order. Matching is tried on normalized text, then with PDF
    line-end hyphenation removed, then with all spacing removed. Positions index the text as
    prepared by the first of those that matches.
    """
    segments = quote_segments(quote)
    if not segments:
        return None
    for prepare in (normalize, _loose, _squash):
        haystack = prepare(text)
        spans: list[tuple[int, int]] = []
        cursor = 0
        for segment in (prepare(s) for s in segments):
            at = haystack.find(segment, cursor)
            if at < 0:
                break
            spans.append((at, at + len(segment)))
            cursor = at + len(segment)
        else:
            return spans
    return None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def quote_hash(quote: str) -> str:
    """Hash of a quote as written in its record. Editing the quote changes it."""
    return sha256_text(quote.strip())
