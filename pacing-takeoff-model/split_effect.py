"""What splitting research into supervisable and HTS fuzzy tasks does, on one trajectory.

Runs AI Futures' Nov 10 example trajectory with AI judgment improving at one
rate on supervisable tasks and a slower rate on HTS fuzzy tasks (calibration.yml,
taste_split), and varies the three inputs that have no measurement behind them:
the share of research effort that is supervisable today, how far supervisable work can stand
in for HTS fuzzy work, and whether supervisable judgment starts ahead.

Writes results/tables_split.md.
"""

from __future__ import annotations

import numpy as np
import pacing_model as pm
from link_effect import T_END, at, date, example, months
from montecarlo_taste import taste_models

OUT = pm.HERE / "results"
CENTRAL, LAG3 = "Comprehension audits, central", "Internal-use lag, 3 months"
PATH_DATES = (2027.0, 2027.5, 2028.0, 2028.5, 2029.0, 2030.0)


def run(m, policy) -> tuple[dict, dict]:
    result = m.simulate(policy, t_end=T_END, step=0.006, stop_at="TED-AI")
    return m.summarize(result), result


def row(label: str, m, policies: dict) -> str:
    free, _ = run(m, policies["No pacing"])
    audit, _ = run(m, policies[CENTRAL])
    lag, _ = run(m, policies[LAG3])
    return (
        f"| {label} | {date(free['t_sar'])} | {date(free['t_ted_ai'])} | "
        f"{months(free['t_sar'], audit['t_sar'])} | {months(free['t_ted_ai'], audit['t_ted_ai'])} "
        "| "
        f"{months(free['t_ted_ai'], lag['t_ted_ai'])} |"
    )


def main() -> None:
    cal = pm.load_calibration()
    sp = cal["taste_split"]
    policies = {p.name: p for p in pm.standard_policies(cal)}
    out = [
        "# Supervisable and HTS fuzzy research tasks on one trajectory",
        "",
        "Written by `split_effect.py`. Do not edit by hand.",
        "",
        "AI Futures' Nov 10 example trajectory. AI research taste is "
        f"{cal['taste_models']['level_sd']:+g} SD on {pm.fmt_date(cal['taste_models']['date'])} in "
        "both "
        "classes unless a row says otherwise. The link from comprehension to human judgment is on. "
        "Pacing starts Jan 1, 2027.",
        "",
    ]
    for spec in (m for m in taste_models(cal) if m.hts_fuzzy is not None):
        out += [f"## {spec.heading} ({spec.name})", ""]
        central = example(cal, spec)
        central.use_calibration(cal, link=True)
        _, path = run(central, policies["No pacing"])
        out += [
            "### No pacing: where the effort goes",
            "",
            "| Date | AI judgment, supervisable tasks | AI judgment, HTS fuzzy tasks | "
            "Judgment of an AI-only lab | "
            "Share of research effort on HTS fuzzy tasks | Share of deployed value that a person "
            "understands | "
            "Pace |",
            "|---|---|---|---|---|---|---|",
        ]
        for when in PATH_DATES:
            if when > path["t"][-1]:
                continue
            cap = at(path, "progress", when)
            supervisable, hts_fuzzy = central.class_sds(cap)
            _, people = central.class_tastes(cap)
            out.append(
                f"| {pm.fmt_date(when + 1e-6)} | {supervisable:+.1f} SD | {hts_fuzzy:+.1f} SD | "
                f"{central.taste_sd(cap):+.1f} SD | {central.effort_shares(people)[1]:.0%} | "
                f"{at(path, 'understood_lab', when):.0%} | {at(path, 'pace', when):.1f}x |"
            )
        out += [
            "",
            "Effort shares use the lab's judgment with its people fully informed.",
            "",
            "### Varying the inputs with no measurement behind them",
            "",
            "| Case | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: "
            "delay to "
            "superhuman AI researcher | Central audits: delay to TED-AI | 3-month lag: delay to "
            "TED-AI |",
            "|---|---|---|---|---|---|",
        ]
        cases = [
            (
                f"Central: supervisable share {sp['supervisable_share']:.0%}, "
                f"substitution {sp['substitution']:g}",
                {},
            ),
            ("Supervisable share 50%", dict(share=0.5)),
            ("Supervisable share 80%", dict(share=0.8)),
            ("Substitution 0 (fixed proportions)", dict(substitution=0.0)),
            ("Substitution 0.5", dict(substitution=0.5)),
            (
                "Substitution 0.83 (one AI Futures author's light bottleneck)",
                dict(substitution=0.83),
            ),
            ("Supervisable judgment starts at -1.5 SD", dict(supervisable_level=-1.5)),
        ]
        for label, override in cases:
            m = example(cal, spec, **override)
            m.use_calibration(cal, link=True)
            out.append(row(label, m, policies))
            print("done:", spec.name, label, flush=True)
        ceiling = (1.0 - sp["supervisable_share"]) ** (-1.0 / (1.0 - sp["substitution"]))
        sigma = float(central.params.taste_distribution.sigma)
        out += [
            "",
            f"With supervisable work free, the lab's judgment is at most {ceiling:.1f} times its "
            "judgment on HTS fuzzy "
            f"tasks, which is {np.log(ceiling) / sigma:.1f} SD on this trajectory's researcher "
            "distribution.",
            "",
        ]
    (OUT / "tables_split.md").write_text("\n".join(out))
    print("wrote results/tables_split.md")


if __name__ == "__main__":
    main()
