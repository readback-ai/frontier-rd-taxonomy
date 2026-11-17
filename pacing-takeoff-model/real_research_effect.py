"""What the labs' own usage data change, on one trajectory.

Two developers report how their agents do on real internal work, which benchmarks do not
show. This script runs AI Futures' Nov 10 example trajectory with one change
(calibration.yml, real_research) and one sensitivity:

  residue      a share of work needs a person however short the task, and that share falls
               as AI judgment rises (on HTS fuzzy tasks, where research is split into classes)
  sensitivity  the supervision schedule fitted to Google DeepMind's share of fully delegated
               pull requests in place of Anthropic's share of AI-led work. The briefing does
               not anchor on that series.

Writes results/tables_real_research.md.
"""

from __future__ import annotations

import numpy as np
import pacing_model as pm
from link_effect import T_END, date, example, months
from montecarlo_taste import taste_models

OUT = pm.HERE / "results"
CENTRAL, LAG3 = "Comprehension audits, central", "Internal-use lag, 3 months"
CASES = (
    ("Earlier sections: Anthropic's automation levels, no residue", "anthropic", False),
    ("Work that needs a person, tied to AI judgment", "anthropic", True),
    (
        "Sensitivity: handover as slow as Google DeepMind's delegation, with the residue",
        "gdm",
        True,
    ),
)


def horizon(points: list[tuple[float, float]], level: float) -> float:
    """Task length in hours at which success crosses `level`, interpolating in log length."""
    points = sorted(points)
    for (h0, s0), (h1, s1) in zip(points, points[1:], strict=False):
        if (s0 - level) * (s1 - level) <= 0 and s0 != s1:
            return float(2 ** (np.log2(h0) + (s0 - level) / (s0 - s1) * np.log2(h1 / h0)))
    return float("nan")


def logit_per_month(dates, shares) -> float:
    x, y = np.asarray(dates, float), np.asarray(shares, float)
    return float(np.polyfit(x, np.log(y / (1 - y)), 1)[0] / 12.0)


def data_tables(cal: dict) -> list[str]:
    openai = [
        (float(r["hours_mid"]), float(r["success_zero_interventions"]))
        for r in pm.read_data("openai_outcomes_by_duration.csv")
    ]
    gdm = [
        (float(r["hours_mid"]), float(r["success_no_intervention"]))
        for r in pm.read_data("gdm_outcomes_by_task_size.csv")
    ]
    monthly = pm.read_data("openai_zero_intervention_success.csv")
    by_month = {}
    for r in monthly:
        by_month.setdefault(r["month"], []).append(
            (float(r["hours_mid"]), float(r["zero_intervention_success"]))
        )
    spring = [horizon(v, 0.8) * 60 for k, v in sorted(by_month.items()) if k >= "2026-03"]
    out = [
        "## Task length finished with no human intervention",
        "",
        "| Source | 80% of the time | Half the time |",
        "|---|---|---|",
        f"| OpenAI, January to July 2026 pooled | {horizon(openai, 0.8) * 60:.0f} min | "
        f"{horizon(openai, 0.5):.1f} h |",
        f"| OpenAI, each month from March to July | {min(spring):.0f} to {max(spring):.0f} min | |",
        f"| Google DeepMind, Gemini 4 Argon | {horizon(gdm, 0.8) * 60:.0f} min | "
        f"{horizon(gdm, 0.5):.1f} h |",
        "| METR benchmark, Claude Mythos Preview, as the AI Futures Model takes it | 186 min | |",
        "",
        "Interpolated between the published buckets in log task length. OpenAI's January and "
        "February values are below 80% in every bucket.",
        "",
        "## How fast work is handed over",
        "",
        "| Series | First value | Last value | Change in log-odds per month |",
        "|---|---|---|---|",
    ]
    pts = cal["anthropic_automation_index"]["al4_share"]
    prs = pm.read_data("gdm_pull_requests_by_ai_share.csv")
    strict = [float(r["ai_100pct_under_3_human_turns"]) for r in prs]
    loose = [
        s + float(r["ai_over_98pct_under_10_human_turns"]) for s, r in zip(strict, prs, strict=True)
    ]
    when = [float(r["decimal_year"]) for r in prs]
    series = [
        (
            "Anthropic, share of work that AI leads",
            [p["date"] for p in pts],
            [p["share"] for p in pts],
        ),
        (
            "Anthropic, the same without March",
            [p["date"] for p in pts[1:]],
            [p["share"] for p in pts[1:]],
        ),
        ("Google DeepMind, fully delegated pull requests (under 3 human turns)", when, strict),
        ("Google DeepMind, over 98% AI-written with under 10 human turns, or better", when, loose),
    ]
    for label, x, y in series:
        out.append(
            f"| {label} | {y[0]:.1%} in {pm.fmt_date(x[0])} | {y[-1]:.1%} in "
            f"{pm.fmt_date(x[-1])} | {logit_per_month(x, y):+.2f} |"
        )
    out += [
        "",
        "The model's supervision schedule is a logistic in capability fitted to the first "
        "series. The sensitivity rows below fit it to the third.",
        "",
    ]
    return out


def ranks(values) -> np.ndarray:
    values = np.asarray(values, float)
    order = np.argsort(values)
    out = np.empty(len(values))
    out[order] = np.arange(len(values))
    for v in np.unique(values):
        out[values == v] = out[values == v].mean()
    return out


def benchmarks(cal: dict) -> list[str]:
    """Three benchmarks scored against human judgment, and how each moves with capability."""
    jb, pairs = cal["judgment_benchmarks"], cal["taste_eval"]["pairs"]
    name = lambda key: jb[key].removeprefix("data/")  # noqa: E731
    taste = pm.read_data(name("taste_rerun"))
    eci = np.array([float(r["eci"]) for r in taste])
    acc = np.array([float(r["taste_accuracy"]) for r in taste])
    noise = 1.96 * np.sqrt(0.25 / pairs)
    outside = int(np.sum(np.abs(acc - 0.5) > noise))
    redwood = pm.read_data(name("redwoodbench"))
    r_eci = np.array([float(r["eci"]) for r in redwood])
    recall = np.array([float(r["recall_pct"]) for r in redwood])
    lmca = pm.read_data(name("lmca"))
    when = np.array([float(r["decimal_year"]) for r in lmca])
    score = np.array([float(r["lmca_score"]) for r in lmca])
    slope, intercept = np.polyfit(when, score, 1)
    ceiling = jb["lmca_estimated_ceiling"]
    latest = when.max() + (ceiling - score.max()) / slope
    return [
        "## Benchmarks scored against human judgment",
        "",
        "| Benchmark | Models | Scores | How it moves with capability |",
        "|---|---|---|---|",
        f"| TASTE, rerun | {len(taste)} | {acc.min():.0%} to {acc.max():.0%}, chance 50% | Rank "
        f"correlation with ECI {np.corrcoef(ranks(eci), ranks(acc))[0, 1]:+.2f}. {outside} "
        f"models are more than {noise * 100:.0f} points from chance, the 95% noise band on {pairs} "
        "pairs |",
        f"| RedwoodBench | {len(redwood)} | {recall.min():.1f}% to {recall.max():.1f}% of human "
        f"reviewers' points matched | Correlation with ECI {np.corrcoef(r_eci, recall)[0, 1]:.2f}, "
        f"{np.polyfit(r_eci, recall, 1)[0]:+.2f} points per ECI point |",
        f"| LMCA, frontier models the chart labels | {len(lmca)} | {score.min():.0f} to "
        f"{score.max():.0f}, estimated ceiling {ceiling} | {slope:+.0f} points a year since "
        f"{pm.fmt_date(when.min())}, correlation {np.corrcoef(when, score)[0, 1]:.2f}. The fitted "
        f"line reaches the ceiling in {pm.fmt_date((ceiling - intercept) / slope)}. From the "
        f"latest model at that slope it is {pm.fmt_date(latest)} |",
        "",
        "All values were read by eye from charts. The benchmarks' pages were not fetched.",
        "",
    ]


def model_a(cal: dict) -> list[str]:
    out = [
        "## Model A, no pacing",
        "",
        "| Supervision fitted to | Capability of the superhuman AI researcher reached | Pace in "
        "January 2028 | Labor uplift in January 2028 |",
        "|---|---|---|---|",
    ]
    for label, kind in (
        ("Anthropic's automation levels", "anthropic"),
        ("Sensitivity: Google DeepMind's fully delegated pull requests", "gdm"),
    ):
        m, _ = pm.build_a(cal, supervision=kind)
        s = pm.summarize_a(m, m.simulate(t_end=2040.0))
        pace = "off scale" if s["pace_2028.0"] > 100 else f"{s['pace_2028.0']:.1f}x"
        uplift = (
            "off scale" if s["labor_uplift_2028.0"] > 1e6 else f"{s['labor_uplift_2028.0']:.0f}x"
        )
        out.append(f"| {label} | {date(s['t_sar'])} | {pace} | {uplift} |")
    out += [
        "",
        "Model A has no research-judgment term, so the residue rule does not apply to it.",
        "",
    ]
    return out


def main() -> None:
    cal = pm.load_calibration()
    policies = {p.name: p for p in pm.standard_policies(cal)}
    rr = cal["real_research"]
    out = [
        "# What the labs' own usage data change, on one trajectory",
        "",
        "Written by `real_research_effect.py`. Do not edit by hand.",
        "",
        *data_tables(cal),
        *benchmarks(cal),
        *model_a(cal),
        "## Model B, AI Futures' Nov 10 example trajectory",
        "",
        "The link from comprehension to human judgment is on. Pacing starts Jan 1, 2027. With the "
        f"residue, {rr['residue_today']:.0%} of work needs a person on Nov 1, 2026, and that share "
        "falls with the share of researchers whose judgment is still better than the AI's. A "
        f"person spends {rr['residue_supervision_time']:.1%} of that work's time supervising it.",
        "",
    ]
    for spec in taste_models(cal):
        out += [
            f"### {spec.heading} ({spec.name})",
            "",
            "| Supervision | No pacing: superhuman AI researcher | No pacing: TED-AI | Central "
            "audits: delay to superhuman AI researcher | Central audits: delay to TED-AI | "
            "3-month lag: delay to TED-AI |",
            "|---|---|---|---|---|---|",
        ]
        for label, kind, residue in CASES:
            m = example(cal, spec)
            m.fit_supervision(kind, cal)
            m.use_calibration(cal, link=True, residue=residue)
            runs = {
                name: m.summarize(
                    m.simulate(policies[name], t_end=T_END, step=0.006, stop_at="TED-AI")
                )
                for name in ("No pacing", CENTRAL, LAG3)
            }
            free, audit, lag = runs["No pacing"], runs[CENTRAL], runs[LAG3]
            out.append(
                f"| {label} | {date(free['t_sar'])} | {date(free['t_ted_ai'])} | "
                f"{months(free['t_sar'], audit['t_sar'])} | "
                f"{months(free['t_ted_ai'], audit['t_ted_ai'])} | "
                f"{months(free['t_ted_ai'], lag['t_ted_ai'])} |"
            )
            print("done:", spec.name, label, flush=True)
        out.append("")
    (OUT / "tables_real_research.md").write_text("\n".join(out))
    print("wrote results/tables_real_research.md")


if __name__ == "__main__":
    main()
