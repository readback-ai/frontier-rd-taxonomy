"""Checks that hold the dataset together. Run by ``taxo validate`` and by CI.

Errors are things that make a record untrustworthy: a broken reference, a number with nothing
behind it, a quote nobody verified. Warnings are gaps in coverage and things going stale.
"""

from __future__ import annotations

import datetime as dt

from .config import Paths
from .locks import read_lock, stamp_is_current
from .schema import Estimate
from .store import Dataset, Problem, load
from .textnorm import quote_hash

# Quantities a researched leaf task is expected to carry (spec section 5).
EXPECTED_LEAF_QUANTITIES = ("automation_level", "oversight_mode")


def evidence_status(paths: Paths, dataset: Dataset) -> dict[str, str]:
    """For each evidence id: "verified", "excused" (carries an unverified_reason) or
    "unverified"."""
    status: dict[str, str] = {}
    locks = {source_id: read_lock(paths, source_id) for source_id in dataset.sources}
    for evidence_id, item in dataset.evidence.items():
        lock = locks[dataset.evidence_source[evidence_id]]
        if stamp_is_current(lock, evidence_id, quote_hash(item.quote)):
            status[evidence_id] = "verified"
        elif item.unverified_reason:
            status[evidence_id] = "excused"
        else:
            status[evidence_id] = "unverified"
    return status


def stale_estimates(dataset: Dataset, as_of: dt.date) -> list[Estimate]:
    return sorted(
        (e for e in dataset.estimates.values() if e.stale_after < as_of), key=lambda e: e.id
    )


def _check_references(dataset: Dataset, error) -> None:
    def need(table: dict, key: str, where: str, what: str) -> None:
        if key not in table:
            error(where, f"unknown {what} {key}")

    for task in dataset.tasks.values():
        if task.parent:
            need(dataset.tasks, task.parent, task.id, "parent task")
    for branch_id, branch in dataset.branches.items():
        need(dataset.tasks, branch_id, branch_id, "branch task")
        root = dataset.tasks.get(branch_id)
        if root and root.parent:
            error(branch_id, "a branch task has no parent")
        for task in branch.tasks:
            if task.id != branch_id and dataset.branch_of(task.id) != branch_id:
                error(task.id, f"is in the file of {branch_id} but does not descend from it")
    for task in dataset.tasks.values():
        chain = dataset.ancestors(task.id)
        last = dataset.tasks.get(chain[-1]) if chain else task
        if last and last.parent:
            error(task.id, "parent chain loops")

    for item in dataset.evidence.values():
        for task_id in item.tasks:
            need(dataset.tasks, task_id, item.id, "task")
    for estimate in dataset.estimates.values():
        need(dataset.tasks, estimate.task, estimate.id, "task")
        for evidence_id in estimate.evidence:
            need(dataset.evidence, evidence_id, estimate.id, "evidence")
    for risk in dataset.risks.values():
        for task_id in risk.tasks:
            need(dataset.tasks, task_id, risk.id, "task")
        for evidence_id in risk.evidence:
            need(dataset.evidence, evidence_id, risk.id, "evidence")
        for incident_id in risk.incidents:
            need(dataset.incidents, incident_id, risk.id, "incident")
    for task_id, question_set in dataset.question_sets.items():
        need(dataset.tasks, task_id, f"questions/{task_id}", "task")
        for question in question_set.questions:
            for risk_id in question.risks:
                need(dataset.risks, risk_id, question.id, "risk")
    for incident in dataset.incidents.values():
        for task_id in incident.tasks:
            need(dataset.tasks, task_id, incident.id, "task")
        for risk_id in incident.risks:
            need(dataset.risks, risk_id, incident.id, "risk")
        for evidence_id in incident.evidence:
            need(dataset.evidence, evidence_id, incident.id, "evidence")
        for entry in incident.backtest:
            need(dataset.questions, entry.question, incident.id, "question")
    for intervention in dataset.interventions.values():
        for task_id in intervention.targets.tasks:
            need(dataset.tasks, task_id, intervention.id, "task")
        for evidence_id in intervention.evidence:
            need(dataset.evidence, evidence_id, intervention.id, "evidence")
    for crosswalk in dataset.crosswalks.values():
        if crosswalk.source:
            need(dataset.sources, crosswalk.source, crosswalk.id, "source")
        for entry in crosswalk.entries:
            for task_id in entry.tasks:
                need(dataset.tasks, task_id, f"{crosswalk.id}/{entry.external_id}", "task")


def _check_evidence(dataset: Dataset, status: dict[str, str], error, warning) -> None:
    for evidence_id, state in status.items():
        if state == "unverified":
            error(
                evidence_id,
                "quote is not verified against the current snapshot. Run `taxo verify-quotes "
                f"{dataset.evidence_source[evidence_id]}`, or give an unverified_reason",
            )
    for estimate in dataset.estimates.values():
        cited = [e for e in estimate.evidence if e in dataset.evidence]
        if cited and all(status.get(e) != "verified" for e in cited):
            warning(estimate.id, "none of the cited evidence has a verified quote")
        if (
            estimate.basis == "evidence"
            and cited
            and all(dataset.evidence[e].grade == "D" for e in cited)
        ):
            warning(estimate.id, "basis 'evidence' rests on grade D (analog) items only")


def validate(paths: Paths, as_of: dt.date | None = None) -> list[Problem]:
    """Every problem in the dataset: load errors, broken references, rule breaks, gaps."""
    problems: list[Problem] = []
    dataset = load(paths, problems)

    def error(where: str, message: str) -> None:
        problems.append(Problem("error", where, message))

    def warning(where: str, message: str) -> None:
        problems.append(Problem("warning", where, message))

    _check_references(dataset, error)
    status = evidence_status(paths, dataset)
    _check_evidence(dataset, status, error, warning)
    _check_coverage(dataset, problems)
    for estimate in stale_estimates(dataset, as_of or dt.date.today()):
        warning(estimate.id, f"stale since {estimate.stale_after}")
    return problems


def _check_coverage(dataset: Dataset, problems: list[Problem]) -> None:
    """Coverage checks, appending to ``problems``."""

    def add(level: str, where: str, message: str) -> None:
        problems.append(Problem(level, where, message))

    estimates_by_task: dict[str, set[str]] = {}
    for estimate in dataset.estimates.values():
        estimates_by_task.setdefault(estimate.task, set()).add(estimate.quantity)
    tasks_with_risk = {task_id for risk in dataset.risks.values() for task_id in risk.tasks}

    for branch in dataset.branches.values():
        researched = branch.status == "researched"
        for task in branch.tasks:
            if not dataset.is_leaf(task.id):
                continue
            if not task.has_attributes:
                add("error" if researched else "warning", task.id, "leaf task lacks attributes")
                continue
            if not researched:
                continue
            for quantity in EXPECTED_LEAF_QUANTITIES:
                if quantity not in estimates_by_task.get(task.id, set()):
                    add("warning", task.id, f"researched leaf has no {quantity} estimate")
            if task.id not in tasks_with_risk:
                add("warning", task.id, "researched leaf has no risk")
            if task.id not in dataset.question_sets:
                add("warning", task.id, "researched leaf has no question set")

    targeted = {risk_id for q in dataset.questions.values() for risk_id in q.risks}
    for risk in dataset.risks.values():
        if risk.review_catchable != "no" and risk.id not in targeted:
            add("warning", risk.id, "review-catchable risk has no question aimed at it")
    for question in dataset.questions.values():
        if not question.risks:
            add("warning", question.id, "question names no risk")
    for incident in dataset.incidents.values():
        if incident.comprehension_failure in ("yes", "partly") and not incident.backtest:
            add("warning", incident.id, "comprehension failure with no backtest")
