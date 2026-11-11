import copy
import datetime as dt

from conftest import PAGE, RISK, SOURCE, TASKS, take_snapshot, write_record

from frontier_taxonomy.config import Paths
from frontier_taxonomy.locks import read_lock
from frontier_taxonomy.validate import validate
from frontier_taxonomy.verify import verify_quotes

AS_OF = dt.date(2026, 3, 1)


def errors(paths: Paths) -> list[str]:
    return [f"{p.where}: {p.message}" for p in validate(paths, AS_OF) if p.level == "error"]


def warnings(paths: Paths) -> list[str]:
    return [f"{p.where}: {p.message}" for p in validate(paths, AS_OF) if p.level == "warning"]


def test_unverified_quotes_are_errors(paths: Paths):
    found = errors(paths)
    assert len(found) == 2
    assert all("not verified" in message for message in found)


def test_verified_dataset_is_clean(verified: Paths):
    assert errors(verified) == []
    assert warnings(verified) == []
    lock = read_lock(verified, SOURCE["id"])
    assert set(lock.quotes) == {item["id"] for item in SOURCE["evidence"]}
    assert lock.snapshot["retrieved"] == "2026-02-01"


def test_no_snapshot_leaves_locks_alone(paths: Paths):
    results = verify_quotes(paths)
    assert {r.status for r in results} == {"no_snapshot"}
    assert read_lock(paths, SOURCE["id"]).quotes == {}


def test_a_paraphrase_is_not_verified(paths: Paths):
    record = copy.deepcopy(SOURCE)
    record["evidence"][0]["quote"] = "The grader was written by a model and never checked"
    write_record(paths, f"sources/{SOURCE['id']}.yml", record)
    take_snapshot(paths)
    status = {r.evidence_id: r.status for r in verify_quotes(paths)}
    assert status["EV-lab-2026-01-risk-report-01"] == "not_found"
    assert status["EV-lab-2026-01-risk-report-02"] == "verified"
    assert any("EV-lab-2026-01-risk-report-01" in message for message in errors(paths))


def test_editing_a_quote_voids_its_stamp(verified: Paths):
    record = copy.deepcopy(SOURCE)
    record["evidence"][0]["quote"] = "The grader was written by a model."
    write_record(verified, f"sources/{SOURCE['id']}.yml", record)
    assert any("EV-lab-2026-01-risk-report-01" in message for message in errors(verified))
    verify_quotes(verified)
    assert errors(verified) == []


def test_a_changed_snapshot_voids_every_stamp(verified: Paths):
    take_snapshot(verified, PAGE.replace("all 40 of them", "all 12 of them"))
    from frontier_taxonomy.locks import record_snapshot
    from frontier_taxonomy.snapshot import read_snapshot

    meta, _ = read_snapshot(verified.snapshot_dir(SOURCE["id"]))
    record_snapshot(verified, meta)
    assert len(errors(verified)) == 2
    status = {r.evidence_id: r.status for r in verify_quotes(verified)}
    assert status["EV-lab-2026-01-risk-report-01"] == "verified"
    assert status["EV-lab-2026-01-risk-report-02"] == "not_found"


def test_unverified_reason_excuses_a_quote(paths: Paths):
    record = copy.deepcopy(SOURCE)
    for item in record["evidence"]:
        item["unverified_reason"] = "The page refuses automated fetches."
    write_record(paths, f"sources/{SOURCE['id']}.yml", record)
    assert errors(paths) == []
    assert any("none of the cited evidence has a verified quote" in w for w in warnings(paths))


def test_broken_references_are_errors(verified: Paths):
    write_record(
        verified,
        "risks/R-x-grader-false-pass.yml",
        dict(RISK, tasks=["T-x-nowhere"], evidence=["EV-lab-2026-01-risk-report-09"]),
    )
    found = errors(verified)
    assert any("unknown task T-x-nowhere" in message for message in found)
    assert any("unknown evidence EV-lab-2026-01-risk-report-09" in message for message in found)


def test_invalid_file_is_reported_not_raised(verified: Paths):
    (verified.records / "risks" / "R-broken.yml").write_text("id: R-broken\ntitle: x\n")
    assert any("risks/R-broken.yml" in message for message in errors(verified))


def test_file_name_must_match_the_id(verified: Paths):
    write_record(verified, "risks/R-other-name.yml", RISK)
    found = errors(verified)
    assert any("file name must be R-x-grader-false-pass.yml" in message for message in found)
    assert any("duplicate id" in message for message in found)


def test_researched_leaf_without_attributes_is_an_error(verified: Paths):
    tasks = copy.deepcopy(TASKS)
    del tasks["tasks"][1]["verifiability"]
    write_record(verified, "tasks/T-x.yml", tasks)
    assert any("lacks attributes" in message for message in errors(verified))
    tasks["status"] = "draft"
    write_record(verified, "tasks/T-x.yml", tasks)
    assert errors(verified) == []


def test_coverage_gaps_are_warnings(verified: Paths):
    (verified.records / "questions" / "T-x-graders.yml").unlink()
    incident = verified.records / "incidents" / "INC-2026-lab-grader.yml"
    incident.write_text(incident.read_text().split("backtest:")[0])
    found = warnings(verified)
    assert any("no question set" in w for w in found)
    assert any("no question aimed at it" in w for w in found)
    assert any("no backtest" in w for w in found)


def test_stale_estimates_warn(verified: Paths):
    stale = [p for p in validate(verified, dt.date(2027, 6, 1)) if "stale since" in p.message]
    assert len(stale) == 4
