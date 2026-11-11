"""Bottom-up inputs for the pacing model's gate on deployed changes.

The pacing and takeoff model lives in readback-ops (research/pacing-takeoff-model). Its gate
takes, for each type of deployed change: how many are deployed per researcher-year, the hours
to understand one, how the count grows with AI labor, and the share of progress that rides on
the type. In that model every one of those numbers is an assumption. This module builds the
same table from task-level estimates here, so each cell names its evidence or says it is
judgment. It does not run the takeoff model.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml

from .config import Paths
from .schema import Estimate, PointValue, RangeValue
from .store import Dataset, load

RESEARCHER_HOURS_PER_YEAR = 2000.0
GATE_QUANTITIES = (
    "changes_per_researcher_year",
    "hours_to_understand",
    "elasticity_to_ai_labor",
    "advance_share",
)
# How task-level values combine into one value per change type.
_COMBINE = {
    "changes_per_researcher_year": "sum",
    "hours_to_understand": "count_weighted_mean",
    "elasticity_to_ai_labor": "count_weighted_mean",
    "advance_share": "sum",
}
_BASIS_RANK = {"evidence": 0, "mixed": 1, "judgment": 2}


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
            "low": round(self.low, 4),
            "central": round(self.central, 4),
            "high": round(self.high, 4),
            "basis": self.basis,
            "estimates": list(self.estimates),
        }


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


def gate_inputs(dataset: Dataset, scope: str = "frontier") -> dict[str, dict[str, Cell]]:
    """Gate inputs by change type, combined from the leaf-task estimates in ``scope``.

    Counts and progress shares add across tasks. Hours and elasticities are averaged, weighted
    by each task's central count of changes; a task with no count estimate weighs 1.
    """
    current = latest(dataset.estimates.values(), scope)
    by_type: dict[str, dict[str, list[tuple[Estimate, float]]]] = {}
    for (task_id, quantity), estimate in current.items():
        if quantity not in GATE_QUANTITIES:
            continue
        task = dataset.tasks.get(task_id)
        if task is None or not task.change_type or task.change_type == "none":
            continue
        count = current.get((task_id, "changes_per_researcher_year"))
        weight = _triple(count)[1] if count else 1.0
        by_type.setdefault(task.change_type, {}).setdefault(quantity, []).append((estimate, weight))

    table: dict[str, dict[str, Cell]] = {}
    for change_type, quantities in sorted(by_type.items()):
        table[change_type] = {}
        for quantity, items in sorted(quantities.items()):
            triples = np.array([_triple(estimate) for estimate, _ in items])
            if _COMBINE[quantity] == "sum":
                low, central, high = triples.sum(axis=0)
            else:
                weights = np.array([weight for _, weight in items])
                low, central, high = (triples * weights[:, None]).sum(axis=0) / weights.sum()
            basis = max((estimate.basis for estimate, _ in items), key=_BASIS_RANK.__getitem__)
            table[change_type][quantity] = Cell(
                float(low),
                float(central),
                float(high),
                basis,
                tuple(sorted(estimate.id for estimate, _ in items)),
            )
    return table


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


def comprehension_load(
    table: dict[str, dict[str, Cell]], draws: int = 20000, seed: int = 0
) -> dict[str, dict[str, float]]:
    """Share of a researcher-year needed to understand every deployed change, by change type.

    Only change types with both a count and an hours estimate contribute. Returns the 10th,
    50th and 90th percentiles of count times hours over hours in a researcher-year.
    """
    rng = np.random.default_rng(seed)
    result: dict[str, dict[str, float]] = {}
    for change_type, cells in table.items():
        count, hours = cells.get("changes_per_researcher_year"), cells.get("hours_to_understand")
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


def write_gate_inputs(paths: Paths, scope: str = "frontier") -> Path:
    """Write ``reports/gate-inputs.yml``: the table, the load it implies and what is missing."""
    dataset = load(paths)
    table = gate_inputs(dataset, scope)
    change_types = sorted(
        {t.change_type for t in dataset.tasks.values() if t.change_type not in (None, "none")}
    )
    missing = {
        change_type: [q for q in GATE_QUANTITIES if q not in table.get(change_type, {})]
        for change_type in change_types
    }
    document = {
        "generated_by": "taxo gate-inputs (do not edit by hand)",
        "scope": scope,
        "note": (
            "Bottom-up counterpart of comprehension_gate.change_types in the readback-ops pacing "
            "model's calibration.yml. low and high are 10th and 90th percentiles. basis is the "
            "weakest basis among the estimates combined into the cell."
        ),
        "change_types": {
            change_type: {quantity: cell.as_dict() for quantity, cell in cells.items()}
            for change_type, cells in table.items()
        },
        "comprehension_load_share_of_researcher_year": comprehension_load(table),
        "missing": {k: v for k, v in missing.items() if v},
    }
    paths.reports.mkdir(parents=True, exist_ok=True)
    out = paths.reports / "gate-inputs.yml"
    out.write_text(yaml.safe_dump(document, sort_keys=False, width=100), encoding="utf-8")
    return out
