"""A standalone model of automated AI research as a chain from small experiments to real value.

One file, numpy and the standard library. It imports none of the other models here.

Experiments at scale are limited by compute. Behind each one the lab runs many small
experiments, picks the candidate that looks best, and runs it at scale. Two links separate how
good a candidate looks from what it is worth:

    small-scale result  ->  result on the metric at scale  ->  real value
                     transfer                            validity

1. Throughput. AI labor raises the number of experiments a lab gets from its compute, with
   diminishing returns and a ceiling, as in the AI Futures Model.

2. Candidates. AI labor multiplies the small experiments behind each experiment at scale. The
   best of n candidates is about sqrt(2 ln n) SD better than a typical one, so volume helps
   less and less. AI also proposes better candidates as its judgment on well-defined problems
   improves. That judgment has no ceiling, as in the AI Futures Model.

3. Transfer. Only part of a small-scale gain holds at scale. How much depends on who judged
   which candidate would transfer.

4. Validity. Only part of a gain on the metric is real. How much depends on who defined the
   metric and checked the result for gaming.

5. People's time. A person who judges an experiment supplies both links. Researchers judge as
   many experiments as they have time for, and the AI judges the rest with its own transfer
   and metric judgment. AI takes over implementation, which frees researcher time. More
   experiments and more candidates behind each use it up.

6. What people can vouch for. People's judgment applies to gains up to what their best
   researcher could have proposed. The AI judges any gain beyond that.

7. The loop. Real research makes software progress, and progress makes better AI.

8. Difficulty. Research gets harder as software advances: each year of software progress
   halves what a unit of research buys, `difficulty` times over. A lab's other inputs,
   compute and people, have grown fast enough to offset that, which is what a pace of 1
   means. Whether the loop runs away or peters out turns on whether the AI's judgment adds
   research faster than difficulty takes it away.

       software pace = research * other inputs / 2 ** (difficulty * software progress)

The links multiply in the exponent of an experiment's value:

    value = exp(kept * (standing + gain) - standing),    kept = transfer * validity

with transfer and validity measured against people's. `standing` is what an experiment was
worth before October 2025 and `gain` is what has been added at small scale since. An
experiment people judged keeps all of it, which is the AI Futures Model's case. One left to an
AI with weak transfer and metric judgment keeps part.

Under comprehension audits researchers must also understand what is deployed, and that time
comes out of judging.

Progress is in years of progress at the rate before October 2025. Pace is years of progress
per calendar year. Run this file to print the scenario tables.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from statistics import NormalDist

import numpy as np

T_BASE = 2025.75  # Oct 1, 2025: the pace is 1 up to here
T_MAY, T_REF = 2026.33, 2026.83  # May 1 and Nov 1, 2026: the two dates with a measured pace
PACE_MAY, PACE_REF = 1.2, 1.7
LABOR_REF = 13.0  # agent workdays per researcher workday on Nov 1, 2026: OpenAI's trend
# The two milestone levels are the AI Futures Project's, in SD of researcher judgment. In its
# public code (github.com/AI-Futures-Project, `progress_model/config.py` and `_impl.py`) both
# are levels of AI research taste.
# - The top researcher is the 99.9th percentile of a normal distribution, +3.09 SD. The code
#   names it TOP_RESEARCHER_SD and marks its superhuman AI researcher there.
# - TED-AI is `ted_ai_m2b` gaps of that size further on. The value below is the one in the
#   parameters of the example trajectory in the project's update of November 10, 2026, and it
#   is a forecaster's judgment. The code's default is 1.00, which puts TED-AI at +6.18 SD.
TOP_PERCENTILE = 0.999
TED_GAPS_ABOVE_TOP = 1.4966629547095764
SD_RESEARCHER = NormalDist().inv_cdf(TOP_PERCENTILE)  # +3.09
SD_TED = SD_RESEARCHER * (1.0 + TED_GAPS_ABOVE_TOP)  # +7.72
SHARES = np.linspace(0.0, 1.0, 201)  # shares of the audit load a lab can choose to carry
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
_NORMAL = NormalDist()


@dataclass(frozen=True)
class Params:
    # The loop
    software_share: float = 2 / 3  # share of progress from software; the rest is more compute
    difficulty: float = 1.0  # halvings of what research buys per year of software progress
    # Throughput
    labor_exponent: float = 0.5  # experiments rise with the square root of AI labor
    labor_ceiling: float = 15.0  # most that unlimited labor can multiply experiments by
    u0: float = 0.103914  # AI labor per researcher on Oct 1, 2025. Fitted
    uplift_doubling: float = 0.193653  # years of progress per doubling of AI labor. Fitted
    progress_at_ref: float = 1.349178  # years of progress from Oct 1, 2025 to Nov 1, 2026. Fitted
    compute_doublings: float = 1.5  # doublings of compute per year on the historical schedule
    compute_slows_in: float = math.inf  # year from which compute grows at `compute_slow_pace`
    compute_slow_pace: float = 0.5  # that growth, as a share of the historical rate
    # Candidates
    candidates_base: float = 20.0  # small experiments behind each one at scale on Oct 1, 2025
    candidates_max: float = 1e4  # most that small-scale compute allows
    value_of_selection: float = 0.3  # log value of one SD of small-scale result
    value_per_sd: float = 0.445  # log value of one SD of researcher judgment
    # AI judgment, in researcher SD, and what it gains per year of progress
    judgment_start: float = -3.5  # all three kinds on Nov 1, 2026
    idea_rate: float = 3.0  # proposing candidates on a well-defined problem
    transfer_rate: float = 1.0  # judging which small-scale gains hold at scale
    metric_rate: float = 1.0  # defining metrics and debugging results that game them
    # The two links. Only their ratios to people's values enter
    transfer_people: float = 0.7  # share of a small-scale gain that holds at scale, people judging
    transfer_ai_start: float = 0.2  # the same with the AI judging, on Nov 1, 2026
    transfer_max: float = 0.9
    validity_people: float = 0.8  # share of a gain on the metric that is real, people judging
    validity_ai_start: float = 0.05  # the same with the AI judging, on Nov 1, 2026
    validity_max: float = 0.95
    vouch_sd: float = SD_RESEARCHER  # people can vouch for gains up to this researcher's
    # ideas, in SD. The default is the top researcher
    # People's time
    time_judging: float = 0.4  # share of researcher time on results, metrics and plans on
    # Oct 1, 2025. The rest was implementation
    volume_elasticity: float = 0.004869  # percent more judging time per experiment at scale per
    # percent more candidates behind it, net of AI help with the analysis. Fitted
    # Comprehension audits
    understanding_today: float = 0.14  # time to understand all deployed changes, Nov 1, 2026
    change_growth: float = 0.4  # percent more deployed changes per percent more AI labor
    tail: float = 1.8  # Pareto index of a change's value. Lower means a few changes matter most
    audit_credit: float = 0.5  # share of audit time that also counts as judging experiments


@dataclass(frozen=True)
class Policy:
    name: str = "No pacing"
    start: float = 2027.0
    audit_hours: float = 0.0  # 0 is no audit; 1 is the central standard; 2 is twice the hours
    lag: float = 0.0  # years by which the AI a lab may use internally trails its newest
    compute_share: float = 1.0  # share of its scheduled compute a lab may use for research
    # and for training
    compute_cap: float = math.inf  # most compute it may use for them, as a multiple of what it
    # used when the policy started


POLICIES = (
    Policy(),
    Policy("Comprehension audits, light", audit_hours=0.5),
    Policy("Comprehension audits, central", audit_hours=1.0),
    Policy("Comprehension audits, strict", audit_hours=2.0),
    Policy("Internal-use lag, 3 months", lag=0.25),
    Policy("Internal-use lag, 9 months", lag=0.75),
    Policy("R&D compute at a third of baseline", compute_share=1 / 3),
    Policy("R&D compute frozen at its Jan 2027 level", compute_cap=1.0),
    Policy("R&D compute frozen at a third of its Jan 2027 level", compute_cap=1 / 3),
    Policy("Comprehension audits (central) + 9-month lag", audit_hours=1.0, lag=0.75),
)


def best_of(n: float) -> float:
    """Expected best of n draws from a standard normal, in SD (Blom's approximation)."""
    n = max(n, 1.0)
    return _NORMAL.inv_cdf((n - 0.375) / (n + 0.25))


def capped_exp(x: float) -> float:
    """exp that stays finite while a run that has run away takes its last steps."""
    return math.exp(min(x, 600.0))


def share_above(sd: float) -> float:
    """Share of researchers whose judgment is better than `sd`."""
    return 0.5 * math.erfc(sd / math.sqrt(2.0))


def lab_judgment(ai_sd: float, k: float) -> float:
    """Average value of the candidates a lab proposes when each researcher uses the better of
    their own judgment and the AI's. Researchers' judgment is standard normal and value is
    exp(k * SD). This is the AI Futures Model's rule."""
    return math.exp(k * ai_sd) * (1.0 - share_above(ai_sd)) + math.exp(0.5 * k * k) * share_above(
        ai_sd - k
    )


def labor_effect(labor: float, p: Params) -> float:
    """Experiments from labor: the square root at first, flattening at the ceiling."""
    x = labor**p.labor_exponent
    return x * p.labor_ceiling / (x + p.labor_ceiling)


def link(sd: float, people: float, ai_start: float, top: float, p: Params) -> float:
    """A link's value with the AI judging: `ai_start` on Nov 1, 2026, people's value when the
    AI's judgment reaches the median researcher, and the same ratio for each SD up to `top`.
    Value is geometric in SD, as research value is in the AI Futures Model."""
    per_sd = math.log(people / ai_start) / -p.judgment_start
    return min(top, people * math.exp(per_sd * sd))


def ai_state(progress: float, p: Params, compute: float = 1.0) -> dict:
    """What an AI at this level of progress supplies. `compute` is the lab's research compute
    against the historical schedule. It scales the AI labor the lab can run and the small
    experiments it can afford."""
    ahead = progress - p.progress_at_ref
    transfer_sd = p.judgment_start + p.transfer_rate * ahead
    metric_sd = p.judgment_start + p.metric_rate * ahead
    labor = 1.0 + compute * p.u0 * 2.0 ** min(progress / p.uplift_doubling, 1000.0)
    # Small experiments grow with AI labor. Experiments at scale grow more slowly, so the
    # candidates behind each one multiply.
    more_labor = labor / (1.0 + p.u0)
    more_at_scale = labor_effect(labor, p) / labor_effect(1.0 + p.u0, p)
    transfer = link(transfer_sd, p.transfer_people, p.transfer_ai_start, p.transfer_max, p)
    validity = link(metric_sd, p.validity_people, p.validity_ai_start, p.validity_max, p)
    return dict(
        labor=labor,
        candidates=min(p.candidates_max * compute, p.candidates_base * more_labor / more_at_scale),
        idea_sd=p.judgment_start + p.idea_rate * ahead,
        transfer_sd=transfer_sd,
        metric_sd=metric_sd,
        transfer=transfer / p.transfer_people,  # against people's
        validity=validity / p.validity_people,
    )


def realized_sd(ai: dict) -> float:
    """Judgment of an AI-only lab in researcher SD: its ideas, times the share of their gain
    that its own transfer and metric judgment keep, against the share people's keep."""
    kept = ai["transfer"] * ai["validity"]
    return ai["idea_sd"] * kept if ai["idea_sd"] > 0.0 else ai["idea_sd"]


def standing(p: Params) -> float:
    """Log value of an experiment before October 2025 that depended on judgment. It is set so
    that an experiment judged by the AI of Nov 1, 2026 is worth what the AI Futures Model gives
    judgment at that AI's level."""
    kept = p.transfer_ai_start * p.validity_ai_start / (p.transfer_people * p.validity_people)
    if kept >= 1.0:  # the AI already judges as well as people, so nothing rests on who judges
        return 0.0
    return -p.value_per_sd * p.judgment_start / (1.0 - kept)


def research(
    ai: dict,
    p: Params,
    experiments: float = 1.0,
    audit_hours: float = 0.0,
    labor_at_ref: float = 1.0,
) -> dict:
    """Research per researcher against Oct 1, 2025, real and as measured on the lab's metrics.

    `experiments` is the number of experiments at scale against that date. Under audits the
    lab chooses the share of its changes to understand and deploy that gives the most
    research."""
    n, n0 = ai["candidates"], p.candidates_base
    # Far past the best researcher every candidate is the AI's, and the rule is exp(k * SD).
    ideas = p.value_per_sd * ai["idea_sd"]
    if ai["idea_sd"] < 20.0:
        ideas = math.log(lab_judgment(ai["idea_sd"], p.value_per_sd))
    ideas -= 0.5 * p.value_per_sd**2
    gain = ideas + p.value_of_selection * (best_of(n) - best_of(n0))  # at small scale
    vouched = min(gain, p.value_per_sd * p.vouch_sd)
    beyond = gain - vouched
    base = standing(p)
    # Once the AI's judgment on a link passes people's, people use it.
    transfer_people = max(1.0, ai["transfer"])
    kept_people = transfer_people * max(1.0, ai["validity"])
    kept_ai = ai["transfer"] * ai["validity"]
    judged = capped_exp(kept_people * (base + vouched) + kept_ai * beyond - base)
    unjudged = capped_exp(kept_ai * (base + gain) - base)
    judged_measured = capped_exp(
        transfer_people * (base + vouched) + ai["transfer"] * beyond - base
    )
    unjudged_measured = capped_exp(ai["transfer"] * (base + gain) - base)
    # Implementation goes to the AI as the candidates multiply, which frees researcher time.
    free = 1.0 - (1.0 - p.time_judging) * n0 / n
    per_experiment = p.time_judging * (n / n0) ** p.volume_elasticity
    if audit_hours > 0.0:
        # `everything` is the time to understand all deployed changes, as a share of
        # researcher time. The lab deploys only what it understands, the most valuable first.
        everything = (
            audit_hours * p.understanding_today * (ai["labor"] / labor_at_ref) ** p.change_growth
        )
        audit = np.minimum(SHARES * everything, free)
        deployed = audit / everything
    else:
        audit, deployed = np.zeros(1), np.ones(1)
    judging = free - (1.0 - p.audit_credit) * audit
    covered = np.minimum(1.0, judging / (per_experiment * experiments))
    kept = deployed ** (1.0 - 1.0 / p.tail)
    real = experiments * kept * (covered * judged + (1.0 - covered) * unjudged)
    measured = (
        experiments * kept * (covered * judged_measured + (1.0 - covered) * unjudged_measured)
    )
    i = int(np.argmax(real))
    return dict(
        real=float(real[i]),
        measured=float(measured[i]),
        covered=float(covered[i]),
        time_audit=float(audit[i]),
        deployed=float(deployed[i]),
    )


KEYS = (
    "t",
    "progress",
    "measured_progress",
    "pace",
    "measured_pace",
    "labor",
    "experiments",
    "candidates",
    "idea_sd",
    "transfer_sd",
    "metric_sd",
    "kept_ai",
    "covered",
    "time_audit",
    "deployed",
)


def simulate(p: Params, policy: Policy | None = None, t_end: float = 2046.0, dt: float = 0.004):
    """Integrate from Oct 1, 2025. Returns the path and the date of each milestone."""
    policy = policy or Policy()
    w = p.software_share
    levels = {"researcher": SD_RESEARCHER, "ted_ai": SD_TED}
    labor_at_ref = ai_state(p.progress_at_ref, p)["labor"]
    base_labor = labor_effect(1.0 + p.u0, p)
    n = int(round((t_end - T_BASE) / dt))
    start_step = int(round((policy.start - T_BASE) / dt))
    lag_steps = int(round(policy.lag / dt))
    out = {key: np.full(n, np.nan) for key in KEYS}
    dates = dict.fromkeys(levels, math.nan)
    # `scheduled` is the compute growth a lab would have with no policy, in years of growth at
    # the historical rate. `hardware` is the part of it that training has used.
    software = measured_software = hardware = scheduled = scheduled_at_start = 0.0
    last = n
    for i in range(n):
        t = T_BASE + i * dt
        elapsed = t - T_BASE
        progress = w * software + (1.0 - w) * hardware
        out["t"][i], out["progress"][i] = t, progress
        out["measured_progress"][i] = w * measured_software + (1.0 - w) * hardware
        paced = i >= start_step
        # The AI the lab may use. Under a lag it is the AI of `lag` years ago, and no older
        # than the AI it had when the policy started.
        j = min(i, max(start_step, i - lag_steps)) if paced else i
        compute_pace = p.compute_slow_pace if t >= p.compute_slows_in else 1.0
        if i == start_step:
            scheduled_at_start = scheduled
        # The compute the lab may use, in the same years of growth. A share of the schedule
        # sets it a fixed number of doublings back. A cap holds it at a level, so a capped lab
        # falls further behind the schedule each year.
        allowed = scheduled
        if paced:
            allowed = min(
                scheduled + math.log2(policy.compute_share) / p.compute_doublings,
                scheduled_at_start + math.log2(policy.compute_cap) / p.compute_doublings,
            )
        # Research compute against the historical schedule.
        compute = 2.0 ** (p.compute_doublings * (allowed - elapsed))
        # Training cannot use more than is allowed, and what it has already used stays used.
        hardware_pace = compute_pace if hardware <= allowed + 1e-9 else 0.0
        ai = ai_state(out["progress"][j], p, compute)
        experiments = (
            labor_effect(ai["labor"], p) / base_labor * compute ** (1.0 - p.labor_exponent)
        )
        lab = research(ai, p, experiments, policy.audit_hours if paced else 0.0, labor_at_ref)
        # Each year of software progress halves what research buys, `difficulty` times over.
        # The lab's other inputs double as often per calendar year, which held the pace at 1
        # before AI helped. Any shortfall in compute is already in `experiments`.
        harder = p.difficulty * (software - elapsed)
        software_pace = lab["real"] / 2.0**harder
        # Measured progress can run far ahead of real progress, so its halvings are capped.
        measured_harder = min(p.difficulty * (measured_software - elapsed), 1000.0)
        measured_pace = lab["measured"] / 2.0**measured_harder
        pace = w * software_pace + (1.0 - w) * hardware_pace
        out["pace"][i] = pace
        out["measured_pace"][i] = w * measured_pace + (1.0 - w) * hardware_pace
        out["experiments"][i] = experiments
        out["kept_ai"][i] = ai["transfer"] * ai["validity"]
        for key in ("labor", "candidates", "idea_sd", "transfer_sd", "metric_sd"):
            out[key][i] = ai[key]
        for key in ("covered", "time_audit", "deployed"):
            out[key][i] = lab[key]
        # Milestones are about the newest AI, whatever the lab is allowed to use.
        newest = realized_sd(ai_state(progress, p))
        for name, level in levels.items():
            if dates[name] != dates[name] and newest >= level:
                dates[name] = t
        if pace > 1e4 or progress > 300.0 or dates["ted_ai"] == dates["ted_ai"]:
            last = i + 1
            break
        software += software_pace * dt
        measured_software += measured_pace * dt
        hardware += hardware_pace * dt
        scheduled += compute_pace * dt
    out = {key: value[:last] for key, value in out.items()}
    ran_away = bool(out["pace"][-1] > 1e4 or out["progress"][-1] > 300.0)
    if ran_away:  # everything left arrives at once
        end = float(out["t"][-1])
        dates = {name: (when if when == when else end) for name, when in dates.items()}
    return dict(out, dates=dates, ran_away=ran_away)


def at(run: dict, key: str, date: float) -> float:
    return float(np.interp(date, run["t"], run[key]))


def pace_on(run: dict, date: float) -> float:
    return at(run, "pace", date)


def calibrate(p: Params, steps: int = 16) -> Params:
    """Fit three inputs to three measurements: AI labor on Oct 1, 2025 to AI labor on Nov 1,
    2026, its doubling to the pace in May 2026, and the growth of judging time with the
    number of candidates to the pace in November 2026. Three nested bisections."""

    def short(q: Params) -> dict:
        return simulate(q, t_end=T_REF + 0.01)

    def fit_level(doubling: float, elasticity: float) -> Params:
        q = replace(p, uplift_doubling=doubling, volume_elasticity=elasticity)
        lo, hi = 1e-6, 5.0
        for _ in range(steps):
            mid = math.sqrt(lo * hi)
            if at(short(replace(q, u0=mid)), "labor", T_REF) - 1.0 > LABOR_REF:
                hi = mid
            else:
                lo = mid
        return replace(q, u0=math.sqrt(lo * hi))

    def fit_doubling(elasticity: float) -> Params:
        # With AI labor fixed in November, a slower doubling puts more of it early, so May
        # runs hotter.
        lo, hi = 0.05, 2.0
        for _ in range(steps):
            mid = math.sqrt(lo * hi)
            if pace_on(short(fit_level(mid, elasticity)), T_MAY) > PACE_MAY:
                hi = mid
            else:
                lo = mid
        return fit_level(math.sqrt(lo * hi), elasticity)

    # The more judging time each experiment takes, the fewer people judge, and November runs
    # cooler.
    lo, hi = 0.0, 1.0
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if pace_on(short(fit_doubling(mid)), T_REF) > PACE_REF:
            lo = mid
        else:
            hi = mid
    fitted = fit_doubling(0.5 * (lo + hi))
    return replace(fitted, progress_at_ref=at(short(fitted), "progress", T_REF))


def critical_share(p: Params) -> float:
    """Share of a gain the AI's own judgment must keep, against the share people's keep, for
    the loop to run away on better ideas alone."""
    return math.log(2.0) * p.difficulty / (p.value_per_sd * p.idea_rate * p.software_share)


def steady_pace(kept: float, p: Params) -> float:
    """Where the pace settles once AI labor is at its ceiling, if the AI keeps the share `kept`
    of a gain, against the share people keep, and that share stays put. Infinite at or above
    the critical share."""
    doublings = p.value_per_sd * p.idea_rate * kept / math.log(2.0) / p.difficulty
    w = p.software_share
    if w * doublings >= 1.0:
        return math.inf
    software = (1.0 + doublings * (1.0 - w)) / (1.0 - w * doublings)
    return w * software + (1.0 - w)


def fmt_date(x: float) -> str:
    if x != x:
        return "after 2045"
    year = int(x)
    return f"{MONTHS[min(11, int((x - year) * 12))]} {year}"


def fmt_delay(base: float, paced: float) -> str:
    if base != base:
        return ""
    return "past 2045" if paced != paced else f"{(paced - base) * 12:+.0f} mo"


CASES = (
    ("Ideas, transfer and metrics all +3 SD a year", dict(transfer_rate=3.0, metric_rate=3.0)),
    ("Ideas and transfer +3, metrics +1", dict(transfer_rate=3.0, metric_rate=1.0)),
    ("Ideas and transfer +3, metrics +0.5", dict(transfer_rate=3.0, metric_rate=0.5)),
    ("Ideas +3, transfer and metrics +1", dict(transfer_rate=1.0, metric_rate=1.0)),
    ("Ideas +3, transfer +1, metrics +0.5", dict(transfer_rate=1.0, metric_rate=0.5)),
    ("Ideas +3, transfer and metrics +0.5", dict(transfer_rate=0.5, metric_rate=0.5)),
)

# The three fitted inputs refitted by `calibrate` at other difficulties. Above a difficulty of
# about 1 no fit reaches the pace measured in November 2026: these two get to 1.57 and 1.46.
DIFFICULTY_FITS = {
    0.5: dict(
        u0=0.080099, uplift_doubling=0.182743, volume_elasticity=0.144372, progress_at_ref=1.341790
    ),
    0.7: dict(
        u0=0.088839, uplift_doubling=0.187031, volume_elasticity=0.088512, progress_at_ref=1.345334
    ),
    1.0: {},
    1.5: dict(
        u0=0.118576, uplift_doubling=0.195657, volume_elasticity=0.0, progress_at_ref=1.325884
    ),
    2.0: dict(
        u0=0.139250, uplift_doubling=0.199425, volume_elasticity=0.0, progress_at_ref=1.305176
    ),
}

SENSITIVITY = (
    ("Central", {}),
    ("Experiments from unlimited AI labor: 5 times", dict(labor_ceiling=5.0)),
    ("Experiments from unlimited AI labor: 60 times", dict(labor_ceiling=60.0)),
    ("Validity with the AI judging today: 0.3", dict(validity_ai_start=0.3)),
    ("Validity with the AI judging today: 0.01", dict(validity_ai_start=0.01)),
    ("Transfer with the AI judging today: 0.4", dict(transfer_ai_start=0.4)),
    ("AI never judges better than people", dict(transfer_max=0.7, validity_max=0.8)),
    ("People can vouch for any gain", dict(vouch_sd=1e9)),
    ("People can vouch for gains up to +1 SD ideas", dict(vouch_sd=1.0)),
    (
        "Judging time per experiment grows with candidates, elasticity 0.25",
        dict(volume_elasticity=0.25),
    ),
    ("60% of researcher time was already on judging", dict(time_judging=0.6)),
    ("Ideas improve +2.1 SD a year", dict(idea_rate=2.1)),
    ("Selection worth twice as much", dict(value_of_selection=0.6)),
    ("Up to a million candidates behind each experiment", dict(candidates_max=1e6)),
    ("Compute grows at half the historical rate from 2029", dict(compute_slows_in=2029.0)),
    ("Audit time counts in full as judging", dict(audit_credit=1.0)),
    ("Audit time does not count as judging", dict(audit_credit=0.0)),
    ("Deployed changes do not grow with AI labor", dict(change_growth=0.0)),
)
PATH_DATES = (2027.0, 2027.5, 2028.0, 2028.5, 2029.0, 2030.0, 2032.0, 2035.0)


def scenario_table(p: Params) -> list[str]:
    out = []
    for label, rates in CASES:
        q = replace(p, **rates)
        base = simulate(q)["dates"]
        out += [
            f"### {label}",
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
    return out


def arrival_table(p: Params) -> list[str]:
    out = [
        "| AI judgment gained per year of progress | Researcher-level AI | TED-AI | "
        "Pace in Jan 2028 | As measured |",
        "|---|---|---|---|---|",
    ]
    for label, rates in CASES:
        run = simulate(replace(p, **rates))
        cells = [label, *(fmt_date(when) for when in run["dates"].values())]
        if run["t"][-1] >= 2028.0:
            cells += [f"{at(run, key, 2028.0):.1f}x" for key in ("pace", "measured_pace")]
        else:
            cells += ["over", "over"]
        out.append("| " + " | ".join(cells) + " |")
    return out


def pacing_table(p: Params) -> list[str]:
    by_name = {policy.name: policy for policy in POLICIES}
    names = (
        "Comprehension audits, central",
        "Comprehension audits, strict",
        "Internal-use lag, 9 months",
        "R&D compute at a third of baseline",
        "R&D compute frozen at its Jan 2027 level",
        "R&D compute frozen at a third of its Jan 2027 level",
    )
    out = [
        "| AI judgment gained per year | TED-AI, no pacing | Central audits | Strict audits | "
        "9-month lag | Compute at a third of baseline | Compute frozen | "
        "Compute frozen at a third |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for label, rates in CASES:
        q = replace(p, **rates)
        base = simulate(q)["dates"]["ted_ai"]
        delays = (fmt_delay(base, simulate(q, by_name[n])["dates"]["ted_ai"]) for n in names)
        out.append("| " + " | ".join([label, fmt_date(base), *delays]) + " |")
    return out


def difficulty_table(p: Params) -> list[str]:
    by_name = {policy.name: policy for policy in POLICIES}
    audits = by_name["Comprehension audits, central"]
    fast, slow = (dict(CASES)[c] for c in (CASES[0][0], "Ideas +3, transfer +1, metrics +0.5"))
    out = [
        "| Halvings of what research buys per year of software progress | Pace it gives for "
        "Nov 2026 | Share of a gain the AI must keep for the loop to run away | TED-AI, all "
        "judgment +3 SD | TED-AI, transfer +1 and metrics +0.5 | Central audits delay it |",
        "|---|---|---|---|---|---|",
    ]
    for difficulty, fit in DIFFICULTY_FITS.items():
        q = replace(p, difficulty=difficulty, **fit)
        pace = pace_on(simulate(q, t_end=T_REF + 0.01), T_REF)
        base = simulate(replace(q, **slow))["dates"]["ted_ai"]
        paced = simulate(replace(q, **slow), audits)["dates"]["ted_ai"]
        out.append(
            f"| {difficulty:g} | {pace:.2f}x | {critical_share(q):.0%} | "
            f"{fmt_date(simulate(replace(q, **fast))['dates']['ted_ai'])} | {fmt_date(base)} | "
            f"{fmt_delay(base, paced)} |"
        )
    return out


def path_table(p: Params) -> list[str]:
    run = simulate(p)
    out = [
        "| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | "
        "Share of experiments people judge | Share of a gain the AI keeps | AI ideas | "
        "AI transfer judgment | AI metric judgment |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for when in PATH_DATES:
        if when > run["t"][-1]:
            break
        v = {key: at(run, key, when) for key in KEYS}
        out.append(
            f"| {fmt_date(when + 1e-6)} | {v['pace']:.1f}x | {v['measured_pace']:.1f}x | "
            f"{v['experiments']:.1f}x | {v['candidates']:,.0f} | {v['covered']:.0%} | "
            f"{v['kept_ai']:.0%} | {v['idea_sd']:+.1f} SD | {v['transfer_sd']:+.1f} SD | "
            f"{v['metric_sd']:+.1f} SD |"
        )
    return out


def sensitivity_table(p: Params) -> list[str]:
    by_name = {policy.name: policy for policy in POLICIES}
    audits, lag = by_name["Comprehension audits, central"], by_name["Internal-use lag, 9 months"]
    out = [
        "| Case | Researcher-level AI | TED-AI | Central audits delay TED-AI | "
        "9-month lag delays TED-AI |",
        "|---|---|---|---|---|",
    ]
    for label, change in SENSITIVITY:
        q = replace(p, **change)
        base = simulate(q)["dates"]
        cells = [label, *(fmt_date(base[name]) for name in base)]
        cells += [
            fmt_delay(base["ted_ai"], simulate(q, policy)["dates"]["ted_ai"])
            for policy in (audits, lag)
        ]
        out.append("| " + " | ".join(cells) + " |")
    return out


def tables(p: Params | None = None) -> str:
    p = p or Params()
    case = "Ideas +3, transfer +1, metrics +0.5"
    slow = replace(p, **dict(CASES)[case])
    most_kept = p.transfer_max * p.validity_max / (p.transfer_people * p.validity_people)
    out = [
        "# Chain model: milestone dates by scenario",
        "",
        "Written by `chain_model.py`. Do not edit by hand.",
        "",
        "Delays are against no pacing. Pacing starts Jan 1, 2027. Rates are SD of researcher "
        "judgment gained per year of progress. The loop runs away on better ideas alone once "
        f"the AI's own judgment keeps {critical_share(p):.0%} of the share of a gain that "
        "people's judgment keeps.",
        "",
        "Researcher-level AI and TED-AI are the dates an AI-only lab's research matches a lab "
        "of researchers at AI Futures' two levels, +3.09 and +7.72 SD. `over` means the run "
        "had ended by then.",
        "",
        "## No pacing",
        "",
        *arrival_table(p),
        "",
        "## Delay to TED-AI",
        "",
        *pacing_table(p),
        "",
        f"## The path with no pacing: {case[0].lower()}{case[1:]}",
        "",
        *path_table(slow),
        "",
        f"## Each input moved: {case[0].lower()}{case[1:]}",
        "",
        *sensitivity_table(slow),
        "",
        "## By how fast research gets harder",
        "",
        "The three fitted inputs are refitted at each difficulty. The most the AI's judgment "
        f"can keep of a gain is {most_kept:.0%} of what people's keeps.",
        "",
        *difficulty_table(p),
        "",
        "## Every scenario",
        "",
        *scenario_table(p),
    ]
    return "\n".join(out)


if __name__ == "__main__":
    print(tables())
