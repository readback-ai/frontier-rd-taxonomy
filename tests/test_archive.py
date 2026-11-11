"""Snapshots survive a round trip through an archive, and a changed one is caught."""

from __future__ import annotations

import io
import shutil
import tarfile

import pytest
from conftest import SOURCE

from frontier_taxonomy.archive import pack_snapshots, restore_snapshots
from frontier_taxonomy.config import Paths
from frontier_taxonomy.validate import validate
from frontier_taxonomy.verify import verify_quotes


def test_pack_and_restore_round_trip(verified: Paths, tmp_path):
    archive = tmp_path / "pack.tar.gz"
    assert pack_snapshots(verified, archive) == [SOURCE["id"]]
    shutil.rmtree(verified.snapshots)
    results = restore_snapshots(verified, archive)
    assert [(r.source_id, r.status) for r in results] == [(SOURCE["id"], "matches")]
    assert {r.status for r in verify_quotes(verified)} == {"verified"}
    assert [p for p in validate(verified) if p.level == "error"] == []


def test_text_only_pack_is_enough_to_verify(verified: Paths, tmp_path):
    archive = tmp_path / "text.tar.gz"
    pack_snapshots(verified, archive, include_raw=False)
    with tarfile.open(archive) as packed:
        names = sorted(packed.getnames())
    assert names == [f"snapshots/{SOURCE['id']}/meta.json", f"snapshots/{SOURCE['id']}/text.txt"]
    shutil.rmtree(verified.snapshots)
    assert restore_snapshots(verified, archive)[0].status == "matches"
    assert {r.status for r in verify_quotes(verified)} == {"verified"}


def test_a_restored_snapshot_that_differs_from_its_lock_is_reported(verified: Paths, tmp_path):
    text = verified.snapshot_dir(SOURCE["id"]) / "text.txt"
    text.write_text(text.read_text() + " A sentence added after the quotes were verified.")
    archive = tmp_path / "pack.tar.gz"
    pack_snapshots(verified, archive)
    assert restore_snapshots(verified, archive)[0].status == "differs"


def test_an_archive_that_reaches_outside_the_snapshot_folder_is_refused(verified: Paths, tmp_path):
    archive = tmp_path / "bad.tar.gz"
    with tarfile.open(archive, "w:gz") as bad:
        payload = b"overwritten"
        entry = tarfile.TarInfo("snapshots/../../pyproject.toml")
        entry.size = len(payload)
        bad.addfile(entry, io.BytesIO(payload))
    with pytest.raises(ValueError, match="refusing"):
        restore_snapshots(verified, archive)
