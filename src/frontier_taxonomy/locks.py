"""Lock files: what was snapshotted and which quotes were verified against it.

One JSON file per source in ``data/locks/``, written only by ``taxo snapshot`` and
``taxo verify-quotes``. A quote's stamp names the hash of the quote and of the snapshot text
it was found in, so editing a quote or refreshing a snapshot voids the stamp until the quote
is verified again. Continuous integration reads these files; it never fetches a source.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .config import Paths
from .snapshot import SnapshotMeta


@dataclass(frozen=True)
class QuoteStamp:
    quote_sha256: str
    text_sha256: str
    verified: str  # ISO date


@dataclass
class Lock:
    source_id: str
    snapshot: dict | None = None  # the SnapshotMeta fields, minus source_id
    quotes: dict[str, QuoteStamp] = field(default_factory=dict)

    @property
    def text_sha256(self) -> str | None:
        return self.snapshot.get("text_sha256") if self.snapshot else None


def lock_path(paths: Paths, source_id: str) -> Path:
    return paths.locks / f"{source_id}.json"


def read_lock(paths: Paths, source_id: str) -> Lock:
    path = lock_path(paths, source_id)
    if not path.is_file():
        return Lock(source_id=source_id)
    data = json.loads(path.read_text(encoding="utf-8"))
    return Lock(
        source_id=source_id,
        snapshot=data.get("snapshot"),
        quotes={key: QuoteStamp(**value) for key, value in data.get("quotes", {}).items()},
    )


def write_lock(paths: Paths, lock: Lock) -> Path:
    path = lock_path(paths, lock.source_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "source_id": lock.source_id,
        "snapshot": lock.snapshot,
        "quotes": {key: asdict(lock.quotes[key]) for key in sorted(lock.quotes)},
    }
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return path


def record_snapshot(paths: Paths, meta: SnapshotMeta) -> Lock:
    """Note a new snapshot in the source's lock. Existing quote stamps stay as they are;
    any stamp made against different text no longer counts (see ``stamp_is_current``)."""
    lock = read_lock(paths, meta.source_id)
    snapshot = asdict(meta)
    snapshot.pop("source_id")
    lock.snapshot = snapshot
    write_lock(paths, lock)
    return lock


def stamp_is_current(lock: Lock, evidence_id: str, quote_sha256: str) -> bool:
    stamp = lock.quotes.get(evidence_id)
    return bool(
        stamp
        and lock.text_sha256
        and stamp.quote_sha256 == quote_sha256
        and stamp.text_sha256 == lock.text_sha256
    )
