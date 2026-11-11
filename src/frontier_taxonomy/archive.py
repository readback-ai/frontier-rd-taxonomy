"""Packing snapshots for storage outside the session, and restoring them.

Snapshots live outside git and a cloud session's disk does not last. ``taxo pack-snapshots``
writes one archive of the snapshots behind recorded sources, to be kept in the organization's
private storage (spec decision D15). ``taxo restore-snapshots`` unpacks one and checks each
snapshot's text against the hash in its lock file, so a restored snapshot is known to be the
text the quotes were verified against.
"""

from __future__ import annotations

import tarfile
from dataclasses import dataclass
from pathlib import Path

from .config import Paths
from .locks import read_lock
from .store import load
from .textnorm import sha256_text

TEXT_FILES = ("meta.json", "text.txt")


def _members(folder: Path, include_raw: bool) -> list[Path]:
    files = [folder / name for name in TEXT_FILES if (folder / name).is_file()]
    if include_raw:
        files += sorted(folder.glob("raw.*"))
    return files


def pack_snapshots(paths: Paths, out: Path, include_raw: bool = True) -> list[str]:
    """Write an archive of the snapshots of every recorded source. Returns the source ids
    packed. Sources with no snapshot on disk are left out; the caller can compare the lists.

    ``include_raw=False`` keeps only the extracted text and its metadata, which is all that
    quote verification reads and a small fraction of the size.
    """
    packed: list[str] = []
    out.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(out, "w:gz") as archive:
        for source_id in sorted(load(paths).sources):
            folder = paths.snapshot_dir(source_id)
            files = _members(folder, include_raw)
            if not (folder / "text.txt").is_file():
                continue
            for file in files:
                archive.add(file, arcname=f"snapshots/{source_id}/{file.name}")
            packed.append(source_id)
    return packed


@dataclass(frozen=True)
class Restored:
    source_id: str
    status: str  # matches | differs | no_lock


def _safe(name: str) -> bool:
    """Only ``snapshots/<source id>/<file>``: nothing absolute, nested or pointing upward."""
    parts = Path(name).parts
    return (
        len(parts) == 3
        and parts[0] == "snapshots"
        and parts[1].startswith("S-")
        and ".." not in parts
        and (parts[2] in TEXT_FILES or parts[2].startswith("raw."))
    )


def restore_snapshots(paths: Paths, archive_path: Path) -> list[Restored]:
    """Unpack an archive into the snapshot folder and compare each text with its lock.

    ``matches`` means the restored text is the text the source's quotes were verified
    against. ``differs`` means it is some other capture: the quotes need verifying again.
    """
    with tarfile.open(archive_path, "r:*") as archive:
        members = archive.getmembers()
        unsafe = [m.name for m in members if not (m.isfile() and _safe(m.name))]
        if unsafe:
            raise ValueError(f"refusing to unpack unexpected entries: {', '.join(unsafe[:5])}")
        paths.snapshots.parent.mkdir(parents=True, exist_ok=True)
        archive.extractall(paths.snapshots.parent, members=members, filter="data")
    results = []
    for source_id in sorted({Path(m.name).parts[1] for m in members}):
        text = (paths.snapshot_dir(source_id) / "text.txt").read_text(encoding="utf-8")
        expected = read_lock(paths, source_id).text_sha256
        if expected is None:
            status = "no_lock"
        else:
            status = "matches" if sha256_text(text) == expected else "differs"
        results.append(Restored(source_id, status))
    return results
