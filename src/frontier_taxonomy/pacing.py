"""Bottom-up inputs for the pacing model's gate on deployed changes.

The pacing and takeoff model lives in readback-ops (research/pacing-takeoff-model). Its gate
takes, for each type of deployed change: how many are deployed per researcher-year, the hours
to understand one, how the count grows with AI labor, and the share of progress that rides on
the type. In that model every one of those numbers is an assumption. This module builds the
same table from task-level estimates here, so each cell names its evidence or says it is
judgment. It does not run the takeoff model; ``sensitivity.py`` does that.

Two kinds of change type. Progress types (training improvements, dataset updates, system
software changes) carry capability progress and take all four numbers. Required-overhead types
(monitor, evaluation and control changes, decisions) carry none: a developer cannot drop them
to save review time, so the pacing model takes their hours off the top, in the term it calls
monitor changes.
"""

from __future__ import annotations

import hashlib
import json
import zlib
from collections.abc import Iterable
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import yaml

from .config import Paths
from .pool import FRONTIER, REQUIRED_LABS, canonical_lab
from .schema import GATE_QUANTITIES, Estimate, PointValue, RangeValue
from .store import Dataset, load

RESEARCHER_HOURS_PER_YEAR = 2000.0
COUNT, HOURS, ELASTICITY, SHARE = GATE_QUANTITIES
PROGRESS_TYPES = ("training_improvement", "dataset_update", "system_software_change")
OVERHEAD_TYPES = ("monitor_change", "evaluation_change", "control_change", "decision")
# The readback-ops model's names for the progress types.
PACING_NAMES = {
    "training_improvement": "training_improvements",
    "dataset_update": "dataset_updates",
    "system_software_change": "system_software_changes",
}
# How values combine across the tasks that feed one change type.
_COMBINE = {
    COUNT: "sum",
    HOURS: "count_weighted_mean",
    ELASTICITY: "count_weighted_mean",
    SHARE: "sum",
}
_BASIS_RANK = {"evidence": 0, "mixed": 1, "judgment": 2}
_DRAWS = 20000
_SEED = 0


def role_of(change_type: str) -> str:
    return "progress" if change_type in PROGRESS_TYPES else "required_overhead"


def expected_quantities(change_type: str) -> tuple[str, ...]:
    """Progress types need all four gate numbers; required overhead needs count and hours."""
    return GATE_QUANTITIES if change_type in PROGRESS_TYPES else (COUNT, HOURS)


def _round(value: float) -> float:
    """Four significant figures: enough for a prior, and stable across platforms."""
    return float(f"{value:.4g}")


@dataclass(frozen=True)
class Cell:
    """One gate input for one change type, with where it came from."""

    low: float
    central: float
    high: float
    basis: str  # the weakest basis among the estimates combined
    estimates: tuple[str, ...]

    def as_dict(self) -> dict:
        return {
            "low": _round(self.low),
            "central": _round(self.central),
            "high": _round(self.high),
            "basis": self.basis,
            "estimates": list(self.estimates),
        }


@dataclass(frozen=True)
class Input:
    """One gate number for one task and change type, before types are combined."""

    task: str
    change_type: str
    quantity: str
    triple: tuple[float, float, float]
    basis: str
    estimates: tuple[str, ...]

    @property
    def key(self) -> str:
        return f"{self.task}/{self.change_type}/{self.quantity}"


def _triple(estimate: Estimate) -> tuple[float, float, float]:
    value = estimate.value
    if isinstance(value, RangeValue):
        return value.low, value.central, value.high
    if isinstance(value, PointValue):
        return value.value, value.value, value.value
    raise TypeError(f"{estimate.id}: {estimate.quantity} needs a numeric value")


def latest(estimates: Iterable[Estimate], scope: str) -> dict[tuple[str, str], Estimate]:
    """The most recent estimate for each (task, quantity) in a scope."""
    chosen: dict[tuple[str, str], Estimate] = {}
    for estimate in estimates:
        if estimate.scope != scope:
            continue
        key = (estimate.task, estimate.quantity)
        if key not in chosen or estimate.as_of > chosen[key].as_of:
            chosen[key] = estimate
    return chosen


Key = tuple[str, str, str]  # task, change type, quantity


def gate_values(
    dataset: Dataset, scope: str = FRONTIER, overrides: dict[Key, float] | None = None
) -> dict[Key, Input]:
    """The gate numbers in a scope, keyed by (task, change type, quantity).

    For the frontier, a pool of the three required developers replaces a frontier estimate
    wherever each of the three has its own number (spec decision D16). ``overrides`` fixes
    chosen inputs at a value, for sensitivity runs.
    """
    values = _recorded_values(dataset, scope)
    for key, value in (overrides or {}).items():
        values[key] = replace(values[key], triple=(value, value, value))
    return values


def _recorded_values(dataset: Dataset, scope: str) -> dict[Key, Input]:
    newest: dict[tuple[str, str, str, str], Estimate] = {}
    for estimate in dataset.estimates.values():
        change_type = dataset.change_type_of(estimate)
        if estimate.quantity not in GATE_QUANTITIES or not change_type:
            continue
        key = (canonical_lab(estimate.scope), estimate.task, change_type, estimate.quantity)
        current = newest.get(key)
        if current is None or (estimate.as_of, estimate.id) > (current.as_of, current.id):
            newest[key] = estimate

    values: dict[tuple[str, str, str], Input] = {}
    for (owner, task, change_type, quantity), estimate in sorted(newest.items()):
        if owner == scope:
            values[(task, change_type, quantity)] = Input(
                task, change_type, quantity, _triple(estimate), estimate.basis, (estimate.id,)
            )
    if scope != FRONTIER:
        return values
    cells = {(task, change_type, quantity) for _, task, change_type, quantity in newest}
    for task, change_type, quantity in sorted(cells):
        labs = [newest.get((lab, task, change_type, quantity)) for lab in REQUIRED_LABS]
        if not all(labs):
            continue
        triples = [_triple(e) for e in labs]
        centrals = sorted(t[1] for t in triples)
        values[(task, change_type, quantity)] = Input(
            task,
            change_type,
            quantity,
            (min(t[0] for t in triples), centrals[1], max(t[2] for t in triples)),
            max((e.basis for e in labs), key=_BASIS_RANK.__getitem__),
            tuple(sorted(e.id for e in labs)),
        )
    return values


def sample_range(
    low: float, central: float, high: float, size: int, rng: np.random.Generator
) -> np.ndarray:
    """Draws from a split lognormal with median ``central``, 10th percentile ``low`` and 90th
    percentile ``high``. All three must be positive. A point value returns a constant."""
    if not (0 < low <= central <= high):
        raise ValueError("sample_range needs 0 < low <= central <= high")
    if low == high:
        return np.full(size, central)
    z90 = 1.2815515655446004
    sigma_low = np.log(central / low) / z90
    sigma_high = np.log(high / central) / z90
    z = rng.standard_normal(size)
    return central * np.exp(np.where(z < 0, sigma_low, sigma_high) * z)


def _draws(item: Input, size: int = _DRAWS) -> np.ndarray:
    """Draws for one input. The stream depends only on the input's key, so adding or changing
    another estimate leaves these draws, and every number built on them, as they were."""
    rng = np.random.default_rng([_SEED, zlib.crc32(item.key.encode())])
    return sample_range(*item.triple, size, rng)


def _central(items: list[Input], counts: dict[tuple[str, str], Input]) -> float:
    """One quantity over the tasks that feed a change type, at every input's central value.

    Counts and progress shares add. Hours and elasticities are averaged, weighted by each
    task's count of changes; a task with no count weighs 1.
    """
    centrals = np.array([item.triple[1] for item in items])
    if _COMBINE[items[0].quantity] == "sum":
        return float(centrals.sum())
    weigh = [counts.get((item.task, item.change_type)) for item in items]
    weights = np.array([w.triple[1] if w else 1.0 for w in weigh])
    return float((centrals * weights).sum() / weights.sum())


def _spread(items: list[Input], counts: dict[tuple[str, str], Input]) -> tuple[float, float]:
    """10th and 90th percentiles of the same combination when the inputs vary independently."""
    if len(items) == 1:
        return items[0].triple[0], items[0].triple[2]
    draws = np.array([_draws(item) for item in items])
    if _COMBINE[items[0].quantity] == "sum":
        combined = draws.sum(axis=0)
    else:
        weigh = [counts.get((item.task, item.change_type)) for item in items]
        weights = np.array([_draws(w) if w else np.ones(_DRAWS) for w in weigh])
        combined = (draws * weights).sum(axis=0) / weights.sum(axis=0)
    low, high = np.percentile(combined, [10, 90])
    return float(low), float(high)


def gate_inputs(
    dataset: Dataset,
    scope: str = FRONTIER,
    overrides: dict[Key, float] | None = None,
    spread: bool = True,
) -> dict[str, dict[str, Cell]]:
    """Gate inputs by change type, combined from the estimates in ``scope``.

    ``central`` is the value at every input's central estimate. ``low`` and ``high`` are the
    10th and 90th percentiles when the inputs vary independently, which is narrower than
    adding the ends. ``spread=False`` skips them, for runs that only use the central values.
    """
    values = gate_values(dataset, scope, overrides)
    counts = {(i.task, i.change_type): i for i in values.values() if i.quantity == COUNT}
    grouped: dict[str, dict[str, list[Input]]] = {}
    for item in values.values():
        grouped.setdefault(item.change_type, {}).setdefault(item.quantity, []).append(item)

    table: dict[str, dict[str, Cell]] = {}
    for change_type, quantities in sorted(grouped.items()):
        table[change_type] = {}
        for quantity, items in sorted(quantities.items()):
            central = _central(items, counts)
            low, high = _spread(items, counts) if spread else (central, central)
            table[change_type][quantity] = Cell(
                low,
                central,
                high,
                max((item.basis for item in items), key=_BASIS_RANK.__getitem__),
                tuple(sorted(i for item in items for i in item.estimates)),
            )
    return table


def by_branch(dataset: Dataset, scope: str = FRONTIER) -> dict[str, dict[str, dict[str, float]]]:
    """For each change type, each branch's central count and the hours it implies."""
    values = gate_values(dataset, scope)
    out: dict[str, dict[str, dict[str, float]]] = {}
    for (task, change_type, quantity), item in sorted(values.items()):
        if quantity != COUNT:
            continue
        hours = values.get((task, change_type, HOURS))
        row = out.setdefault(change_type, {}).setdefault(
            dataset.branch_of(task),
            {"changes_per_researcher_year": 0.0, "hours_per_researcher_year": 0.0},
        )
        row["changes_per_researcher_year"] += item.triple[1]
        if hours:
            row["hours_per_researcher_year"] += item.triple[1] * hours.triple[1]
    return {
        change_type: {b: {k: _round(v) for k, v in row.items()} for b, row in branches.items()}
        for change_type, branches in out.items()
    }


def totals(dataset: Dataset, scope: str = FRONTIER) -> dict[str, dict[str, float]]:
    """Deployed changes and the hours to understand them, per researcher-year, over all types.

    ``at_central_values`` adds up every input's central estimate, which is what the pacing
    model is given. The percentiles vary the inputs independently. With wide, right-skewed
    priors the sum of the medians sits below the median of the sum, so both are reported.
    """
    values = gate_values(dataset, scope)
    count_central, hours_central = 0.0, 0.0
    count_draws, hours_draws = np.zeros(_DRAWS), np.zeros(_DRAWS)
    for (task, change_type, quantity), item in sorted(values.items()):
        if quantity != COUNT:
            continue
        draws = _draws(item)
        count_central += item.triple[1]
        count_draws += draws
        hours = values.get((task, change_type, HOURS))
        if hours:
            hours_central += item.triple[1] * hours.triple[1]
            hours_draws += draws * _draws(hours)

    def summary(central: float, draws: np.ndarray, scale: float = 1.0) -> dict[str, float]:
        p10, p50, p90 = np.percentile(draws, [10, 50, 90]) if draws.any() else (0.0, 0.0, 0.0)
        return {
            "at_central_values": _round(central / scale),
            "p10": _round(float(p10) / scale),
            "p50": _round(float(p50) / scale),
            "p90": _round(float(p90) / scale),
        }

    return {
        "changes_per_researcher_year": summary(count_central, count_draws),
        "hours_per_researcher_year": summary(hours_central, hours_draws),
        "comprehension_load_share_of_researcher_year": summary(
            hours_central, hours_draws, RESEARCHER_HOURS_PER_YEAR
        ),
    }


def comprehension_load(
    table: dict[str, dict[str, Cell]], draws: int = _DRAWS, seed: int = _SEED
) -> dict[str, dict[str, float]]:
    """Share of a researcher-year needed to understand every deployed change, by change type.

    Only change types with both a count and an hours estimate contribute. Returns the 10th,
    50th and 90th percentiles of count times hours over hours in a researcher-year.
    """
    rng = np.random.default_rng(seed)
    result: dict[str, dict[str, float]] = {}
    for change_type, cells in table.items():
        count, hours = cells.get(COUNT), cells.get(HOURS)
        if not (count and hours):
            continue
        load_share = (
            sample_range(count.low, count.central, count.high, draws, rng)
            * sample_range(hours.low, hours.central, hours.high, draws, rng)
            / RESEARCHER_HOURS_PER_YEAR
        )
        p10, p50, p90 = np.percentile(load_share, [10, 50, 90])
        result[change_type] = {
            "p10": round(float(p10), 4),
            "p50": round(float(p50), 4),
            "p90": round(float(p90), 4),
        }
    return result


def pacing_block(table: dict[str, dict[str, Cell]]) -> dict:
    """Values in the shape of ``comprehension_gate`` in the readback-ops calibration file.

    A progress type is included only when it has all four numbers. Progress weights are the
    shares, scaled to sum to one over the included types. Every required-overhead type with a
    count and hours is folded into ``monitor_changes``, the model's one required term.
    """
    ready = [t for t in PROGRESS_TYPES if all(q in table.get(t, {}) for q in GATE_QUANTITIES)]
    share_total = sum(table[t][SHARE].central for t in ready)
    change_types = {
        PACING_NAMES[t]: {
            "per_researcher_year": _round(table[t][COUNT].central),
            "hours_to_understand": _round(table[t][HOURS].central),
            "elasticity": _round(table[t][ELASTICITY].central),
            "progress_weight": _round(table[t][SHARE].central / share_total),
        }
        for t in ready
    }
    folded = [t for t in OVERHEAD_TYPES if COUNT in table.get(t, {}) and HOURS in table[t]]
    count = sum(table[t][COUNT].central for t in folded)
    hours = sum(table[t][COUNT].central * table[t][HOURS].central for t in folded)
    block: dict = {"change_types": change_types}
    if folded:
        block["monitor_changes"] = {
            "per_researcher_year": _round(count),
            "hours_to_understand": _round(hours / count),
        }
    block["folded_into_monitor_changes"] = sorted(folded)
    return block


def missing_inputs(dataset: Dataset, table: dict[str, dict[str, Cell]]) -> dict[str, list[str]]:
    """For each change type some task deploys: the gate numbers it should have and lacks."""
    deployed = sorted(
        {t.change_type for t in dataset.tasks.values() if t.change_type not in (None, "none")}
    )
    gaps = {
        change_type: [
            q for q in expected_quantities(change_type) if q not in table.get(change_type, {})
        ]
        for change_type in deployed
    }
    return {change_type: lacking for change_type, lacking in gaps.items() if lacking}


def gate_document(dataset: Dataset, scope: str = FRONTIER) -> dict:
    """Everything ``reports/gate-inputs.yml`` holds."""
    table = gate_inputs(dataset, scope)
    branches = by_branch(dataset, scope)
    return {
        "generated_by": "taxo gate-inputs (do not edit by hand)",
        "scope": scope,
        "note": (
            "Bottom-up counterpart of comprehension_gate in the readback-ops pacing model's "
            "calibration.yml. central is the value at every input's central estimate. low and "
            "high are the 10th and 90th percentiles when the inputs vary independently. basis "
            "is the weakest basis among the estimates combined into the cell. Progress types "
            "carry capability progress. Required-overhead types carry none and are folded into "
            "the model's monitor_changes term."
        ),
        "change_types": {
            change_type: {
                "role": role_of(change_type),
                **{quantity: cell.as_dict() for quantity, cell in cells.items()},
                "by_branch": branches.get(change_type, {}),
            }
            for change_type, cells in table.items()
        },
        "totals": totals(dataset, scope),
        "comprehension_load_share_of_researcher_year": comprehension_load(table),
        "pacing_model": pacing_block(table),
        "missing": missing_inputs(dataset, table),
    }


def digest(document: dict) -> str:
    """A fingerprint of the numbers a sensitivity run depends on."""
    core = {k: document[k] for k in ("scope", "change_types", "pacing_model")}
    return hashlib.sha256(json.dumps(core, sort_keys=True).encode()).hexdigest()[:16]


def write_gate_inputs(paths: Paths, scope: str = FRONTIER) -> Path:
    """Write ``reports/gate-inputs.yml``: the table, the load it implies and what is missing."""
    document = gate_document(load(paths), scope)
    paths.reports.mkdir(parents=True, exist_ok=True)
    out = paths.reports / "gate-inputs.yml"
    out.write_text(yaml.safe_dump(document, sort_keys=False, width=100), encoding="utf-8")
    return out
