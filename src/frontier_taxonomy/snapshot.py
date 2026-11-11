"""Snapshots of sources: fetch a page or PDF, keep the raw bytes and the extracted text.

The extracted text is what quotes are verified against. Its hash is committed in the source's
lock file; the snapshot itself stays in ``FRT_DATA_DIR`` (spec section 6).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

from .textnorm import sha256_text

# Says what it is. A site that refuses automated fetches is not worked around: a person
# saves the page and the snapshot is taken from that file (AGENTS.md, "Fetching sources").
USER_AGENT = "research-snapshot/0.1"
TIMEOUT_SECONDS = 60.0
# Text shorter than this from an HTML page usually means a bot wall or a script-rendered page.
MIN_PLAUSIBLE_TEXT = 400


class SnapshotError(RuntimeError):
    """The source could not be fetched or yielded no usable text."""


@dataclass(frozen=True)
class SnapshotMeta:
    source_id: str
    url: str
    final_url: str
    retrieved: str  # ISO date
    method: str  # "http", or "file" for a copy a person saved
    content_type: str
    raw_sha256: str
    text_sha256: str
    text_chars: int


def _is_pdf(raw: bytes, content_type: str) -> bool:
    return raw[:5] == b"%PDF-" or "application/pdf" in content_type.lower()


def extract_text(raw: bytes, content_type: str) -> str:
    """Readable text of an HTML page or a PDF. PDF pages are separated by a page marker."""
    if _is_pdf(raw, content_type):
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(raw))
        pages = []
        for number, page in enumerate(reader.pages, start=1):
            pages.append(f"[page {number}]\n{page.extract_text() or ''}")
        return "\n\n".join(pages).strip()
    if "html" in content_type.lower() or raw.lstrip()[:1] == b"<":
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg", "template", "iframe"]):
            tag.decompose()
        lines = (line.strip() for line in soup.get_text("\n").splitlines())
        return "\n".join(line for line in lines if line)
    return raw.decode("utf-8", errors="replace").strip()


def fetch_http(url: str) -> tuple[bytes, str, str]:
    """Raw bytes, content type and final URL of ``url``, following redirects."""
    try:
        response = httpx.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf,*/*"},
            follow_redirects=True,
            timeout=TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as error:
        raise SnapshotError(f"{url}: {error}") from error
    if response.status_code != 200:
        raise SnapshotError(f"{url}: HTTP {response.status_code}")
    return response.content, response.headers.get("content-type", ""), str(response.url)


def write_snapshot(
    folder: Path,
    source_id: str,
    url: str,
    raw: bytes,
    content_type: str,
    final_url: str,
    method: str,
    retrieved: dt.date | None = None,
) -> SnapshotMeta:
    """Store raw bytes, extracted text and metadata in ``folder``; return the metadata."""
    text = extract_text(raw, content_type)
    if not _is_pdf(raw, content_type) and len(text) < MIN_PLAUSIBLE_TEXT:
        raise SnapshotError(
            f"{url}: only {len(text)} characters of text extracted. The page is probably "
            "script-rendered or refuses automated fetches; have a person save it and use "
            "--from-file."
        )
    folder.mkdir(parents=True, exist_ok=True)
    suffix = "pdf" if _is_pdf(raw, content_type) else "html"
    for stale in folder.glob("raw.*"):
        stale.unlink()
    (folder / f"raw.{suffix}").write_bytes(raw)
    (folder / "text.txt").write_text(text, encoding="utf-8")
    meta = SnapshotMeta(
        source_id=source_id,
        url=url,
        final_url=final_url,
        retrieved=(retrieved or dt.date.today()).isoformat(),
        method=method,
        content_type=content_type,
        raw_sha256=hashlib.sha256(raw).hexdigest(),
        text_sha256=sha256_text(text),
        text_chars=len(text),
    )
    (folder / "meta.json").write_text(json.dumps(asdict(meta), indent=2) + "\n", encoding="utf-8")
    return meta


def snapshot_url(folder: Path, source_id: str, url: str) -> SnapshotMeta:
    raw, content_type, final_url = fetch_http(url)
    return write_snapshot(folder, source_id, url, raw, content_type, final_url, method="http")


def snapshot_file(folder: Path, source_id: str, url: str, path: Path) -> SnapshotMeta:
    """Snapshot a copy of the page or PDF that a person saved, for sources HTTP cannot read."""
    raw = path.read_bytes()
    if raw[:5] == b"%PDF-":
        content_type = "application/pdf"
    elif path.suffix.lower() in (".html", ".htm") or raw.lstrip()[:1] == b"<":
        content_type = "text/html"
    else:
        content_type = "text/plain"
    return write_snapshot(folder, source_id, url, raw, content_type, url, method="file")


def read_snapshot(folder: Path) -> tuple[SnapshotMeta, str] | None:
    """Metadata and text of a stored snapshot, or None if there is none."""
    meta_path, text_path = folder / "meta.json", folder / "text.txt"
    if not (meta_path.is_file() and text_path.is_file()):
        return None
    meta = SnapshotMeta(**json.loads(meta_path.read_text(encoding="utf-8")))
    return meta, text_path.read_text(encoding="utf-8")
