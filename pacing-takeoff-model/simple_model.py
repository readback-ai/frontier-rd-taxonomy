"""A small model of how pacing mechanisms change the takeoff of automated AI R&D.

One state variable, five ideas, numpy only. It is the short version of the two full models in
this directory, and it keeps the parts their results turn on.

1. The loop. Better AI adds research input, research input makes software progress, and
   progress makes better AI. Research gets harder as it goes: each year of software progress
   ahead of the historical schedule halves what a unit of research input buys.

       software pace = research input / 2 ** (years of software progress ahead of schedule)

2. AI labor helps up to a ceiling. AI labor per researcher doubles every `uplift_doubling`
   years of progress. Its effect on research has diminishing returns and tops out at
   `labor_ceiling`, because experiments need compute.

3. Judgment has no ceiling, and it comes in two kinds. Research input is multiplied by the
   lab's research judgment. On supervisable tasks people can judge the work, and AI judgment
   improves at one rate. On hard-to-supervise (HTS) fuzzy tasks there are no clear criteria
   and human judgment is systematically flawed, and AI judgment improves at a slower rate.
   Supervisable work stands in for HTS fuzzy work poorly, so the slower rate ends up setting
   the pace. A share of work also needs a person until AI judgment on HTS fuzzy tasks catches
   up.

4. Understanding takes people's time. The count of deployed changes grows with AI labor. The
   hours it takes a person to understand one do not shrink.

5. The lab chooses. Under comprehension audits a lab may deploy only what its people
   understand. It splits researcher time between research and understanding to go fastest,
   and it understands the most valuable changes first.

Progress is measured in years of progress at the rate before October 2025. Pace is years of
progress per calendar year. Run this file to print the scenario table.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np

T_BASE = 2025.75  # Oct 1, 2025: the pace is 1 up to here
T_MAY, T_REF = 2026.33, 2026.83  # May 1 and Nov 1, 2026: the two dates with a measured pace
PACE_MAY, PACE_REF = 1.2, 1.7
SD_RESEARCHER, SD_TED = 3.09, 7.72  # AI Futures' levels for the two milestones, in researcher SD
THETA = np.linspace(0.0, 0.95, 96)  # shares of researcher time a lab can give to understanding
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


@dataclass(frozen=True)
class Params:
    # 1. The loop
    software_share: float = 2 / 3  # share of progress from software; the rest is more compute
    stock_doublings: float = 1.0  # halvings of research productivity per year ahead of schedule
    # 2. AI labor
    labor_exponent: float = 0.5  # research input rises with the square root of labor
    labor_ceiling: float = 15.0  # most that unlimited labor can multiply research input by
    u0: float = 0.2522  # AI labor per researcher, less one, on Oct 1, 2025. Fitted to the pace
    uplift_doubling: float = 0.2471  # years of progress per doubling of AI labor. Fitted
    progress_at_ref: float = 1.3327  # years of progress from Oct 1, 2025 to Nov 1, 2026. Fitted
    # 3. Judgment
    judgment_start: float = -3.5  # AI research judgment on Nov 1, 2026, in researcher SD
    supervisable_rate: float = 3.0  # SD gained per year of progress on supervisable tasks
    hts_fuzzy_rate: float = (
        1.0  # the same on HTS fuzzy tasks. Equal rates give one kind of judgment
    )
    supervisable_weight: float = 0.8  # weight of supervisable work in research
    substitution: float = (
        0.25  # how well supervisable work stands in for HTS fuzzy work. 1 is neutral
    )
    value_per_sd: float = 0.445  # log research value of one SD of judgment
    residue: float = 0.14  # share of work that needs a person on Nov 1, 2026
    supervision_time: float = 0.005  # a person's time on that work, as a share of doing it
    # 4. Understanding
    understanding_today: float = 0.14  # share of researcher time spent understanding changes
    change_growth: float = 0.4  # percent more deployed changes per percent more AI labor
    tail: float = 1.8  # Pareto index of a change's value. Lower means a few changes matter most


@dataclass(frozen=True)
class Policy:
    name: str = "No pacing"
    start: float = 2027.0
    audit_hours: float = 0.0  # 0 is no audit; 1 is the central standard; 2 is twice the hours
    lag: float = 0.0  # years by which the AI a lab may use internally trails its newest
    compute_cut: float = 1.0  # factor by which experiment compute is cut


POLICIES = (
    Policy(),
    Policy("Comprehension audits, light", audit_hours=0.5),
    Policy("Comprehension audits, central", audit_hours=1.0),
    Policy("Comprehension audits, strict", audit_hours=2.0),
    Policy("Internal-use lag, 3 months", lag=0.25),
    Policy("Internal-use lag, 9 months", lag=0.75),
    Policy("R&D compute cut 3x", compute_cut=3.0),
    Policy("Comprehension audits (central) + 9-month lag", audit_hours=1.0, lag=0.75),
)


def share_above(sd: float) -> float:
    """Share of researchers whose judgment is better than `sd`."""
    return 0.5 * math.erfc(sd / math.sqrt(2.0))


def lab_judgment(ai_sd: float, k: float) -> float:
    """Average research value across a lab whose researchers each use the better of their own
    judgment and the AI's. Researchers' judgment is standard normal and value is exp(k * SD)."""
    return math.exp(k * ai_sd) * (1.0 - share_above(ai_sd)) + math.exp(0.5 * k * k) * share_above(
        ai_sd - k
    )


def combine(supervisable: float, hts_fuzzy: float, p: Params) -> float:
    """Judgment across the two kinds of task when the lab spreads its experiments to get the
    most from them. Below a substitution of 1 the weaker kind pulls the result down."""
    r = p.substitution - 1.0
    w = p.supervisable_weight
    if abs(r) < 1e-9:
        return supervisable**w * hts_fuzzy ** (1.0 - w)
    return (w * supervisable**r + (1.0 - w) * hts_fuzzy**r) ** (1.0 / r)


def labor_effect(labor, p: Params):
    """Research input from labor: the square root at first, flattening at the ceiling."""
    x = np.asarray(labor, dtype=float) ** p.labor_exponent
    return x * p.labor_ceiling / (x + p.labor_ceiling)


def ai_labor(progress: float, hts_fuzzy_sd: float, p: Params) -> float:
    """AI labor per researcher. The share of work that needs a person holds it down."""
    labor = 1.0 + p.u0 * 2.0 ** (min(progress, 200.0) / p.uplift_doubling)
    if p.residue > 0.0:
        needs_person = p.residue * share_above(hts_fuzzy_sd) / share_above(p.judgment_start)
        labor = min(labor, 1.0 / max(needs_person * p.supervision_time, 1e-12))
    return labor


def simulate(p: Params, policy: Policy | None = None, t_end: float = 2046.0, dt: float = 0.002):
    """Integrate from Oct 1, 2025. Returns the path and the date of each milestone."""
    policy = policy or Policy()
    k, a, w = p.value_per_sd, p.labor_exponent, p.software_share
    base_labor = float(labor_effect(1.0 + p.u0, p))
    base_judgment = math.exp(0.5 * k * k)
    labor_at_ref = 1.0 + p.u0 * 2.0 ** (p.progress_at_ref / p.uplift_doubling)
    value_power = 1.0 - 1.0 / p.tail  # the best share q of changes holds q ** value_power of value
    levels = {
        "researcher": math.exp(k * SD_RESEARCHER),
        "ted_ai": math.exp(k * SD_TED),
    }
    n = int(round((t_end - T_BASE) / dt))
    start_step = int(round((policy.start - T_BASE) / dt))
    lag_steps = int(round(policy.lag / dt))
    out = {key: np.full(n, np.nan) for key in ("t", "progress", "pace", "labor", "supervisable_sd")}
    out.update(
        {key: np.full(n, np.nan) for key in ("hts_fuzzy_sd", "understood", "time_understanding")}
    )
    dates = dict.fromkeys(levels, math.nan)
    software, last = 0.0, n
    for i in range(n):
        t = T_BASE + i * dt
        elapsed = t - T_BASE
        progress = w * software + (1.0 - w) * elapsed
        out["t"][i], out["progress"][i] = t, progress
        paced = i >= start_step
        # The AI the lab may use. Under a lag it is the AI of `lag` years ago, and no older
        # than the AI it had when the policy started.
        used = out["progress"][min(i, max(start_step, i - lag_steps))] if paced else progress
        supervisable_sd = p.judgment_start + p.supervisable_rate * (used - p.progress_at_ref)
        hts_fuzzy_sd = p.judgment_start + p.hts_fuzzy_rate * (used - p.progress_at_ref)
        labor = ai_labor(used, hts_fuzzy_sd, p)
        judgment = (
            combine(lab_judgment(supervisable_sd, k), lab_judgment(hts_fuzzy_sd, k), p)
            / base_judgment
        )
        compute = 1.0 / policy.compute_cut if paced else 1.0
        understood, theta = 1.0, p.understanding_today
        effort = float(labor_effect(labor, p))
        if paced and policy.audit_hours > 0.0:
            # Researchers who spend more time understanding direct less AI labor, and the lab
            # then deploys fewer changes. `everything` is the time to understand all of them,
            # as a share of researcher time.
            time = np.maximum(THETA, p.understanding_today)
            directed = labor * (1.0 - time) / (1.0 - p.understanding_today)
            everything = (
                policy.audit_hours
                * p.understanding_today
                * (directed / labor_at_ref) ** p.change_growth
            )
            q = np.minimum(1.0, THETA / everything)
            kept = q**value_power * labor_effect(directed, p)
            best = int(np.argmax(kept))
            effort, understood, theta = float(kept[best]), float(q[best]), float(time[best])
        research = effort / base_labor * judgment * compute ** (1.0 - a)
        software_pace = research / 2.0 ** (p.stock_doublings * (software - elapsed))
        pace = w * software_pace + (1.0 - w)
        for key, value in (
            ("pace", pace),
            ("labor", labor),
            ("supervisable_sd", supervisable_sd),
            ("hts_fuzzy_sd", hts_fuzzy_sd),
            ("understood", understood),
            ("time_understanding", theta),
        ):
            out[key][i] = value
        # Milestones are about the newest AI, whatever the lab is allowed to use.
        newest = (
            p.judgment_start + rate * (progress - p.progress_at_ref)
            for rate in (p.supervisable_rate, p.hts_fuzzy_rate)
        )
        ai_only = combine(*(math.exp(k * sd) for sd in newest), p)
        for name, level in levels.items():
            if dates[name] != dates[name] and ai_only >= level:
                dates[name] = t
        if pace > 1e4 or dates["ted_ai"] == dates["ted_ai"]:
            last = i + 1
            break
        software += software_pace * dt
    out = {key: value[:last] for key, value in out.items()}
    ran_away = bool(out["pace"][-1] > 1e4)
    if ran_away:  # everything left arrives at once
        dates = {
            name: (when if when == when else float(out["t"][-1])) for name, when in dates.items()
        }
    return dict(out, dates=dates, ran_away=ran_away)


def pace_on(run: dict, date: float) -> float:
    return float(np.interp(date, run["t"], run["pace"]))


def calibrate(p: Params) -> Params:
    """Fit AI labor on Oct 1, 2025 and its doubling to the pace measured in May and November
    2026: for each doubling, bisect the level to hit November, then bisect the doubling to hit
    May."""

    def fit_level(doubling: float) -> Params:
        # Above about 0.5 the level stops raising the pace, because the pace is measured
        # against Oct 1, 2025, when the same AI labor was already there.
        lo, hi = 1e-6, 0.5
        for _ in range(50):
            mid = math.sqrt(lo * hi)
            trial = replace(p, u0=mid, uplift_doubling=doubling, residue=0.0)
            if pace_on(simulate(trial, t_end=T_REF + 0.01), T_REF) > PACE_REF:
                hi = mid
            else:
                lo = mid
        return replace(p, u0=math.sqrt(lo * hi), uplift_doubling=doubling)

    lo, hi = 0.05, 2.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        run = simulate(replace(fit_level(mid), residue=0.0), t_end=T_REF + 0.01)
        # A slower doubling needs a higher level to hit November, so May runs hotter. If no
        # level hits November, the doubling is too slow as well.
        if pace_on(run, T_REF) < PACE_REF - 1e-3 or pace_on(run, T_MAY) > PACE_MAY:
            hi = mid
        else:
            lo = mid
    fitted = fit_level(0.5 * (lo + hi))
    run = simulate(replace(fitted, residue=0.0), t_end=T_REF + 0.01)
    return replace(fitted, progress_at_ref=float(np.interp(T_REF, run["t"], run["progress"])))


def steady_pace(rate: float, p: Params) -> float:
    """Where the pace settles once AI labor is at its ceiling and judgment improves `rate` SD
    per year of progress. Infinite at or above the critical rate."""
    doublings = p.value_per_sd * rate / math.log(2.0) / p.stock_doublings
    w = p.software_share
    if w * doublings >= 1.0:
        return math.inf
    software = (1.0 + doublings * (1.0 - w)) / (1.0 - w * doublings)
    return w * software + (1.0 - w)


def critical_rate(p: Params) -> float:
    """Judgment gained per year of progress above which the loop runs away on judgment alone."""
    return math.log(2.0) * p.stock_doublings / (p.value_per_sd * p.software_share)


def fmt_date(x: float) -> str:
    if x != x:
        return "after 2045"
    year = int(x)
    return f"{MONTHS[min(11, int((x - year) * 12))]} {year}"


def fmt_delay(base: float, paced: float) -> str:
    if base != base:
        return ""
    return "past 2045" if paced != paced else f"{(paced - base) * 12:+.0f} mo"


TASTES = (
    ("One kind of judgment, +3 SD a year", dict(supervisable_rate=3.0, hts_fuzzy_rate=3.0)),
    ("One kind of judgment, +1 SD a year", dict(supervisable_rate=1.0, hts_fuzzy_rate=1.0)),
    ("Supervisable +3, HTS fuzzy +1 SD a year", dict(supervisable_rate=3.0, hts_fuzzy_rate=1.0)),
    ("Supervisable +3, HTS fuzzy +0.5 SD a year", dict(supervisable_rate=3.0, hts_fuzzy_rate=0.5)),
)


def table(p: Params | None = None) -> str:
    p = p or Params()
    out = [
        "# Simple model: milestone dates by scenario",
        "",
        "Written by `simple_model.py`. Do not edit by hand.",
        "",
        "Delays are against no pacing. Pacing starts Jan 1, 2027. Critical rate: "
        f"{critical_rate(p):.2f} SD per year of progress. Above it the loop runs away on "
        "judgment alone.",
        "",
    ]
    for label, rates in TASTES:
        q = replace(p, **rates)
        base = simulate(q)["dates"]
        settled = steady_pace(q.hts_fuzzy_rate, q)
        settled = "runs away" if settled == math.inf else f"{settled:.1f}x"
        out += [
            f"### {label}",
            "",
            f"Pace once AI labor is at its ceiling: {settled}.",
            "",
            "| Scenario | Researcher-level AI | Delay | TED-AI | Delay |",
            "|---|---|---|---|---|",
        ]
        for policy in POLICIES:
            d = simulate(q, policy)["dates"]
            first = policy.name == "No pacing"
            cells = [policy.name]
            for name in ("researcher", "ted_ai"):
                cells += [fmt_date(d[name]), "" if first else fmt_delay(base[name], d[name])]
            out.append("| " + " | ".join(cells) + " |")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    print(table())
