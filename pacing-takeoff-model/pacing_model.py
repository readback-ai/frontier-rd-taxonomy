"""Pacing and takeoff model: shared building blocks and Model A.

Model A is Ajeya Cotra's simple Cobb-Douglas account of AI R&D acceleration
(Planned Obsolescence, 2026-11-06) written as a dynamic model, then modified so
that human time stays a required input.

Units
-----
Progress Y is measured in baseline-years: one baseline-year is one year of
progress at the pre-October-2025 rate (about 15 AECI points). Pace is dY/dt,
so 1.0 is the historical rate.

Human time per unit of work (tau, h, psi) is a fraction of the time a human
would need to do the same work unaided. Labor uplift is its reciprocal.

See README.md for the derivation and the sources behind each parameter.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from pathlib import Path

import numpy as np
import yaml
from scipy.optimize import brentq, least_squares

HERE = Path(__file__).resolve().parent
LN2 = math.log(2.0)


def load_calibration(path: Path | None = None) -> dict:
    with open(path or HERE / "calibration.yml") as f:
        return yaml.safe_load(f)


def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))


def logit(p):
    return math.log(p / (1.0 - p))


# --------------------------------------------------------------------------
# Pacing mechanisms
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class ChangeType:
    """One kind of change that reaches production."""

    name: str
    per_year: float  # deployed per researcher-year at the reference date, with no gate
    hours: float  # researcher-hours to understand one to audit standard
    elasticity: float  # percent growth in the count per percent growth in AI labor
    weight: float  # share of progress that rides on this type


@dataclass(frozen=True)
class Gate:
    """Deployed changes by type, and the human time a rule requires on each.

    Experiments are not gated. Their number grows in proportion to AI labor.
    The number of deployed changes of each type grows with AI labor to the
    power `elasticity`, below one, so deployed changes are a shrinking share
    of experiments. Monitor changes are not driven by labor: their count grows
    with the log of the training improvements that are promoted.
    """

    types: tuple[ChangeType, ...]
    monitor_per_year: float = 2.0
    monitor_hours: float = 12.0
    hours_per_year: float = 2000.0
    experiments_per_change: float = 20.0  # at the reference date
    tail: float = 1.8  # Pareto tail index of the value of a deployed change
    hours_scale: float = 1.0  # multiplies every type's hours
    signoff_hours: float = 0.0  # if positive, every change costs this instead of its hours
    coverage: float = 1.0  # share of deployed changes the lab keeps understood
    hours_halving: float = 0.0  # AI helps people understand: hours halve per this much capability
    hours_floor: float = 0.25
    hours_doubling: float = (
        0.0  # changes get harder to understand: hours double per this much capability
    )

    def hours_multiplier(self, cap: float, cap_start: float) -> float:
        m = 1.0
        if self.hours_halving > 0.0:
            m *= max(self.hours_floor, 2.0 ** (-(cap - cap_start) / self.hours_halving))
        if self.hours_doubling > 0.0:
            m *= 2.0 ** ((cap - cap_start) / self.hours_doubling)
        return m

    @property
    def changes_at_reference(self) -> float:
        return sum(t.per_year for t in self.types) + self.monitor_per_year

    @property
    def hours_at_reference(self) -> float:
        """Researcher-hours per year to understand everything deployed at the reference date."""
        return (
            sum(t.per_year * t.hours for t in self.types)
            + self.monitor_per_year * self.monitor_hours
        )


@dataclass(frozen=True)
class Policy:
    """A pacing mechanism. All fields default to "no pacing"."""

    name: str = "No pacing"
    start: float = 2027.0
    # Human time required on every deployed change. None means no requirement.
    gate: Gate | None = None
    # Models may be used for AI R&D only `lag` years after they exist.
    lag: float = 0.0
    # R&D compute (experiments and training) is cut by this constant factor.
    compute_cut: float = 1.0
    # R&D compute is frozen at its level on the start date.
    compute_freeze: bool = False


# --------------------------------------------------------------------------
# The gate on deployed changes
# --------------------------------------------------------------------------
_USE = np.geomspace(1e-5, 1.0, 400)  # the lab may leave AI labor unused


def _waterfill(budget: np.ndarray, load: np.ndarray, weight: np.ndarray) -> np.ndarray:
    """Split `budget` hours across change types to maximize sum_k weight_k * log(q_k),
    where q_k = hours_k / load_k is capped at 1. Shapes: budget (n,), load (k, n), weight (k,)."""
    k, n = load.shape
    q = np.ones((k, n))
    active = np.ones((k, n), dtype=bool)
    remaining = budget.copy()
    for _ in range(k):
        wsum = (weight[:, None] * active).sum(axis=0)
        alloc = np.where(active, remaining * weight[:, None] / np.maximum(wsum, 1e-300), 0.0)
        full = active & (alloc >= load)
        if not full.any():
            break
        remaining = remaining - (load * full).sum(axis=0)
        active &= ~full
    wsum = (weight[:, None] * active).sum(axis=0)
    alloc = remaining * weight[:, None] / np.maximum(wsum, 1e-300)
    return np.where(active, np.clip(alloc / np.maximum(load, 1e-300), 1e-12, 1.0), q)


def deployment(
    g: Gate, labor_ratio, q=None, enforce: bool = False, hours_mult: float = 1.0
) -> dict:
    """Counts and hours per researcher-year at AI labor `labor_ratio` times the reference level."""
    r = np.asarray(labor_ratio, dtype=float)
    want = np.array([t.per_year * r**t.elasticity for t in g.types])
    q = np.ones_like(want) if q is None else q
    train = next(i for i, t in enumerate(g.types) if t.name.startswith("training"))
    promoted_training = q[train] * want[train] / g.types[train].per_year
    monitors = g.monitor_per_year * (1.0 + np.log(np.maximum(promoted_training, math.exp(-1.0))))
    per_change = (
        np.full(len(g.types), g.signoff_hours)
        if g.signoff_hours > 0.0
        else np.array([t.hours for t in g.types]) * g.hours_scale * hours_mult
    )
    monitor_cost = (
        g.signoff_hours if g.signoff_hours > 0.0 else g.monitor_hours * g.hours_scale * hours_mult
    )
    deployed = (q * want).sum(axis=0) + monitors
    return dict(
        want=want,
        load=want * per_change[:, None] * g.coverage,
        monitor_hours=monitors * monitor_cost * g.coverage,
        deployed=deployed,
        experiments=g.experiments_per_change * g.changes_at_reference * r,
    )


def gate(tau: float, effort_of_labor, labor_ref: float, g: Gate, hours_mult: float = 1.0) -> dict:
    """Research effort when every deployed change needs human time.

    tau: human time per unit of work spent directing AI (supervision only).
    effort_of_labor: maps a labor multiple (array) to a research effort multiple
        (array), both relative to the human-only case.
    labor_ref: the labor multiple at the reference date, where the counts in `g` hold.

    The lab chooses how much AI labor to use. Directing it takes a share
    theta = labor * tau of each person's year. The rest is available for
    understanding deployed changes. If that is not enough to cover every
    change the lab would deploy, it deploys the most valuable fraction q_k of
    each type. With Pareto-distributed value the best fraction q holds
    q ** (1 - 1/tail) of the value, and types combine by their progress
    weights. Hours go first to the monitor changes that promoted training
    improvements require, then across types to maximize value.
    """
    labor = _USE / tau
    theta = _USE
    effort = np.asarray(effort_of_labor(labor), dtype=float)
    weight = np.array([t.weight for t in g.types])
    weight = weight / weight.sum()
    hours = g.hours_per_year * (1.0 - theta)
    q = np.ones((len(g.types), len(labor)))
    for _ in range(3):  # monitor load depends on promoted training changes
        d = deployment(g, labor / labor_ref, q, hours_mult=hours_mult)
        q = _waterfill(np.maximum(hours - d["monitor_hours"], 0.0), d["load"], weight)
    d = deployment(g, labor / labor_ref, q, hours_mult=hours_mult)
    kept = np.prod(q ** ((1.0 - 1.0 / g.tail) * weight[:, None]), axis=0)
    value = effort * kept
    i = int(np.argmax(value))
    used = float((q[:, i] * d["load"][:, i]).sum() + d["monitor_hours"][i])
    return dict(
        effort=float(value[i]),
        theta=float(theta[i]),
        labor=float(labor[i]),
        kept=float(kept[i]),
        comprehension_share=used / g.hours_per_year,
        deployed=float(d["deployed"][i]),
        experiments=float(d["experiments"][i]),
        q={t.name: float(q[k, i]) for k, t in enumerate(g.types)},
    )


# --------------------------------------------------------------------------
# The link from comprehension to human research judgment
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class Link:
    """People apply research judgment only to the deployed changes they understand.

    Without the link, a lab keeps the full benefit of its researchers' judgment
    however little of the deployed work they understand. With it, the judgment
    behind the lab's research is a blend: the usual mix of people and AI on the
    share of deployed value people understand, and AI alone on the rest.
    """

    depth: float = 1.0  # hours to understand a change well enough to judge what to try next,
    #                           as a multiple of the hours the central audit standard requires
    time_today: float = 0.0  # share of researcher time that goes to understanding deployed changes
    #                           at the reference date; measured labor uplift already reflects it


def link_from_calibration(cal: dict, **overrides) -> Link:
    g = gate_from_calibration(cal)
    depth = overrides.pop("depth", cal["judgment_link"]["depth"])
    # Monitor changes carry no progress weight, so no judgment rides on understanding them.
    hours = sum(t.per_year * t.hours for t in g.types)
    base = dict(depth=depth, time_today=depth * hours / g.hours_per_year)
    base.update(overrides)
    return Link(**base)


def power_mean(values, weights, r: float):
    """Weighted power mean along the first axis, with exponent r. r = 0 is the geometric mean.

    This is the judgment of a lab whose research needs several classes of task, when it
    spreads its experiments across the classes to best effect. With an elasticity of
    substitution sigma between the classes, r = sigma - 1. For sigma below 1 the classes
    are complements: the mean is pulled toward the weakest class, and the share of effort
    that goes to class k, weights_k * values_k ** r / sum, rises as that class falls behind.
    """
    v = np.maximum(np.asarray(values, dtype=float), 1e-300)
    w = np.asarray(weights, dtype=float)
    w = (w / w.sum()).reshape((-1,) + (1,) * (v.ndim - 1))
    if abs(r) < 1e-9:
        return np.exp((w * np.log(v)).sum(axis=0))
    return (w * v**r).sum(axis=0) ** (1.0 / r)


_USE_FINE = np.concatenate([np.geomspace(1e-5, 0.1, 80), np.linspace(0.1, 1.0, 301)[1:]])
_SPLIT = (1.0, 0.75, 0.5, 0.25)  # share of hours tried for required time before top-ups


def _concave_fill(
    budget: np.ndarray, cost: np.ndarray, weight: np.ndarray, cap: np.ndarray, beta: float
) -> np.ndarray:
    """Split `budget` hours across change types to maximize sum_k weight_k * x_k ** beta,
    where x_k = hours_k / cost_k is capped at cap_k. All arrays are (k, n) except budget (n,)."""
    k, _ = cost.shape
    costly = cost > 0.0
    merit = np.where(costly, (weight / np.maximum(cost, 1e-300)) ** (1.0 / (1.0 - beta)), 0.0)
    x = np.where(costly, 0.0, cap)  # a type that costs nothing is understood in full
    active = costly & (cap > 0.0) & (weight > 0.0)
    remaining = budget.astype(float).copy()
    for _ in range(k):
        denom = (cost * merit * active).sum(axis=0)
        trial = np.where(active, remaining * merit / np.maximum(denom, 1e-300), 0.0)
        full = active & (trial >= cap)
        if not full.any():
            break
        x = np.where(full, cap, x)
        remaining = remaining - (cost * cap * full).sum(axis=0)
        active &= ~full
    denom = (cost * merit * active).sum(axis=0)
    trial = remaining * merit / np.maximum(denom, 1e-300)
    return np.where(active, np.clip(trial, 0.0, cap), x)


def lab_choice(
    tau: float,
    capacity_of_labor,
    labor_ref: float,
    changes: Gate,
    rule: Gate | None,
    taste_people,
    taste_ai,
    link: Link,
    hours_mult: float = 1.0,
    people_share: float = 1.0,
    class_shares=None,
    class_r: float = 0.0,
) -> dict:
    """Research effort when human judgment depends on comprehension.

    tau: human time per unit of work spent directing AI.
    capacity_of_labor: maps a labor multiple (array) to research effort at a judgment
        level of 1, relative to the human-only case.
    changes: the counts of deployed changes. rule: the pacing rule in force, or None.
    taste_people: the lab's research judgment when people's judgment is applied to all
        work (people where they beat AI, AI elsewhere). taste_ai: AI judgment alone.

    Returns `understood`, the share u below for researchers ahead of the AI, and
    `understood_lab`, the share of the lab's deployed value that some person understands.

    The lab chooses how much AI labor to use, how many changes of each type to deploy
    (the most valuable fraction q_k), and how many to understand in depth (the most
    valuable fraction x_k of the type, x_k <= q_k). Each deployed change costs the hours
    the rule requires, and understanding one in depth costs any further hours up to
    `link.depth` times the central standard. Time a rule requires counts toward
    understanding in proportion to depth. The understood share of deployed value is

        u = sum_k weight_k * (c_k + (1 - c_k) * (x_k / q_k) ** (1 - 1/tail)),

    with c_k the credit from required time, and the lab's judgment is
    taste_ai + (taste_people - taste_ai) * u. With no rule nothing is required, every
    change is deployed, and all understanding is the lab's own choice.

    people_share: the share of researchers whose judgment is better than the AI's. Only
    they gain anything from understanding beyond what a rule requires, so only they
    spend the extra hours, each on their own share of the lab's changes.

    With several classes of research task, taste_people and taste_ai are sequences with
    one entry per class, class_shares the classes' effort shares at equal judgment, and
    class_r the power-mean exponent (see power_mean). A person who understands a change
    applies their judgment to it in every class, so one understood share serves all
    classes, and the lab's judgment is the power mean of the per-class blends.
    """
    g = rule if rule is not None else changes
    if g.coverage != 1.0:
        raise ValueError("the judgment link is not defined for partial coverage")
    theta = _USE_FINE
    labor = theta / tau
    capacity = np.asarray(capacity_of_labor(labor), dtype=float)
    k, n = len(g.types), len(labor)
    weight = np.array([t.weight for t in g.types])
    weight = weight / weight.sum()
    beta = 1.0 - 1.0 / g.tail
    hours = g.hours_per_year * (1.0 - theta)
    judge = np.array([t.hours for t in g.types]) * link.depth * hours_mult
    if rule is None:
        need = np.zeros(k)
    elif g.signoff_hours > 0.0:
        need = np.full(k, g.signoff_hours)
    else:
        need = np.array([t.hours for t in g.types]) * g.hours_scale * hours_mult
    credit = np.minimum(need / judge, 1.0)
    top = np.maximum(judge - need, 0.0)
    taste_ai = np.atleast_1d(np.asarray(taste_ai, dtype=float))
    gain = np.maximum(np.atleast_1d(np.asarray(taste_people, dtype=float)) - taste_ai, 0.0)
    class_shares = (
        np.ones(len(taste_ai)) if class_shares is None else np.asarray(class_shares, dtype=float)
    )
    share = min(max(people_share, 1e-9), 1.0)
    ratio = labor / labor_ref
    best = None
    for split in (0.0,) if rule is None else _SPLIT if top.any() else (1.0,):
        if rule is None:
            q = np.ones((k, n))
            d = deployment(g, ratio, q)
            required = np.zeros(n)
        else:
            q = np.ones((k, n))
            for _ in range(3):  # monitor load depends on promoted training changes
                d = deployment(g, ratio, q, hours_mult=hours_mult)
                q = _waterfill(
                    np.maximum(hours * split - d["monitor_hours"], 0.0), d["load"], weight
                )
            d = deployment(g, ratio, q, hours_mult=hours_mult)
            required = (q * d["load"]).sum(axis=0) + d["monitor_hours"]
        cost = d["want"] * top[:, None]
        spare = np.maximum(hours - required, 0.0)  # per researcher, averaged over the lab
        own = np.maximum(g.hours_per_year - required, 0.0)  # the most one researcher can add
        x = _concave_fill(
            np.minimum(spare / share, own),
            cost,
            (weight * (1.0 - credit))[:, None] / q**beta,
            q,
            beta,
        )
        topped = (1.0 - credit[:, None]) * (x / q) ** beta
        understood = (weight[:, None] * (credit[:, None] + topped)).sum(axis=0)
        # Across the whole lab: researchers behind the AI add nothing beyond what a rule requires.
        understood_lab = (weight[:, None] * (credit[:, None] + share * topped)).sum(axis=0)
        kept = np.prod(q ** (beta * weight[:, None]), axis=0)
        taste = power_mean(
            taste_ai[:, None] + gain[:, None] * understood[None, :], class_shares, class_r
        )
        value = capacity * kept * taste
        i = int(np.argmax(value))
        if best is None or value[i] > best["effort"]:
            spent = float(required[i] + share * (x[:, i] * cost[:, i]).sum())
            best = dict(
                effort=float(value[i]),
                theta=float(theta[i]),
                labor=float(labor[i]),
                kept=float(kept[i]),
                understood=float(understood[i]),
                understood_lab=float(understood_lab[i]),
                taste=float(taste[i]),
                comprehension_share=spent / g.hours_per_year,
                deployed=float(d["deployed"][i]),
                experiments=float(d["experiments"][i]),
                q={t.name: float(q[j, i]) for j, t in enumerate(g.types)},
                x={t.name: float(x[j, i]) for j, t in enumerate(g.types)},
            )
    return best


def free_deployment(g: Gate, labor: float, labor_ref: float) -> dict:
    """What the lab deploys with no gate, for reporting."""
    d = deployment(g, np.array([labor / labor_ref]))
    return dict(
        deployed=float(d["deployed"][0]),
        experiments=float(d["experiments"][0]),
        hours_if_understood=float(d["load"][:, 0].sum() + d["monitor_hours"][0]),
    )


def gate_from_calibration(cal: dict, **overrides) -> Gate:
    c = cal["comprehension_gate"]
    types = tuple(
        ChangeType(
            name,
            v["per_researcher_year"],
            v["hours_to_understand"],
            v["elasticity"],
            v["progress_weight"],
        )
        for name, v in c["change_types"].items()
    )
    base = dict(
        types=types,
        monitor_per_year=c["monitor_changes"]["per_researcher_year"],
        monitor_hours=c["monitor_changes"]["hours_to_understand"],
        hours_per_year=c["researcher_hours_per_year"],
        experiments_per_change=1.0 / c["deployed_share_of_experiments_today"],
        tail=c["value_tail_index"],
    )
    base.update(overrides)
    return Gate(**base)


def rescale(
    g: Gate, counts: float = 1.0, elasticity: float | None = None, weights: dict | None = None
) -> Gate:
    """A copy of `g` with every count multiplied, every elasticity replaced, or weights replaced."""
    types = tuple(
        replace(
            t,
            per_year=t.per_year * counts,
            elasticity=t.elasticity if elasticity is None else elasticity,
            weight=t.weight if weights is None else weights[t.name],
        )
        for t in g.types
    )
    return replace(g, types=types, monitor_per_year=g.monitor_per_year * counts)


# --------------------------------------------------------------------------
# Human time needed to supervise AI work
# --------------------------------------------------------------------------
@dataclass
class Supervision:
    """Human time per unit of work as a function of capability.

    kind = "none":      no supervision requirement beyond what capability implies.
    kind = "anthropic": shares of work by automation level follow logistics in
                        capability fitted to Anthropic's Automation Index, with
                        fixed human time per level. Unsupervised work (AL5)
                        lags AI-led work (AL4).
    kind = "gdm":       the same schedule fitted to Google DeepMind's share of fully
                        delegated pull requests. It is stored with kind "anthropic".
    kind = "openai":    human time per unit of work halves each time the task
                        length that agents complete with zero interventions
                        doubles. That horizon is fitted to OpenAI's monthly
                        zero-intervention success rates by task duration.
    kind = "openai_runtime": human time per unit of agent work halves each time
                        OpenAI's ratio of agent workdays to human workdays
                        doubles. This is supervision as practiced, not as needed.

    Both OpenAI schedules are set to equal 1 / labor uplift at the reference date.

    The realized human time per unit of work is the larger of this schedule
    and 1 / (capability-limited uplift).
    """

    kind: str = "none"
    # anthropic
    k: float = 0.0  # logistic slope per unit of capability
    mid4: float = 0.0  # capability at which AL4+ share is 50%
    lag5: float = 0.0  # capability distance by which AL5 trails AL4
    lead3: float = 0.0  # capability distance by which AL3 leads AL4
    h2: float = 0.50
    h3: float = 0.12
    h4: float = 0.04
    al5_ceiling: float = 1.0
    # openai
    cap_ref: float = 0.0
    halving: float = 1.0
    h_ref: float = 1.0  # human time per unit of work at cap_ref
    # anthropic: level rescale so that h(reference) = 1 / labor uplift(reference).
    # Labor uplift is output per human hour, so the two are the same quantity today.
    scale: float = 1.0

    def shares(self, cap, al5_ceiling: float | None = None):
        ceiling = self.al5_ceiling if al5_ceiling is None else al5_ceiling
        s3 = logistic(self.k * (cap - self.mid4 + self.lead3))
        s4 = logistic(self.k * (cap - self.mid4))
        s5 = ceiling * logistic(self.k * (cap - self.mid4 - self.lag5))
        return s3, s4, s5

    def raw(self, cap: float, al5_ceiling: float | None = None) -> float:
        if self.kind == "anthropic":
            s3, s4, s5 = self.shares(cap, al5_ceiling)
            return float(self.h2 * (1 - s3) + self.h3 * (s3 - s4) + self.h4 * (s4 - s5))
        if self.kind in ("openai", "openai_runtime"):
            return float(self.h_ref * 2.0 ** (-(cap - self.cap_ref) / self.halving))
        return 0.0

    def h(self, cap: float, al5_ceiling: float | None = None) -> float:
        """Human time per unit of work. `al5_ceiling` overrides the largest share of work that
        can run unsupervised, for a ceiling that moves with capability."""
        return self.scale * self.raw(cap, al5_ceiling)


def read_data(name: str) -> list[dict]:
    """Rows of a CSV in data/, skipping the comment header."""
    import csv

    with open(HERE / "data" / name) as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def openai_horizon_fit(x: np.ndarray, hours: np.ndarray, success: np.ndarray):
    """Least-squares fit of logit(success) = a + b * x - c * log2(hours).

    Returns (a, b, c). The task length completed half the time with zero
    interventions is 2 ** ((a + b * x) / c), so it doubles every c / b units of x.
    """
    y = np.log(success / (1.0 - success))
    A = np.column_stack([np.ones(len(x)), x, -np.log2(hours)])
    (a, b, c), *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(a), float(b), float(c)


def fit_supervision(
    kind: str,
    cap_at,
    cap_ref: float,
    uplift_ref: float,
    cal: dict,
    al5_lag_months: float | None = None,
    h4: float | None = None,
    al5_ceiling: float = 1.0,
    openai_from: float = 0.0,
) -> Supervision:
    """Fit a supervision schedule in a model's own capability units.

    cap_at(date) maps a calendar date to that model's capability on its
    calibrated history, so the fit carries no assumption about pace.
    """
    if kind == "none":
        return Supervision("none")
    if kind == "openai":
        rows = [
            r
            for r in read_data("openai_zero_intervention_success.csv")
            if float(r["decimal_year"]) >= openai_from
        ]
        cap = np.array([cap_at(float(r["decimal_year"])) for r in rows])
        _, b, c = openai_horizon_fit(
            cap,
            np.array([float(r["hours_mid"]) for r in rows]),
            np.array([float(r["zero_intervention_success"]) for r in rows]),
        )
        return Supervision("openai", cap_ref=cap_ref, h_ref=1.0 / uplift_ref, halving=c / b)
    if kind == "openai_runtime":
        rows = [
            r
            for r in read_data("openai_chart_series.csv")
            if r["series"] == "agent_workdays_per_human_workday"
        ]
        cap = np.array([cap_at(float(r["decimal_year"])) for r in rows])
        slope, _ = np.polyfit(cap, np.log2([float(r["value"]) for r in rows]), 1)
        return Supervision(
            "openai_runtime", cap_ref=cap_ref, h_ref=1.0 / uplift_ref, halving=1.0 / float(slope)
        )
    idx = cal["anthropic_automation_index"]
    ht = cal["human_time_per_unit_work"]
    pts, al3_plus = idx["al4_share"], idx["al3_plus_share_aug_2026"]
    if kind == "gdm":
        # Google DeepMind's pull requests, read on the same levels: fully delegated ones are
        # AI-led work (AL4), and those with over 75% of the code written by AI are AL3 or above.
        rows = read_data("gdm_pull_requests_by_ai_share.csv")
        pts = [
            dict(date=float(r["decimal_year"]), share=float(r["ai_100pct_under_3_human_turns"]))
            for r in rows
        ]
        al3_plus = sum(
            float(rows[-1][c])
            for c in (
                "ai_100pct_under_3_human_turns",
                "ai_over_98pct_under_10_human_turns",
                "ai_over_75pct",
            )
        )
    x = np.array([cap_at(p["date"]) for p in pts])
    y = np.array([logit(p["share"]) for p in pts])
    k, b = np.polyfit(x, y, 1)  # logit(share) = k * cap + b
    mid4 = -b / k
    d_first, d_last = pts[0]["date"], pts[-1]["date"]
    cap_per_year = (cap_at(d_last) - cap_at(d_first)) / (d_last - d_first)
    lag_months = idx["al5_lag_behind_al4_months"] if al5_lag_months is None else al5_lag_months
    # AL3+ share is known at one date; assume the same slope and solve its offset.
    lead3 = logit(al3_plus) / k - (cap_at(d_last) - mid4)
    sup = Supervision(
        "anthropic",
        k=float(k),
        mid4=float(mid4),
        lag5=lag_months / 12.0 * cap_per_year,
        lead3=float(lead3),
        h2=ht["al2_or_less"],
        h3=ht["al3"],
        h4=ht["al4"] if h4 is None else h4,
        al5_ceiling=al5_ceiling,
    )
    sup.scale = 1.0 / (uplift_ref * sup.raw(cap_ref))
    return sup


# --------------------------------------------------------------------------
# Model A
# --------------------------------------------------------------------------
@dataclass
class ModelA:
    """Cobb-Douglas research production with Jones-style diminishing returns.

    research effort   RE = RE_cf(t) * F(labor multiple, compute multiple)
    F                 labor**alpha * compute**(1 - alpha)   (CES if rho != 0)
    research stock    dRS/dt = RE
    software pace     (RE / RS) / g_R      (1.0 on the no-AI path)
    overall pace      sigma * software pace + (1 - sigma) * training-compute pace
    AI feedback       labor uplift potential 1 + u0 * 2 ** (Y / D_U)
    """

    alpha: float = 0.5
    rho: float = 0.0
    sigma: float = 2.0 / 3.0
    g_R: float = LN2
    g_X: float = math.log(3.3)  # experiment compute growth, for the freeze policy
    g_C: float = math.log(3.5)  # training compute growth, to convert a cut to baseline-years
    u0: float = 0.2  # excess labor uplift at t0
    D_U: float = 0.45  # baseline-years of progress per doubling of excess uplift
    t0: float = 2025.0
    t_ref: float = 2026.83
    sar_uplift: float = 1000.0
    supervision: Supervision = field(default_factory=Supervision)
    changes: Gate | None = None  # deployed-change counts, for reporting when no gate is enforced
    labor_ref: float = 1.0  # labor uplift at t_ref, where those counts hold

    # ---- pieces -----------------------------------------------------------
    def uplift_cap(self, Y: float) -> float:
        return 1.0 + self.u0 * 2.0 ** (min(Y, 60.0) / self.D_U)

    def effort(self, labor, compute: float = 1.0):
        """Research effort multiple F for a labor multiple (array) and compute multiple."""
        labor = np.asarray(labor, dtype=float)
        if abs(self.rho) < 1e-9:
            return labor**self.alpha * compute ** (1.0 - self.alpha)
        return (self.alpha * labor**self.rho + (1.0 - self.alpha) * compute**self.rho) ** (
            1.0 / self.rho
        )

    @property
    def Y_sar(self) -> float:
        return self.D_U * math.log2((self.sar_uplift - 1.0) / self.u0)

    def tau(self, cap: float, supervised: bool) -> float:
        """Human time per unit of work: capability limit or supervision, whichever binds."""
        t = 1.0 / self.uplift_cap(cap)
        if supervised and self.supervision.kind != "none":
            t = max(t, self.supervision.h(cap))
        return t

    # ---- simulation -------------------------------------------------------
    def simulate(
        self,
        policy: Policy | None = None,
        t_end: float = 2032.0,
        supervised_from: float | None = None,
        max_pace: float = 300.0,
        dY_step: float = 0.004,
        dt_max: float = 0.004,
    ) -> dict:
        """Integrate from t0. Supervision applies from `supervised_from` (default t_ref)."""
        pol = policy or Policy()
        sup_from = self.t_ref if supervised_from is None else supervised_from
        g = self.g_R
        t, S, C, RS = self.t0, 0.0, 0.0, 1.0  # RS_cf(t) = exp(g (t - t0)), RE_cf = g * RS_cf
        hist_t, hist_Y = [t], [0.0]
        Y_best = 0.0
        rows = []
        cut_applied = False
        cap_start = None
        while t < t_end:
            active = t >= pol.start
            # training and experiment compute relative to the unpaced path
            x, pace_C = 1.0, 1.0
            if active and pol.compute_cut != 1.0:
                x = 1.0 / pol.compute_cut
                if not cut_applied:
                    C -= math.log(pol.compute_cut) / self.g_C
                    cut_applied = True
            if active and pol.compute_freeze:
                x = math.exp(-self.g_X * (t - pol.start))
                pace_C = 0.0
            Y = self.sigma * S + (1.0 - self.sigma) * C
            Y_best = max(Y_best, Y)  # the best model so far stays usable
            cap = Y_best
            if active and pol.lag > 0.0:
                cap = float(np.interp(t - pol.lag, hist_t, hist_Y))
            tau = self.tau(cap, supervised=t >= sup_from)

            def f(labor, compute=x):
                return self.effort(labor, compute)

            if active and cap_start is None:
                cap_start = Y_best
            free_labor = 1.0 / tau
            F_free = float(f(np.array([free_labor]))[0])
            spec = pol.gate if (active and pol.gate is not None) else None
            if spec is not None:
                out = gate(tau, f, self.labor_ref, spec, spec.hours_multiplier(Y_best, cap_start))
                F, theta, labor, kept = out["effort"], out["theta"], out["labor"], out["kept"]
                comp, deployed, experiments = (
                    out["comprehension_share"],
                    out["deployed"],
                    out["experiments"],
                )
            else:
                F, theta, labor, kept, comp = F_free, 1.0, free_labor, 1.0, 0.0
                deployed = experiments = float("nan")
                if self.changes is not None and t >= self.t_ref:
                    d = free_deployment(self.changes, labor, self.labor_ref)
                    deployed, experiments = d["deployed"], d["experiments"]
                    comp = d["hours_if_understood"] / self.changes.hours_per_year
            RE = g * math.exp(g * (t - self.t0)) * F
            pace_S = RE / (RS * g)
            pace = self.sigma * pace_S + (1.0 - self.sigma) * pace_C
            rows.append(
                (
                    t,
                    Y_best,
                    pace,
                    pace_S,
                    F,
                    labor,
                    self.uplift_cap(cap),
                    tau,
                    theta,
                    kept,
                    F_free,
                    comp,
                    deployed,
                    experiments,
                )
            )
            if pace > max_pace:
                break
            dt = min(dt_max, dY_step / max(pace, 1e-9))
            RS += RE * dt
            S += pace_S * dt
            C += pace_C * dt
            t += dt
            hist_t.append(t)
            hist_Y.append(max(Y_best, self.sigma * S + (1.0 - self.sigma) * C))
        cols = [
            "t",
            "Y",
            "pace",
            "pace_software",
            "rd_uplift",
            "labor",
            "uplift_cap",
            "tau",
            "theta",
            "kept",
            "rd_free",
            "comprehension_share",
            "deployed",
            "experiments",
        ]
        out = {c: np.array([r[i] for r in rows]) for i, c in enumerate(cols)}
        out["policy"] = pol
        out["ran_away"] = bool(out["pace"][-1] > max_pace)
        return out

    def capability_at(self, hist: dict):
        return lambda date: float(np.interp(date, hist["t"], hist["Y"]))


# --------------------------------------------------------------------------
# Reading results
# --------------------------------------------------------------------------
def first_crossing(t: np.ndarray, series: np.ndarray, level: float) -> float:
    """First time `series` reaches `level`; nan if it never does."""
    above = np.nonzero(series >= level)[0]
    if len(above) == 0:
        return float("nan")
    i = int(above[0])
    if i == 0:
        return float(t[0])
    f = (level - series[i - 1]) / (series[i] - series[i - 1])
    return float(t[i - 1] + f * (t[i] - t[i - 1]))


def value_at(t: np.ndarray, series: np.ndarray, when: float) -> float:
    if when > t[-1]:
        return float("nan")
    return float(np.interp(when, t, series))


def summarize_a(model: ModelA, run: dict) -> dict:
    t = run["t"]
    return {
        "pace_2027.5": value_at(t, run["pace"], 2027.5),
        "pace_2028.0": value_at(t, run["pace"], 2028.0),
        "labor_uplift_2028.0": value_at(t, run["labor"], 2028.0),
        "t_pace_3x": first_crossing(t, run["pace"], 3.0),
        "t_pace_10x": first_crossing(t, run["pace"], 10.0),
        "t_sar": first_crossing(t, run["Y"], model.Y_sar),
        "Y_2028.0": value_at(t, run["Y"], 2028.0),
        "Y_2029.0": value_at(t, run["Y"], 2029.0),
        "min_kept": float(run["kept"].min()),
        "ran_away": run["ran_away"],
    }


# --------------------------------------------------------------------------
# Calibration of Model A
# --------------------------------------------------------------------------
def calibrate_a(
    cal: dict,
    pace_ref: float | None = None,
    pace_mid: float | None = None,
    D_U: float | None = None,
    **overrides,
) -> ModelA:
    """Choose u0 and D_U so the unmodified model reproduces the two pace estimates.

    If D_U is given, only u0 is solved, against the reference-date pace alone.
    """
    p, pr = cal["pace"], cal["production"]
    pace_ref = p["ai_attributable"] if pace_ref is None else pace_ref
    if pace_mid is None:
        # keep the same share of the acceleration six months earlier
        frac = (p["ai_attributable_six_months_earlier"] - 1.0) / (p["ai_attributable"] - 1.0)
        pace_mid = 1.0 + frac * (pace_ref - 1.0)
    base = dict(
        alpha=pr["labor_exponent"],
        sigma=pr["software_share_of_progress"],
        g_R=LN2 * pr["research_stock_doublings_per_year"],
        g_X=math.log(pr["experiment_compute_growth_per_year"]),
        g_C=math.log(pr["training_compute_growth_per_year"]),
        t_ref=cal["reference_date"],
        sar_uplift=cal["milestones"]["sar_labor_uplift"],
    )
    base.update(overrides)
    t_mid, t_ref = p["date_six_months_earlier"], base["t_ref"]

    if D_U is not None:

        def miss(z):
            m = ModelA(u0=math.exp(z), D_U=D_U, **base)
            r = m.simulate(t_end=t_ref + 0.02, supervised_from=1e9)
            v = value_at(r["t"], r["pace"], t_ref)
            return 1e3 if v != v else v - pace_ref  # nan means the run diverged early

        return ModelA(u0=math.exp(brentq(miss, math.log(1e-6), math.log(5.0))), D_U=D_U, **base)

    def resid(z):
        m = ModelA(u0=math.exp(z[0]), D_U=math.exp(z[1]), **base)
        r = m.simulate(t_end=t_ref + 0.02, supervised_from=1e9)
        return [
            value_at(r["t"], r["pace"], t_mid) - pace_mid,
            value_at(r["t"], r["pace"], t_ref) - pace_ref,
        ]

    sol = least_squares(resid, x0=[math.log(0.3), math.log(0.5)], xtol=1e-10, ftol=1e-10)
    if max(abs(v) for v in sol.fun) > 1e-3:
        raise RuntimeError(f"Model A calibration did not converge: residuals {sol.fun}")
    return ModelA(u0=math.exp(sol.x[0]), D_U=math.exp(sol.x[1]), **base)


def build_a(
    cal: dict,
    supervision: str = "anthropic",
    al5_lag_months: float | None = None,
    h4: float | None = None,
    al5_ceiling: float = 1.0,
    openai_from: float = 0.0,
    **kw,
) -> tuple[ModelA, dict]:
    """Calibrated Model A with a fitted supervision schedule. Returns (model, history)."""
    m = calibrate_a(cal, **kw)
    hist = m.simulate(t_end=m.t_ref + 0.02, supervised_from=1e9)
    cap_ref = value_at(hist["t"], hist["Y"], m.t_ref)
    m.labor_ref = m.uplift_cap(cap_ref)
    m.changes = gate_from_calibration(cal)
    m.supervision = fit_supervision(
        supervision,
        m.capability_at(hist),
        cap_ref,
        m.uplift_cap(cap_ref),
        cal,
        al5_lag_months=al5_lag_months,
        h4=h4,
        al5_ceiling=al5_ceiling,
        openai_from=openai_from,
    )
    return m, hist


def standard_policies(cal: dict) -> list[Policy]:
    c, o, start = cal["comprehension_gate"], cal["other_mechanisms"], cal["policy_start"]
    g = gate_from_calibration(cal)
    lag = o["internal_use_lag_months"] / 12.0
    short = o["internal_use_lag_months_short"]
    cut = o["rd_compute_cut_factor"]
    leak = 1.0 / (1.0 - (1.0 - 1.0 / cut) * (1.0 - o["scoped_control_substitution"]))
    return [
        Policy("No pacing", start=start),
        Policy(
            "Human sign-off, no comprehension standard",
            start=start,
            gate=replace(g, signoff_hours=c["signoff_hours_per_change"]),
        ),
        Policy(
            "Comprehension audits, light",
            start=start,
            gate=replace(g, hours_scale=c["light_scale"]),
        ),
        Policy("Comprehension audits, central", start=start, gate=g),
        Policy(
            "Comprehension audits, strict",
            start=start,
            gate=replace(g, hours_scale=c["strict_scale"]),
        ),
        Policy(f"Internal-use lag, {short} months", start=start, lag=short / 12.0),
        Policy(f"Internal-use lag, {o['internal_use_lag_months']} months", start=start, lag=lag),
        Policy(f"R&D compute cut {cut:g}x", start=start, compute_cut=cut),
        Policy("R&D compute frozen", start=start, compute_freeze=True),
        Policy(f"R&D compute cut {cut:g}x, scoped and substituted", start=start, compute_cut=leak),
        Policy(
            f"Comprehension audits (central) + {short}-month lag",
            start=start,
            gate=g,
            lag=short / 12.0,
        ),
        Policy(
            f"Comprehension audits (central) + {o['internal_use_lag_months']}-month lag",
            start=start,
            gate=g,
            lag=lag,
        ),
    ]


MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def fmt_date(x: float) -> str:
    if x != x:
        return "not by 2032"
    year = int(math.floor(x))
    month = min(11, int((x - year) * 12))
    return f"{MONTHS[month]} {year}"
