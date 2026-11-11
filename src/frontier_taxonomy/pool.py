"""Pooling per-developer estimates into one frontier figure.

Most published evidence comes from one developer. A figure labeled "frontier" that rests on
one lab's self-report says less than its label. The rule (spec decision D16): a pooled figure
exists for a task and quantity only when Anthropic, OpenAI and Google DeepMind each have their
own estimate. The pool is then the spread across the three, never an average that hides it:
levels and oversight modes pool to a range, numbers to the envelope of the three intervals with
the middle lab's central value.
"""

from __future__ import annotations

from dataclasses import dataclass

from .schema import (
    CategoryValue,
    Estimate,
    LevelsValue,
    LevelValue,
    PointValue,
    RangeValue,
)
from .store import Dataset

REQUIRED_LABS = ("Anthropic", "OpenAI", "Google DeepMind")
FRONTIER = "frontier"
POOLED_QUANTITIES = ("automation_level", "oversight_mode")
_ALIASES = {
    "google": "Google DeepMind",
    "gdm": "Google DeepMind",
    "deepmind": "Google DeepMind",
    "google deepmind": "Google DeepMind",
    "anthropic": "Anthropic",
    "openai": "OpenAI",
}
# From most to least human involvement.
OVERSIGHT_ORDER = (
    "human_every_change",
    "human_sampled",
    "ai_review_human_by_exception",
    "ai_review_only",
    "none",
)
_BASIS_RANK = {"evidence": 0, "mixed": 1, "judgment": 2}


def canonical_lab(name: str) -> str:
    """One spelling per developer, so "Google" and "Google DeepMind" count as the same lab."""
    return _ALIASES.get(name.strip().lower(), name.strip())


def _modal_level(estimate: Estimate) -> str:
    value = estimate.value
    if isinstance(value, LevelValue):
        return value.level
    if isinstance(value, LevelsValue):
        return max(sorted(value.shares), key=lambda level: value.shares[level])
    raise TypeError(f"{estimate.id}: not a level")


def _triple(estimate: Estimate) -> tuple[float, float, float]:
    value = estimate.value
    if isinstance(value, RangeValue):
        return value.low, value.central, value.high
    if isinstance(value, PointValue):
        return value.value, value.value, value.value
    raise TypeError(f"{estimate.id}: not a number")


@dataclass(frozen=True)
class Pool:
    """The required labs' latest estimates of one quantity for one task."""

    task: str
    quantity: str
    by_lab: dict[str, Estimate]

    @property
    def missing(self) -> tuple[str, ...]:
        return tuple(lab for lab in REQUIRED_LABS if lab not in self.by_lab)

    @property
    def complete(self) -> bool:
        return not self.missing

    @property
    def basis(self) -> str:
        """The weakest basis among the pooled estimates."""
        return max((e.basis for e in self.by_lab.values()), key=_BASIS_RANK.__getitem__)

    @property
    def estimates(self) -> tuple[str, ...]:
        return tuple(sorted(e.id for e in self.by_lab.values()))

    def triple(self) -> tuple[float, float, float]:
        """Lowest low, the middle lab's central value, highest high."""
        triples = [_triple(self.by_lab[lab]) for lab in REQUIRED_LABS]
        centrals = sorted(t[1] for t in triples)
        return min(t[0] for t in triples), centrals[len(centrals) // 2], max(t[2] for t in triples)

    def text(self) -> str:
        """The pooled value for a table cell, or which labs it still needs."""
        if not self.complete:
            return "needs " + ", ".join(self.missing)
        sample = next(iter(self.by_lab.values())).value
        if isinstance(sample, LevelValue | LevelsValue):
            levels = sorted(_modal_level(e) for e in self.by_lab.values())
            return levels[0] if levels[0] == levels[-1] else f"{levels[0]} to {levels[-1]}"
        if isinstance(sample, CategoryValue):
            modes = sorted((e.value.value for e in self.by_lab.values()), key=OVERSIGHT_ORDER.index)
            show = [modes[0]] if modes[0] == modes[-1] else [modes[0], modes[-1]]
            return " to ".join(mode.replace("_", " ") for mode in show)
        low, central, high = self.triple()
        return f"{central:g} ({low:g} to {high:g})"


def pool(dataset: Dataset, task_id: str, quantity: str) -> Pool:
    """The latest estimate from each required lab, for one task and quantity."""
    by_lab: dict[str, Estimate] = {}
    for estimate in dataset.estimates.values():
        if estimate.task != task_id or estimate.quantity != quantity:
            continue
        lab = canonical_lab(estimate.scope)
        if lab not in REQUIRED_LABS:
            continue
        current = by_lab.get(lab)
        if current is None or (estimate.as_of, estimate.id) > (current.as_of, current.id):
            by_lab[lab] = estimate
    return Pool(task_id, quantity, by_lab)


def lab_coverage(dataset: Dataset, branch_id: str) -> dict[str, tuple[int, int]]:
    """For each pooled quantity: (leaves with all three labs, leaves) in a branch."""
    leaves = [t for t in dataset.branches[branch_id].tasks if dataset.is_leaf(t.id)]
    return {
        quantity: (
            sum(1 for task in leaves if pool(dataset, task.id, quantity).complete),
            len(leaves),
        )
        for quantity in POOLED_QUANTITIES
    }


def labs_behind(dataset: Dataset, estimate: Estimate) -> set[str]:
    """The developers named by the sources of an estimate's evidence."""
    labs: set[str] = set()
    for evidence_id in estimate.evidence:
        source = dataset.sources.get(dataset.evidence_source.get(evidence_id, ""))
        if source:
            labs.update(canonical_lab(lab) for lab in source.labs)
    return labs
