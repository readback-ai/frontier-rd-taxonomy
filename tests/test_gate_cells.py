"""Gate inputs recorded above the leaves, by change type, and what the pacing model gets."""

from __future__ import annotations

import datetime as dt

import pytest
import yaml
from conftest import write_record

from frontier_taxonomy.config import Paths
from frontier_taxonomy.pacing import gate_inputs, pacing_block, write_gate_inputs
from frontier_taxonomy.store import load
from frontier_taxonomy.validate import validate


def leaf(task_id: str, change_type: str) -> dict:
    return {
        "id": task_id,
        "name": task_id,
        "parent": "T-y",
        "description": "A task.",
        "output_roles": ["runs"],
        "verifiability": "empirical",
        "feedback_latency": "days",
        "failure_visibility": "quiet",
        "reversibility": "cheap",
        "privilege": ["internal_code"],
        "change_type": change_type,
    }


BRANCH = {
    "branch": "T-y",
    "status": "draft",
    "tasks": [
        {"id": "T-y", "name": "Second branch", "description": "A branch."},
        leaf("T-y-software", "system_software_change"),
        leaf("T-y-recipes", "training_improvement"),
    ],
}


def prior(suffix: str, quantity: str, values: tuple, change_type: str | None, **extra) -> dict:
    low, central, high = values
    record = {
        "id": f"EST-y-{suffix}",
        "task": "T-y",
        "quantity": quantity,
        "scope": "frontier",
        "as_of": "2026-11",
        "value": {"kind": "range", "low": low, "central": central, "high": high},
        "basis": "judgment",
        "reasoning": "A prior.",
        "confidence": "low",
        "stale_after": dt.date(2027, 6, 1),
    }
    if change_type:
        record["change_type"] = change_type
    if quantity == "advance_share":
        record["denominator"] = "capability progress"
    record.update(extra)
    return record


SOFTWARE = "system_software_change"
TRAINING = "training_improvement"
PRIORS = [
    prior("software-count", "changes_per_researcher_year", (10, 20, 40), SOFTWARE),
    prior("software-hours", "hours_to_understand", (2, 5, 10), SOFTWARE),
    prior("software-elasticity", "elasticity_to_ai_labor", (0.2, 0.4, 0.8), SOFTWARE),
    prior("software-share", "advance_share", (0.1, 0.2, 0.4), SOFTWARE),
    prior("training-count", "changes_per_researcher_year", (2, 6, 12), TRAINING),
    prior("training-hours", "hours_to_understand", (5, 10, 20), TRAINING),
    prior("training-elasticity", "elasticity_to_ai_labor", (0.3, 0.5, 0.9), TRAINING),
    prior("training-share", "advance_share", (0.3, 0.6, 0.8), TRAINING),
]


@pytest.fixture
def repo(verified: Paths) -> Paths:
    write_record(verified, "tasks/T-y.yml", BRANCH)
    write_record(verified, "estimates/T-y.yml", {"task": "T-y", "estimates": PRIORS})
    return verified


def errors(paths: Paths) -> list[str]:
    return [f"{p.where}: {p.message}" for p in validate(paths) if p.level == "error"]


def rewrite(paths: Paths, estimates: list[dict]) -> None:
    write_record(paths, "estimates/T-y.yml", {"task": "T-y", "estimates": estimates})


def test_a_branch_level_prior_feeds_its_change_type(repo: Paths):
    assert errors(repo) == []
    table = gate_inputs(load(repo))
    assert table[SOFTWARE]["changes_per_researcher_year"].central == 20
    assert table[TRAINING]["hours_to_understand"].central == 10
    assert table[TRAINING]["hours_to_understand"].basis == "judgment"
    # the leaf-level estimates of the first branch still count
    assert table["evaluation_change"]["changes_per_researcher_year"].central == 4


def test_a_number_above_the_leaves_must_say_which_change_type(repo: Paths):
    rewrite(repo, [prior("software-count", "changes_per_researcher_year", (1, 2, 3), None)])
    found = errors(repo)
    assert any("EST-y-software-count" in m and "change_type" in m for m in found)


def test_the_change_type_must_exist_under_the_task(repo: Paths):
    rewrite(repo, [prior("data-count", "changes_per_researcher_year", (1, 2, 3), "dataset_update")])
    assert any("no task under T-y deploys dataset_update" in m for m in errors(repo))


def test_a_leaf_estimate_cannot_contradict_its_task(repo: Paths):
    wrong = dict(
        prior("leaf-count", "changes_per_researcher_year", (1, 2, 3), TRAINING),
        id="EST-y-software-leaf-count",
        task="T-y-software",
    )
    write_record(repo, "estimates/T-y-software.yml", {"task": "T-y-software", "estimates": [wrong]})
    assert any("T-y-software deploys system_software_change" in m for m in errors(repo))


def test_counting_a_change_at_two_levels_is_an_error(repo: Paths):
    below = dict(
        prior("leaf-count", "changes_per_researcher_year", (1, 2, 3), None),
        id="EST-y-software-leaf-count",
        task="T-y-software",
    )
    write_record(repo, "estimates/T-y-software.yml", {"task": "T-y-software", "estimates": [below]})
    found = errors(repo)
    assert any("counted twice" in m and "EST-y-software-count" in m for m in found)


def test_change_type_is_for_gate_quantities_only(repo: Paths):
    bad = prior("software-level", "automation_level", (0, 0, 0), SOFTWARE)
    bad["value"] = {"kind": "level", "level": "AL3"}
    rewrite(repo, [bad])
    assert any("gate quantities only" in m for m in errors(repo))


def test_low_and_high_of_a_sum_are_narrower_than_adding_the_ends(repo: Paths):
    extra = dict(BRANCH, tasks=[*BRANCH["tasks"], leaf("T-y-more", SOFTWARE)])
    write_record(repo, "tasks/T-y.yml", extra)
    rewrite(repo, [e for e in PRIORS if e["id"] != "EST-y-software-count"])
    for name in ("software", "more"):
        record = dict(
            prior("count", "changes_per_researcher_year", (5, 10, 20), None),
            id=f"EST-y-{name}-count",
            task=f"T-y-{name}",
        )
        write_record(
            repo, f"estimates/T-y-{name}.yml", {"task": f"T-y-{name}", "estimates": [record]}
        )
    assert errors(repo) == []
    cell = gate_inputs(load(repo))[SOFTWARE]["changes_per_researcher_year"]
    assert cell.central == 20, "central is the sum at central values"
    assert 10 < cell.low < 20 < cell.high < 40, "independent cells do not all sit at one end"


def test_the_pacing_model_gets_progress_types_and_one_overhead_term(repo: Paths):
    block = pacing_block(gate_inputs(load(repo)))
    types = block["change_types"]
    assert set(types) == {"training_improvements", "system_software_changes"}
    assert types["system_software_changes"] == {
        "per_researcher_year": 20,
        "hours_to_understand": 5,
        "elasticity": 0.4,
        "progress_weight": 0.25,
    }
    assert types["training_improvements"]["progress_weight"] == 0.75
    # evaluation changes carry no progress: their count and hours go in the required term
    assert block["monitor_changes"] == {"per_researcher_year": 4, "hours_to_understand": 10}
    assert block["folded_into_monitor_changes"] == ["evaluation_change"]


def test_a_progress_type_without_its_four_numbers_is_left_out_and_listed(repo: Paths):
    rewrite(repo, [e for e in PRIORS if e["id"] != "EST-y-training-elasticity"])
    document = yaml.safe_load(write_gate_inputs(repo).read_text())
    assert document["missing"] == {"training_improvement": ["elasticity_to_ai_labor"]}
    assert "training_improvements" not in document["pacing_model"]["change_types"]
    assert document["change_types"][SOFTWARE]["role"] == "progress"
    assert document["change_types"]["evaluation_change"]["role"] == "required_overhead"
    by_branch = document["change_types"][SOFTWARE]["by_branch"]
    assert by_branch == {
        "T-y": {"changes_per_researcher_year": 20, "hours_per_researcher_year": 100}
    }


def test_totals_cover_every_type(repo: Paths):
    document = yaml.safe_load(write_gate_inputs(repo).read_text())
    totals = document["totals"]
    assert totals["changes_per_researcher_year"]["at_central_values"] == 20 + 6 + 4
    assert totals["hours_per_researcher_year"]["at_central_values"] == 20 * 5 + 6 * 10 + 4 * 10
    share = totals["comprehension_load_share_of_researcher_year"]
    assert share["at_central_values"] == pytest.approx(200 / 2000)
    assert share["p10"] < share["p50"] < share["p90"]
    # skewed inputs add up to more than their medians do
    assert share["p50"] > share["at_central_values"]


# ---- sensitivity: which input moves the pacing result most ------------------------------


def hours_runner(block: dict) -> dict[str, float]:
    """Stands in for the pacing model: the result is the hours needed to understand it all."""
    hours = sum(
        t["per_researcher_year"] * t["hours_to_understand"] for t in block["change_types"].values()
    )
    monitor = block.get("monitor_changes")
    if monitor:
        hours += monitor["per_researcher_year"] * monitor["hours_to_understand"]
    return {"hours": hours}


def test_an_override_moves_one_input_and_nothing_else(repo: Paths):
    dataset = load(repo)
    key = ("T-y", SOFTWARE, "changes_per_researcher_year")
    table = gate_inputs(dataset, overrides={key: 40})
    assert table[SOFTWARE]["changes_per_researcher_year"].central == 40
    assert table[TRAINING]["changes_per_researcher_year"].central == 6
    assert gate_inputs(dataset)[SOFTWARE]["changes_per_researcher_year"].central == 20


def test_inputs_are_ranked_by_how_far_they_move_the_result(repo: Paths):
    from frontier_taxonomy.sensitivity import one_at_a_time

    rows = one_at_a_time(load(repo), hours_runner, metric="hours")
    assert len(rows) == 10, "eight priors on the second branch, two leaf estimates on the first"
    first, second = rows[0], rows[1]
    # software hours 2 to 10 over 20 changes moves the total by 160 hours, the largest swing
    assert (first.task, first.change_type, first.quantity) == (
        "T-y",
        SOFTWARE,
        "hours_to_understand",
    )
    assert first.at_low == pytest.approx(200 - 60) and first.at_high == pytest.approx(200 + 100)
    # software count 10 to 40 at 5 hours each moves it by 150
    assert second.quantity == "changes_per_researcher_year" and second.change_type == SOFTWARE
    assert second.swing == pytest.approx(150)
    assert [r.swing for r in rows] == sorted((r.swing for r in rows), reverse=True)
    # elasticity and share do not enter this stand-in result at all
    assert rows[-1].swing == 0


def test_joint_draws_give_a_spread(repo: Paths):
    from frontier_taxonomy.sensitivity import joint_draws

    results = joint_draws(load(repo), hours_runner, draws=200)
    hours = sorted(r["hours"] for r in results)
    assert len(hours) == 200
    assert hours[20] < 200 < hours[180], "the central result sits inside the 80% interval"
    assert joint_draws(load(repo), hours_runner, draws=5) == joint_draws(
        load(repo), hours_runner, draws=5
    ), "draws are reproducible"


def test_a_sensitivity_report_run_on_older_inputs_is_flagged(repo: Paths):
    from frontier_taxonomy.pacing import digest, gate_document

    def warnings() -> list[str]:
        return [p.message for p in validate(repo) if p.level == "warning"]

    current = digest(gate_document(load(repo)))
    repo.reports.mkdir(parents=True, exist_ok=True)
    report = repo.reports / "sensitivity.md"
    report.write_text(f"Data date: 2026-02-01. Gate inputs fingerprint: `{current}`. More text.\n")
    assert not any("taxo sensitivity" in message for message in warnings())
    rewrite(repo, [dict(PRIORS[0], value={"kind": "point", "value": 99}), *PRIORS[1:]])
    assert any("taxo sensitivity" in message for message in warnings())
