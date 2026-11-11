import json

import pytest
from conftest import PAGE, SOURCE, write_record

from frontier_taxonomy import cli
from frontier_taxonomy.config import ENV_DATA_DIR, ENV_REPO_ROOT, Paths
from frontier_taxonomy.locks import lock_path, read_lock
from frontier_taxonomy.validate import validate


@pytest.fixture
def repo(paths: Paths, monkeypatch) -> Paths:
    """The test repository, as the command line finds it."""
    monkeypatch.setenv(ENV_REPO_ROOT, str(paths.root))
    monkeypatch.setenv(ENV_DATA_DIR, str(paths.data_dir))
    return paths


def saved_page(repo: Paths):
    page = repo.root / "saved.html"
    page.write_text(PAGE, encoding="utf-8")
    return page


def test_snapshot_of_a_source_with_no_record_leaves_no_lock(repo: Paths, capsys):
    page = saved_page(repo)
    code = cli.main(
        ["snapshot", "S-not-added", "--url", "https://example.org/x", "--from-file", str(page)]
    )
    assert code == 0
    assert (repo.snapshot_dir("S-not-added") / "text.txt").is_file()
    assert not lock_path(repo, "S-not-added").exists()


def test_snapshot_then_verify_writes_the_lock(repo: Paths, capsys):
    page = saved_page(repo)
    assert cli.main(["snapshot", SOURCE["id"], "--from-file", str(page)]) == 0
    assert read_lock(repo, SOURCE["id"]).snapshot["method"] == "file"
    assert cli.main(["verify-quotes", SOURCE["id"]]) == 0
    assert len(read_lock(repo, SOURCE["id"]).quotes) == 2
    assert cli.main(["validate"]) == 0


def test_check_quote_reports_found_and_not_found(repo: Paths, capsys):
    page = saved_page(repo)
    cli.main(["snapshot", SOURCE["id"], "--from-file", str(page)])
    assert cli.main(["check-quote", SOURCE["id"], "The grader was written by a model."]) == 0
    assert cli.main(["check-quote", SOURCE["id"], "The grader was written by a person."]) == 1
    assert cli.main(["check-quote", "S-none", "anything"]) == 2


def test_validate_fails_on_unverified_quotes(repo: Paths, capsys):
    assert cli.main(["validate"]) == 1
    assert "not verified" in capsys.readouterr().out


def test_a_lock_with_no_source_record_is_a_warning(verified: Paths):
    lock_path(verified, "S-orphan").write_text(
        json.dumps({"source_id": "S-orphan", "snapshot": None, "quotes": {}})
    )
    found = [p for p in validate(verified) if p.where == "data/locks/S-orphan.json"]
    assert [p.level for p in found] == ["warning"]
    assert "no source record" in found[0].message


def test_a_source_with_evidence_and_unrelated_record_edits_keeps_its_stamps(repo: Paths):
    page = saved_page(repo)
    cli.main(["snapshot", SOURCE["id"], "--from-file", str(page)])
    cli.main(["verify-quotes"])
    before = read_lock(repo, SOURCE["id"]).quotes
    write_record(repo, f"sources/{SOURCE['id']}.yml", dict(SOURCE, summary="Reworded."))
    cli.main(["verify-quotes"])
    assert read_lock(repo, SOURCE["id"]).quotes == before


def test_prune_locks_removes_only_locks_with_no_source_record(repo: Paths, capsys):
    page = saved_page(repo)
    cli.main(["snapshot", SOURCE["id"], "--from-file", str(page)])
    cli.main(["verify-quotes"])
    orphan = lock_path(repo, "S-orphan")
    orphan.write_text(json.dumps({"source_id": "S-orphan", "snapshot": None, "quotes": {}}))
    assert cli.main(["prune-locks"]) == 0
    assert not orphan.exists()
    assert lock_path(repo, SOURCE["id"]).exists()
    assert "S-orphan" in capsys.readouterr().out


def test_snapshot_flags_a_page_that_marks_itself_paywalled(repo: Paths, capsys):
    page = repo.root / "paywalled.html"
    page.write_text(
        PAGE.replace(
            "<script>ignored()</script>",
            '<script type="application/ld+json">{"isAccessibleForFree": "False"}</script>',
        ),
        encoding="utf-8",
    )
    assert cli.main(["snapshot", SOURCE["id"], "--from-file", str(page)]) == 0
    assert "paywalled" in capsys.readouterr().out
    assert read_lock(repo, SOURCE["id"]).snapshot["paywalled"] is True


def test_snapshot_of_an_open_page_is_not_flagged(repo: Paths, capsys):
    cli.main(["snapshot", SOURCE["id"], "--from-file", str(saved_page(repo))])
    assert "paywalled" not in capsys.readouterr().out
    assert read_lock(repo, SOURCE["id"]).snapshot["paywalled"] is False
