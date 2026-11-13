"""How far the result on work that needs a person depends on its unmeasured inputs.

The briefing starts with 14% of work needing a person, supervised at the time AI-led work
takes, a share that falls with the share of researchers whose judgment is still better than
the AI's. This script lists what three developers report on that share and reruns AI Futures'
Nov 10 example trajectory with the starting share, the supervision time, the rule for how the
share falls and the audit hours varied (calibration.yml, real_research.sensitivity).

Writes results/tables_residue_sensitivity.md.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from multiprocessing import Pool

import pacing_model as pm
from link_effect import T_END, example
from montecarlo_taste import taste_models

OUT = pm.HERE / "results"
CENTRAL, LAG9, HEAVY = "Comprehension audits, central", "Internal-use lag, 9 months", "heavy"
TASTES = (("split_3_1", "Fuzzy tasks at +1 SD"), ("split_3_0.5", "Fuzzy tasks at +0.5 SD"))


def cases(cal: dict) -> dict[str, dict]:
    """Label -> arguments of Aifm.set_residue."""
    rr = cal["real_research"]
    today, sens = rr["residue_today"], rr["sensitivity"]
    al4 = cal["human_time_per_unit_work"]["al4"]
    out = {
        "No work needs a person": dict(share=0.0),
        f"Central: {today:.0%} of work, supervised at {al4:.0%} of its time": dict(share=today),
    }
    for share in sens["residue_today"]:
        out[f"Starting share {share:.0%}"] = dict(share=share)
    for mult in sens["supervision_multiple"]:
        out[f"Supervised at {al4 * mult:.1%} of its time"] = dict(share=today, supervision=mult)
    for sd in sens["halving_sd"]:
        out[f"Share halves per {sd:g} SD of judgment the AI gains"] = dict(
            share=today, halving_sd=sd
        )
    return out


def run(job: tuple[str, str, str]) -> tuple[tuple[str, str, str], float, float]:
    taste, case, policy = job
    cal = pm.load_calibration()
    policies = {p.name: p for p in pm.standard_policies(cal)}
    scale = cal["real_research"]["sensitivity"]["audit_hours_scale"]
    central = policies[CENTRAL]
    policies[HEAVY] = replace(central, name=HEAVY, gate=replace(central.gate, hours_scale=scale))
    spec = {s.name: s for s in taste_models(cal)}[taste]
    m = example(cal, spec)
    m.use_calibration(cal, link=True)
    m.set_residue(**cases(cal)[case])
    s = m.summarize(m.simulate(policies[policy], t_end=T_END, step=0.006, stop_at="TED-AI"))
    print("done:", *job, flush=True)
    return job, s["t_sar"], s["t_ted_ai"]


def date(x: float) -> str:
    return "after 2039" if x != x else pm.fmt_date(x)


def months(a: float, b: float) -> str:
    return "past 2039" if b != b else f"{(b - a) * 12:+.0f} mo"


def reported() -> list[str]:
    """What three developers report on work that needs a person however easy the task."""
    monthly = [
        r
        for r in pm.read_data("openai_zero_intervention_success.csv")
        if r["bucket"] == "<15m" and r["month"] >= "2026-03"
    ]
    spring = [1.0 - float(r["zero_intervention_success"]) for r in monthly]
    pooled = pm.read_data("openai_outcomes_by_duration.csv")[0]
    gdm = pm.read_data("gdm_outcomes_by_task_size.csv")[0]
    ant = pm.read_data("anthropic_session_success.csv")
    first, last = ant[0], ant[-1]
    tiers = ("trivial", "routine", "substantial", "open_ended")
    out = [
        "## What three developers report",
        "",
        "| Source | Measure | Earlier | Latest |",
        "|---|---|---|---|",
        "| OpenAI | Tasks under 15 minutes that needed an intervention or failed | "
        f"{min(spring):.0%} to {max(spring):.0%} in each month from March to July 2026 | "
        f"{1 - float(pooled['success_zero_interventions']):.0%}, January to July 2026 pooled |",
        "| Google DeepMind, Gemini 4 Argon | Tasks under 15 minutes that needed an intervention "
        f"or failed | | {1 - float(gdm['success_no_intervention']):.0%} of {gdm['n']} tasks |",
    ]
    for tier in tiers:
        out.append(
            f"| Anthropic | Sessions on {tier.replace('_', '-')} tasks that needed a correction | "
            f"{1 - float(first[tier]):.0%} in {pm.fmt_date(float(first['decimal_year']))} | "
            f"{1 - float(last[tier]):.0%} in {pm.fmt_date(float(last['decimal_year']))} |"
        )
    out += [
        "",
        "OpenAI's monthly values and Anthropic's values were read by eye from charts, to about "
        "2 points.",
        "",
    ]
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    cal = pm.load_calibration()
    scale = cal["real_research"]["sensitivity"]["audit_hours_scale"]
    labels = list(cases(cal))
    policies = ("No pacing", CENTRAL, HEAVY, LAG9)
    jobs = [(t, c, p) for t, _ in TASTES for c in labels for p in policies]
    with Pool(args.workers) as pool:
        got = {job: (sar, ted) for job, sar, ted in pool.imap_unordered(run, jobs)}
    out = [
        "# Work that needs a person: what is reported, and how far the result depends on it",
        "",
        "Written by `residue_sensitivity.py`. Do not edit by hand.",
        "",
        *reported(),
        "## Sensitivity on AI Futures' Nov 10 example trajectory",
        "",
        "Crisp tasks improve 3 SD per year of 2025 progress. The link from comprehension to "
        "human judgment is on. Pacing starts Jan 1, 2027. Each row changes one input of the "
        "central case.",
        "",
    ]
    for taste, heading in TASTES:
        out += [
            f"### {heading} ({taste})",
            "",
            "| Case | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: "
            f"delay to TED-AI | Audits at {scale:g} times the hours: delay to superhuman AI "
            f"researcher | Audits at {scale:g} times the hours: delay to TED-AI | 9-month lag: "
            "delay to TED-AI |",
            "|---|---|---|---|---|---|---|",
        ]
        for case in labels:
            sar, ted = got[(taste, case, "No pacing")]
            heavy = got[(taste, case, HEAVY)]
            out.append(
                f"| {case} | {date(sar)} | {date(ted)} | "
                f"{months(ted, got[(taste, case, CENTRAL)][1])} | {months(sar, heavy[0])} | "
                f"{months(ted, heavy[1])} | {months(ted, got[(taste, case, LAG9)][1])} |"
            )
        out.append("")
    (OUT / "tables_residue_sensitivity.md").write_text("\n".join(out))
    print("wrote results/tables_residue_sensitivity.md")


if __name__ == "__main__":
    main()
