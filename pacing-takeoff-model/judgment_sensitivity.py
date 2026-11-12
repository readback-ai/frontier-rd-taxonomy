"""How three disputed inputs change what audits do in the AI Futures Model.

1. AI research judgment ("research taste") is weaker today, or improves more slowly.
2. Progress is driven by data generation, a volume of deployed dataset updates.
3. The real pace is lower than measured, because benchmarks favor verifiable tasks.

Parts 1 and 2 vary AI Futures' Nov 10 example trajectory. Part 1 also splits the
Monte Carlo trajectories by their sampled research-judgment parameters. Part 3
reads the slower-pace Monte Carlo band, if it has been run:

    python montecarlo_b.py --samples 4000 --pace-low 1.25 --pace-high 1.5 --tag slow \\
        --scenarios "No pacing;Comprehension audits, central;Comprehension audits, strict;\\
Internal-use lag, 3 months"

Writes results/tables_judgment.md.
"""

from __future__ import annotations

import csv
import math
from dataclasses import replace

import numpy as np
import pacing_model as pm
from aifm_adapter import DEFAULT_AIFM_PATH, ELI_AUG_2026, Q35_EXAMPLE, Aifm
from montecarlo_b import OUT, draw_samples

CENTRAL, STRICT, LAG3 = (
    "Comprehension audits, central",
    "Comprehension audits, strict",
    "Internal-use lag, 3 months",
)
T_END = 2036.0
TASTE_AT_AC = "ai_research_taste_at_coding_automation_anchor_sd"
SLOPE = "ai_research_taste_slope"


def months(a: float, b: float) -> str:
    if a != a:
        return "n/a"
    return "past 2035" if b != b else f"{(b - a) * 12:+.0f} mo"


def date(x: float) -> str:
    return "after 2035" if x != x else pm.fmt_date(x)


def _ted_ai(m: Aifm, policy) -> float:
    """Date of TED-AI on model `m` under `policy`, nan if not reached by T_END."""
    return m.summarize(m.simulate(policy, t_end=T_END, step=0.006)).get("t_ted_ai", float("nan"))


def variants(cal: dict) -> list[str]:
    policies = {p.name: p for p in pm.standard_policies(cal)}
    g0 = pm.gate_from_calibration(cal)
    data_types = tuple(
        replace(t, elasticity=1.0) if t.name == "dataset_updates" else t for t in g0.types
    )
    data_gate = pm.rescale(
        replace(g0, types=data_types),
        weights={
            "training_improvements": 0.3,
            "dataset_updates": 0.5,
            "system_software_changes": 0.2,
        },
    )
    data_policy = pm.Policy(
        "Central audits, data-driven progress", start=cal["policy_start"], gate=data_gate
    )
    cases = [
        ("AI Futures' Nov 10 example (judgment +0.5 SD at automated coder, +2.1 SD a year)", {}),
        ("Judgment -1 SD at automated coder", {TASTE_AT_AC: -1.0}),
        ("Judgment -2.5 SD at automated coder", {TASTE_AT_AC: -2.5}),
        ("Judgment improves +1.0 SD a year", {SLOPE: 1.0}),
    ]
    out = [
        "## Varying research judgment on AI Futures' example trajectory",
        "",
        "| Case | Pace Nov 2026 | No pacing: SAR | No pacing: TED-AI | Central audits: TED-AI "
        "delay "
        "| Strict audits: TED-AI delay | 3-month lag: TED-AI delay | Central audits with "
        "data-driven "
        "progress: TED-AI delay |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for label, override in cases:
        m = Aifm(dict(ELI_AUG_2026, **Q35_EXAMPLE, **override))
        m.use_calibration(cal)
        m.fit_supervision("anthropic", cal)
        base = m.summarize(m.simulate(policies["No pacing"], t_end=T_END, step=0.006))
        ted = base.get("t_ted_ai", float("nan"))
        out.append(
            f"| {label} | {m.base_pace(cal['reference_date']):.2f}x | "
            f"{date(base.get('t_sar', float('nan')))} | "
            f"{date(ted)} | {months(ted, _ted_ai(m, policies[CENTRAL]))} | "
            f"{months(ted, _ted_ai(m, policies[STRICT]))} | "
            f"{months(ted, _ted_ai(m, policies[LAG3]))} | {months(ted, _ted_ai(m, data_policy))} |"
        )
        print("done:", label, flush=True)
    out += [
        "",
        "Data-driven progress: dataset updates grow in proportion to AI labor and carry half of "
        "progress "
        "(training improvements 0.3, system software 0.2).",
        "",
    ]
    return out


def load(tag: str = "") -> list[dict]:
    path = OUT / f"model_b_montecarlo{'_' + tag if tag else ''}.csv"
    if not path.exists():
        return []
    with open(path) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["sample"] = int(r["sample"])
        for k in ("pace_nov_2026", "sar", "ted_ai", "asi"):
            r[k] = float(r[k])
    return rows


def paired(rows: list[dict], reference: float):
    """Per trajectory with no SAR on the reference date and TED-AI reached with no pacing:
    {scenario: delay in months}, plus the no-pacing row."""
    by = {}
    for r in rows:
        by.setdefault(r["sample"], {})[r["scenario"]] = r
    out = {}
    for sample, d in by.items():
        base = d["No pacing"]
        if base["sar"] <= reference + 0.01 or base["ted_ai"] != base["ted_ai"]:
            continue
        delays = {
            name: (
                math.inf if r["ted_ai"] != r["ted_ai"] else (r["ted_ai"] - base["ted_ai"]) * 12.0
            )
            for name, r in d.items()
            if name != "No pacing"
        }
        out[sample] = (base, delays)
    return out


def med(xs) -> str:
    x = float(np.median(list(xs)))
    return "past 2035" if x == math.inf else f"{x:+.1f} mo"


def split_by_judgment(cal: dict) -> list[str]:
    rows = load()
    if not rows:
        return []
    meta_seed, n = 20261110, 4000
    samples = draw_samples(DEFAULT_AIFM_PATH, "daniel", n, meta_seed)
    pairs = paired(rows, cal["reference_date"])
    keys = sorted(pairs)
    out = [
        "## Monte Carlo trajectories split by sampled research judgment",
        "",
        f"{len(keys)} trajectories with a pace of 1.5x to 2x on Nov 1, 2026, no superhuman AI "
        "researcher by then, "
        "and TED-AI reached by 2035 with no pacing.",
        "",
        "| Split | Third | Range | No pacing: median SAR | No pacing: median TED-AI | Central "
        "audits: median delay "
        "| Strict audits: median delay | 3-month lag: median delay |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for name, label, unit in (
        (SLOPE, "Judgment improvement per year", "SD"),
        (TASTE_AT_AC, "Judgment at automated coder", "SD"),
    ):
        x = np.array([samples[k][name] for k in keys])
        for third, idx in zip(
            ("lowest", "middle", "highest"), np.array_split(np.argsort(x), 3), strict=True
        ):
            ks = [keys[i] for i in idx]
            out.append(
                f"| {label} | {third} | {x[idx].min():+.1f} to {x[idx].max():+.1f} {unit} | "
                f"{date(float(np.median([pairs[k][0]['sar'] for k in ks])))} | "
                f"{date(float(np.median([pairs[k][0]['ted_ai'] for k in ks])))} | "
                f"{med(pairs[k][1][CENTRAL] for k in ks)} | {med(pairs[k][1][STRICT] for k in ks)} "
                "| "
                f"{med(pairs[k][1][LAG3] for k in ks)} |"
            )
    out.append("")
    return out


def by_pace(cal: dict) -> list[str]:
    bands = [
        ("1.5x to 2x (METR's central estimate)", load()),
        ("1.25x to 1.5x (slower real pace)", load("slow")),
    ]
    if not bands[1][1]:
        return []
    out = [
        "## Monte Carlo by pace on Nov 1, 2026",
        "",
        "| Pace band | Trajectories | No pacing: median SAR | No pacing: median TED-AI | Central "
        "audits: median delay "
        "| Central audits: delayed 6 months or more | Strict audits: median delay | 3-month lag: "
        "median delay |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for label, rows in bands:
        pairs = paired(rows, cal["reference_date"])
        base_all = [
            r
            for r in rows
            if r["scenario"] == "No pacing" and not r["sar"] <= cal["reference_date"] + 0.01
        ]
        ted = [math.inf if r["ted_ai"] != r["ted_ai"] else r["ted_ai"] for r in base_all]
        sar = [math.inf if r["sar"] != r["sar"] else r["sar"] for r in base_all]
        m_ted, m_sar = float(np.median(ted)), float(np.median(sar))
        central = [d[CENTRAL] for _, d in pairs.values()]
        out.append(
            f"| {label} | {len(base_all)} | {date(float('nan') if m_sar == math.inf else m_sar)} | "
            f"{date(float('nan') if m_ted == math.inf else m_ted)} | {med(central)} | "
            f"{sum(1 for x in central if x >= 6) / len(central):.0%} | "
            f"{med(d[STRICT] for _, d in pairs.values())} | "
            f"{med(d[LAG3] for _, d in pairs.values())} |"
        )
    out += [
        "",
        "Trajectories with a superhuman AI researcher already on Nov 1, 2026 are excluded. Delays "
        "are over "
        "trajectories that reach TED-AI by 2035 with no pacing.",
        "",
    ]
    return out


def main() -> None:
    cal = pm.load_calibration()
    out = [
        "# Research judgment, data generation and pace: effect on audits",
        "",
        "Written by `judgment_sensitivity.py`. Do not edit by hand.",
        "",
    ]
    out += variants(cal) + split_by_judgment(cal) + by_pace(cal)
    (OUT / "tables_judgment.md").write_text("\n".join(out))
    print("wrote results/tables_judgment.md")


if __name__ == "__main__":
    main()
