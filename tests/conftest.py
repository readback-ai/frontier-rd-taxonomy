"""A small, self-contained dataset written to a temporary folder for each test."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest
import yaml

from frontier_taxonomy.config import Paths
from frontier_taxonomy.schema import CANARY
from frontier_taxonomy.snapshot import write_snapshot

PAGE = """<html><body><h1>Risk report</h1>
<p>We reviewed “every” transcript by hand &ndash; all 40 of them.</p>
<p>The grader was written by a model. Nobody checked it against human labels
until after release.</p>
<script>ignored()</script>
<p>{filler}</p></body></html>""".format(
    filler="The rest of the report describes the evaluation suite in general terms. " * 8
)

SOURCE = {
    "id": "S-lab-2026-01-risk-report",
    "title": "Risk report",
    "publisher": "Lab",
    "published": "2026-01-15",
    "url": "https://example.org/risk-report",
    "type": "risk_report",
    "vantage": "first_party",
    "labs": ["Lab"],
    "summary": "A test source.",
    "evidence": [
        {
            "id": "EV-lab-2026-01-risk-report-01",
            "claim": "The grader was model-written and unchecked until after release.",
            "quote": "The grader was written by a model. Nobody checked it against human labels",
            "kind": "incident",
            "strength": "reported",
            "grade": "B",
            "tasks": ["T-x-graders"],
        },
        {
            "id": "EV-lab-2026-01-risk-report-02",
            "claim": "All 40 transcripts were reviewed by hand.",
            "quote": 'We reviewed "every" transcript by hand [...] all 40 of them.',
            "kind": "oversight",
            "strength": "measured",
            "grade": "A",
            "tasks": ["T-x-graders"],
        },
    ],
}

TASKS = {
    "branch": "T-x",
    "status": "researched",
    "tasks": [
        {"id": "T-x", "name": "Branch", "description": "A branch."},
        {
            "id": "T-x-graders",
            "name": "Graders",
            "parent": "T-x",
            "description": "Deciding what counts as success.",
            "output_roles": ["measures"],
            "verifiability": "judgment",
            "feedback_latency": "months",
            "failure_visibility": "silent",
            "reversibility": "costly",
            "privilege": ["eval_infra"],
            "change_type": "evaluation_change",
        },
    ],
}


def estimate(suffix: str, quantity: str, value: dict, **extra) -> dict:
    record = {
        "id": f"EST-x-graders-{suffix}",
        "task": "T-x-graders",
        "quantity": quantity,
        "scope": "frontier",
        "as_of": "2026-01",
        "value": value,
        "basis": "evidence",
        "evidence": ["EV-lab-2026-01-risk-report-01"],
        "reasoning": "From the report.",
        "confidence": "low",
        "stale_after": dt.date(2027, 1, 1),
    }
    record.update(extra)
    return record


ESTIMATES = {
    "task": "T-x-graders",
    "estimates": [
        estimate("automation", "automation_level", {"kind": "level", "level": "AL4"}),
        estimate(
            "oversight",
            "oversight_mode",
            {"kind": "category", "value": "ai_review_human_by_exception"},
        ),
        estimate(
            "count",
            "changes_per_researcher_year",
            {"kind": "range", "low": 2, "central": 4, "high": 8},
            basis="judgment",
            evidence=[],
        ),
        estimate(
            "hours",
            "hours_to_understand",
            {"kind": "range", "low": 5, "central": 10, "high": 20},
            basis="judgment",
            evidence=[],
        ),
    ],
}

RISK = {
    "id": "R-x-grader-false-pass",
    "title": "A model-written grader passes wrong answers",
    "tasks": ["T-x-graders"],
    "failure_mode": "The grader accepts outputs that a human would reject.",
    "harm_path": "false_assurance",
    "mechanisms": ["comprehension_gap", "correlated_error"],
    "automation_effect": "Nobody reads the grader when a model writes and a model reviews it.",
    "review_catchable": "yes",
    "review_rationale": "Asking for agreement with human labels exposes the gap.",
    "severity": "high",
    "status": "observed_frontier",
    "evidence": ["EV-lab-2026-01-risk-report-01"],
    "incidents": ["INC-2026-lab-grader"],
}

QUESTIONS = {
    "canary": CANARY,
    "task": "T-x-graders",
    "contribution": "A new model judge.",
    "questions": [
        {
            "id": "Q-x-graders-01",
            "category": "failure",
            "topical_area": "analysis_of_results",
            "question": "How do you know the grader agrees with people?",
            "good_answer_shows": "Agreement measured on held-out human labels.",
            "red_flags": ["Agreement was never measured."],
            "risks": ["R-x-grader-false-pass"],
        }
    ],
}

INCIDENT = {
    "id": "INC-2026-lab-grader",
    "title": "Unchecked grader",
    "org": "Lab",
    "frontier": True,
    "occurred": "2026-01",
    "summary": "A model-written grader was wrong.",
    "root_cause": "No human labels.",
    "detected_by": "An external reader.",
    "automation_involved": "yes",
    "comprehension_failure": "yes",
    "comprehension_note": "Nobody had read the grader.",
    "tasks": ["T-x-graders"],
    "risks": ["R-x-grader-false-pass"],
    "evidence": ["EV-lab-2026-01-risk-report-01"],
    "backtest": [
        {
            "question": "Q-x-graders-01",
            "verdict": "would_surface",
            "rationale": "The answer would have been that it was never measured.",
        }
    ],
}

FILES = {
    "sources/S-lab-2026-01-risk-report.yml": SOURCE,
    "tasks/T-x.yml": TASKS,
    "estimates/T-x-graders.yml": ESTIMATES,
    "risks/R-x-grader-false-pass.yml": RISK,
    "questions/T-x-graders.yml": QUESTIONS,
    "incidents/INC-2026-lab-grader.yml": INCIDENT,
}


def write_record(paths: Paths, relative: str, record: dict) -> Path:
    path = paths.records / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
    return path


def take_snapshot(paths: Paths, page: str = PAGE) -> None:
    write_snapshot(
        paths.snapshot_dir(SOURCE["id"]),
        SOURCE["id"],
        SOURCE["url"],
        page.encode("utf-8"),
        "text/html",
        SOURCE["url"],
        method="file",
        retrieved=dt.date(2026, 2, 1),
    )


@pytest.fixture
def paths(tmp_path: Path) -> Paths:
    """A repository with one source, one branch and one of every other record, unverified."""
    root = tmp_path / "repo"
    (root / "data").mkdir(parents=True)
    (root / "pyproject.toml").write_text("")
    paths = Paths(root=root, data_dir=tmp_path / "outside")
    for relative, record in FILES.items():
        write_record(paths, relative, record)
    return paths


@pytest.fixture
def verified(paths: Paths) -> Paths:
    """The same repository with a snapshot taken and every quote stamped."""
    from frontier_taxonomy.verify import verify_quotes

    take_snapshot(paths)
    results = verify_quotes(paths, today=dt.date(2026, 2, 1))
    assert {r.status for r in results} == {"verified"}
    return paths
