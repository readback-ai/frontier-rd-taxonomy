import copy
import datetime as dt

import numpy as np
import pytest
import yaml
from conftest import ESTIMATES, TASKS, estimate, write_record

from frontier_taxonomy.config import Paths
from frontier_taxonomy.pacing import (
    comprehension_load,
    gate_inputs,
    sample_range,
    write_gate_inputs,
)
from frontier_taxonomy.report import data_date, write_reports
from frontier_taxonomy.store import load


def test_gate_inputs_come_from_leaf_estimates(verified: Paths):
    table = gate_inputs(load(verified))
    cells = table["evaluation_change"]
    assert cells["changes_per_researcher_year"].central == 4
    assert cells["hours_to_understand"].central == 10
    assert cells["hours_to_understand"].basis == "judgment"
    assert cells["hours_to_understand"].estimates == ("EST-x-graders-hours",)


def test_counts_add_and_hours_average_by_count(verified: Paths):
    tasks = copy.deepcopy(TASKS)
    second = dict(tasks["tasks"][1], id="T-x-tasks", name="Tasks")
    tasks["tasks"].append(second)
    write_record(verified, "tasks/T-x.yml", tasks)
    more = {
        "task": "T-x-tasks",
        "estimates": [
            dict(
                estimate(
                    "count",
                    "changes_per_researcher_year",
                    {"kind": "range", "low": 6, "central": 12, "high": 24},
                    basis="judgment",
                    evidence=[],
                ),
                id="EST-x-tasks-count",
                task="T-x-tasks",
            ),
            dict(
                estimate("hours", "hours_to_understand", {"kind": "point", "value": 2}),
                id="EST-x-tasks-hours",
                task="T-x-tasks",
            ),
        ],
    }
    write_record(verified, "estimates/T-x-tasks.yml", more)
    cells = gate_inputs(load(verified))["evaluation_change"]
    assert cells["changes_per_researcher_year"].central == 16
    assert cells["hours_to_understand"].central == pytest.approx((4 * 10 + 12 * 2) / 16)
    # one evidence-based and one judgment estimate combine to the weaker basis
    assert cells["hours_to_understand"].basis == "judgment"


def test_latest_estimate_wins(verified: Paths):
    newer = copy.deepcopy(ESTIMATES)
    newer["estimates"].append(
        dict(
            estimate(
                "count-2",
                "changes_per_researcher_year",
                {"kind": "point", "value": 9},
                basis="judgment",
                evidence=[],
            ),
            as_of="2026-06",
        )
    )
    write_record(verified, "estimates/T-x-graders.yml", newer)
    cells = gate_inputs(load(verified))["evaluation_change"]
    assert cells["changes_per_researcher_year"].central == 9


def test_other_scopes_are_ignored(verified: Paths):
    assert gate_inputs(load(verified), scope="Lab") == {}


def test_sample_range_hits_its_percentiles():
    draws = sample_range(2.0, 5.0, 20.0, 200_000, np.random.default_rng(1))
    p10, p50, p90 = np.percentile(draws, [10, 50, 90])
    assert p10 == pytest.approx(2.0, rel=0.03)
    assert p50 == pytest.approx(5.0, rel=0.03)
    assert p90 == pytest.approx(20.0, rel=0.03)
    assert (sample_range(3.0, 3.0, 3.0, 5, np.random.default_rng(1)) == 3.0).all()
    with pytest.raises(ValueError):
        sample_range(0.0, 1.0, 2.0, 5, np.random.default_rng(1))


def test_comprehension_load_is_count_times_hours(verified: Paths):
    load_share = comprehension_load(gate_inputs(load(verified)))["evaluation_change"]
    assert load_share["p50"] == pytest.approx(4 * 10 / 2000, rel=0.05)
    assert load_share["p10"] < load_share["p50"] < load_share["p90"]


def test_gate_inputs_file_lists_what_is_missing(verified: Paths):
    document = yaml.safe_load(write_gate_inputs(verified).read_text())
    assert document["missing"]["evaluation_change"] == ["elasticity_to_ai_labor", "advance_share"]


def test_reports_are_reproducible_and_dated_by_the_data(verified: Paths):
    assert data_date(verified, load(verified)) == dt.date(2026, 2, 1)
    first = {p.name: p.read_text() for p in write_reports(verified)}
    second = {p.name: p.read_text() for p in write_reports(verified)}
    assert first == second
    assert set(first) == {
        "coverage.md",
        "branch-x.md",
        "question-pack-x.md",
        "backtest.md",
        "gate-inputs.yml",
    }
    assert "Data date: 2026-02-01." in first["coverage.md"]
    assert "2 of 2 quotes are verified" in first["coverage.md"]
    assert "2 of 4 estimates (50%) rest on judgment alone" in first["coverage.md"]
    assert "How do you know the grader agrees with people?" in first["question-pack-x.md"]
    assert "1 of 1 backtested incidents" in first["backtest.md"]
    from frontier_taxonomy.schema import CANARY

    assert CANARY in first["question-pack-x.md"]
    assert CANARY in first["backtest.md"]
    assert "A model-written grader passes wrong answers" in first["branch-x.md"]


def test_coverage_shows_each_scope_and_never_merges_them(verified: Paths):
    two_scopes = copy.deepcopy(ESTIMATES)
    two_scopes["estimates"].append(
        dict(
            estimate("automation-other", "automation_level", {"kind": "level", "level": "AL2"}),
            scope="Other Lab",
            as_of="2026-06",
        )
    )
    write_record(verified, "estimates/T-x-graders.yml", two_scopes)
    coverage = {p.name: p.read_text() for p in write_reports(verified)}["coverage.md"]
    assert "Other Lab: AL2 [evidence]; frontier: AL4 [evidence]" in coverage


def test_no_judgment_estimates_is_stated_plainly(verified: Paths):
    sourced = copy.deepcopy(ESTIMATES)
    sourced["estimates"] = sourced["estimates"][:2]
    write_record(verified, "estimates/T-x-graders.yml", sourced)
    coverage = {p.name: p.read_text() for p in write_reports(verified)}["coverage.md"]
    assert "0 of 2 estimates (0%) rest on judgment alone.\n" in coverage
    assert "priors" not in coverage
