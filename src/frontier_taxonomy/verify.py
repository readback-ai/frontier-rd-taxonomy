"""Verify evidence quotes against snapshots and stamp the ones that are there."""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass

import yaml
from pydantic import ValidationError

from .config import Paths
from .locks import QuoteStamp, read_lock, write_lock
from .schema import Source
from .snapshot import read_snapshot
from .textnorm import find_quote, quote_hash


@dataclass(frozen=True)
class QuoteResult:
    evidence_id: str
    source_id: str
    status: str  # "verified", "not_found", "no_snapshot" or "invalid_record"
    detail: str = ""


def _read_source(paths: Paths, source_id: str) -> Source:
    path = paths.records / "sources" / f"{source_id}.yml"
    with open(path, encoding="utf-8") as handle:
        return Source.model_validate(yaml.safe_load(handle))


def verify_quotes(
    paths: Paths, source_ids: list[str] | None = None, today: dt.date | None = None
) -> list[QuoteResult]:
    """Check each quote of the chosen sources (default all) against its source's snapshot.

    A found quote gets a stamp in the source's lock file. A quote that is not found loses any
    stamp it had. Sources with no local snapshot are left untouched: their stamps can only be
    confirmed where the snapshot is. Each source file is read on its own, so one invalid
    record does not stop the others.
    """
    if source_ids is None:
        source_ids = sorted(p.stem for p in (paths.records / "sources").glob("*.yml"))
    stamp_date = (today or dt.date.today()).isoformat()
    results: list[QuoteResult] = []
    for source_id in source_ids:
        try:
            source = _read_source(paths, source_id)
        except (OSError, yaml.YAMLError, ValidationError) as error:
            results.append(QuoteResult("", source_id, "invalid_record", str(error)))
            continue
        stored = read_snapshot(paths.snapshot_dir(source_id))
        if stored is None:
            results.extend(QuoteResult(e.id, source_id, "no_snapshot") for e in source.evidence)
            continue
        meta, text = stored
        lock = read_lock(paths, source_id)
        if lock.text_sha256 != meta.text_sha256:
            lock.snapshot = {k: v for k, v in asdict(meta).items() if k != "source_id"}
        kept: dict[str, QuoteStamp] = {}
        for item in source.evidence:
            if find_quote(text, item.quote) is None:
                results.append(QuoteResult(item.id, source_id, "not_found"))
                continue
            digest = quote_hash(item.quote)
            previous = lock.quotes.get(item.id)
            if (
                previous
                and previous.quote_sha256 == digest
                and previous.text_sha256 == meta.text_sha256
            ):
                kept[item.id] = previous
            else:
                kept[item.id] = QuoteStamp(digest, meta.text_sha256, stamp_date)
            results.append(QuoteResult(item.id, source_id, "verified"))
        lock.quotes = kept
        write_lock(paths, lock)
    return results
