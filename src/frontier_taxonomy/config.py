"""Where things live: records in the repository, third-party snapshots outside it.

Records (YAML under ``data/``) and lock files are committed. Snapshots of third-party pages
are not: they stay in ``FRT_DATA_DIR``, and only their hashes are committed (spec section 6).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_DATA_DIR = Path.home() / "frontier-rd-taxonomy-data"
ENV_DATA_DIR = "FRT_DATA_DIR"
ENV_REPO_ROOT = "FRT_REPO_ROOT"


def find_repo_root(start: Path | None = None) -> Path:
    """The nearest folder at or above ``start`` that holds ``data/`` and ``pyproject.toml``."""
    override = os.environ.get(ENV_REPO_ROOT)
    if override:
        return Path(override).expanduser().resolve()
    here = (start or Path.cwd()).resolve()
    for folder in (here, *here.parents):
        if (folder / "pyproject.toml").is_file() and (folder / "data").is_dir():
            return folder
    raise FileNotFoundError(
        f"No repository root found at or above {here}. Run from inside the repository or set "
        f"{ENV_REPO_ROOT}."
    )


@dataclass(frozen=True)
class Paths:
    root: Path
    data_dir: Path

    @classmethod
    def discover(cls, root: Path | None = None, data_dir: Path | None = None) -> Paths:
        root = (root or find_repo_root()).resolve()
        if data_dir is None:
            data_dir = Path(os.environ.get(ENV_DATA_DIR, DEFAULT_DATA_DIR)).expanduser()
        return cls(root=root, data_dir=data_dir.resolve())

    @property
    def records(self) -> Path:
        return self.root / "data"

    @property
    def locks(self) -> Path:
        return self.records / "locks"

    @property
    def reports(self) -> Path:
        return self.root / "reports"

    @property
    def snapshots(self) -> Path:
        return self.data_dir / "snapshots"

    def snapshot_dir(self, source_id: str) -> Path:
        return self.snapshots / source_id
