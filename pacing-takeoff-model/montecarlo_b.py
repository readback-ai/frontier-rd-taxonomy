"""Monte Carlo for Model B: median milestone dates under each pacing scenario.

AI Futures forecasts with a distribution over the AI Futures Model's parameters,
then keeps the sampled trajectories whose pace of progress on Nov 1, 2026
matches what METR measured. This script does the same with their public code
and their August 2026 sampling configuration, and then runs every kept
trajectory under each pacing scenario.

Usage:
    python montecarlo_b.py --samples 2000            # about 30 minutes on 4 cores
    python montecarlo_b.py --samples 2000 --forecaster eli

Writes results/model_b_montecarlo.csv, results/tables_montecarlo.md and
results/fig4_ted_ai_by_scenario.png.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import logging
import math
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np
import pacing_model as pm
from aifm_adapter import DEFAULT_AIFM_PATH, Aifm

OUT = pm.HERE / "results"
CONFIGS = {"daniel": "sampling_config_q2_daniel.yaml", "eli": "sampling_config_q2_eli.yaml"}
SCENARIOS = [
    "No pacing",
    "Human sign-off, no comprehension standard",
    "Comprehension audits, light",
    "Comprehension audits, central",
    "Comprehension audits, strict",
    "Internal-use lag, 3 months",
    "Internal-use lag, 9 months",
    "R&D compute cut 3x",
    "Comprehension audits (central) + 3-month lag",
    "Comprehension audits (central) + 9-month lag",
]
T_END = 2036.0  # a milestone not reached by then is recorded as later than this
# Sampled parameters recorded with each kept trajectory, for analysis.
RECORD = [
    "ai_research_taste_slope",
    "ai_research_taste_at_coding_automation_anchor_sd",
    "median_to_top_taste_multiplier",
    "inf_labor_asymptote",
    "inv_compute_anchor_exp_cap",
    "rho_coding_labor",
    "serial_uplift_at_reference_date",
    "ac_anchor_mode",
]
_STATE = {}


def draw_samples(aifm_path: Path, forecaster: str, n: int, seed: int) -> list[dict]:
    """Parameter sets drawn with AI Futures' own sampler and configuration."""
    logging.disable(logging.WARNING)
    if str(aifm_path) not in sys.path:
        sys.path.insert(0, str(aifm_path))
    spec = importlib.util.spec_from_file_location(
        "aifm_batch_rollout", aifm_path / "scripts" / "pipelines" / "batch_rollout.py"
    )
    br = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(br)
    from progress_model import config as cfg

    conf = br._load_config(str(aifm_path / "config" / CONFIGS[forecaster]))
    dists = dict(conf.get("parameters", {}))
    corr = conf.get("correlation_matrix")
    master = np.random.SeedSequence(seed)
    if corr is not None and corr.get("parameters") and corr.get("correlation_matrix") is not None:
        latent = br._calibrate_gaussian_copula_latent_corr(
            dists,
            corr["parameters"],
            np.array(corr["correlation_matrix"], dtype=float),
            np.random.default_rng(master.spawn(1)[0]),
            interpretation=str(
                corr.get("correlation_type", corr.get("interpretation", "spearman"))
            ),
            calibration_samples=int(corr.get("calibration_samples", 20000)),
        )
        corr["latent_correlation_matrix"] = latent.tolist()
    out = []
    for child in master.spawn(n):
        with br._suppress_noise():
            p = br._sample_parameter_dict(dists, np.random.default_rng(child), corr)
        p.setdefault("horizon_extrapolation_type", cfg.DEFAULT_HORIZON_EXTRAPOLATION_TYPE)
        p.setdefault("taste_schedule_type", cfg.DEFAULT_TASTE_SCHEDULE_TYPE)
        out.append(p)
    return out


def _init(aifm_path, band, supervision, scenarios=None):
    import warnings

    warnings.filterwarnings("ignore")  # AIFM overflows harmlessly on extreme draws
    np.seterr(all="ignore")
    logging.disable(logging.WARNING)
    _STATE.update(path=aifm_path, band=band, supervision=supervision, cal=pm.load_calibration())
    _STATE["policies"] = {p.name: p for p in pm.standard_policies(_STATE["cal"])}
    _STATE["scenarios"] = list(scenarios or SCENARIOS)


def _work(job):
    """Run one sampled parameter set. Returns (index, pace, rows) with rows empty unless kept."""
    index, params = job
    cal = _STATE["cal"]
    try:
        m = Aifm(params, _STATE["path"], cal["reference_date"])
        pace = m.base_pace(cal["reference_date"])
    except Exception:
        return index, float("nan"), []
    lo, hi = _STATE["band"]
    if not (lo <= pace <= hi) or "TED-AI" not in m.milestones:
        return index, pace, []
    rows = []
    try:
        m.use_calibration(cal)
        m.fit_supervision(_STATE["supervision"], cal)
        extra = {k: params.get(k, "") for k in RECORD}
        extra["ac_date_no_pacing"] = m.milestones.get("AC", (float("nan"),))[0]
        extra["sar_date_aifm"] = m.milestones.get("SAR", (float("nan"),))[0]
        for name in _STATE["scenarios"]:
            s = m.summarize(m.simulate(_STATE["policies"][name], t_end=T_END, step=0.006))
            rows.append(
                dict(
                    sample=index,
                    pace_nov_2026=pace,
                    scenario=name,
                    sar=s.get("t_sar", float("nan")),
                    ted_ai=s.get("t_ted_ai", float("nan")),
                    asi=s.get("t_asi", float("nan")),
                    **extra,
                )
            )
    except Exception:
        return index, pace, []
    return index, pace, rows


def quantile(values: list[float], q: float) -> float:
    """Quantile where a missing date means later than T_END. nan if the quantile is missing."""
    v = sorted(math.inf if x != x else x for x in values)
    x = v[min(len(v) - 1, int(math.floor(q * (len(v) - 1) + 0.5)))]
    return float("nan") if x == math.inf else x


def summarize(rows: list[dict]) -> list[dict]:
    present = [name for name in SCENARIOS if any(r["scenario"] == name for r in rows)]
    by = {name: [r for r in rows if r["scenario"] == name] for name in present}
    base = {r["sample"]: r for r in by["No pacing"]}
    out = []
    for name in present:
        rs = by[name]
        # Paired delay, over trajectories that reach TED-AI by T_END with no pacing.
        delay = [
            (r["ted_ai"] - base[r["sample"]]["ted_ai"]) * 12.0
            for r in rs
            if base[r["sample"]]["ted_ai"] == base[r["sample"]]["ted_ai"]
        ]
        out.append(
            dict(
                scenario=name,
                n=len(rs),
                sar_median=quantile([r["sar"] for r in rs], 0.5),
                ted_ai_p25=quantile([r["ted_ai"] for r in rs], 0.25),
                ted_ai_median=quantile([r["ted_ai"] for r in rs], 0.5),
                ted_ai_p75=quantile([r["ted_ai"] for r in rs], 0.75),
                asi_median=quantile([r["asi"] for r in rs], 0.5),
                ted_ai_delay_months_median=quantile(delay, 0.5),
                ted_ai_delay_months_p75=quantile(delay, 0.75),
                ted_ai_after_2035=sum(1 for r in rs if r["ted_ai"] != r["ted_ai"])
                / max(len(rs), 1),
            )
        )
    return out


def date_text(x: float) -> str:
    return f"after {T_END - 1:.0f}" if x != x else pm.fmt_date(x)


def _delay(x: float) -> str:
    return "past 2035" if x != x else f"{x:+.0f} mo"


def _table(summary) -> list[str]:
    out = [
        "| Scenario | Median TED-AI | Middle half of trajectories | Median delay | Delay, upper "
        "quartile "
        "| Median SAR | Median ASI |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in summary:
        out.append(
            f"| {s['scenario']} | {date_text(s['ted_ai_median'])} | {date_text(s['ted_ai_p25'])} "
            "to "
            f"{date_text(s['ted_ai_p75'])} | {_delay(s['ted_ai_delay_months_median'])} | "
            f"{_delay(s['ted_ai_delay_months_p75'])} | {date_text(s['sar_median'])} | "
            f"{date_text(s['asi_median'])} |"
        )
    return out


def not_yet(rows: list[dict], reference: float) -> list[dict]:
    """Trajectories in which no superhuman AI researcher exists on the reference date."""
    # A run starts on the reference date, so a milestone already passed is dated to that day.
    late = {
        r["sample"]
        for r in rows
        if r["scenario"] == "No pacing" and not r["sar"] <= reference + 0.01
    }
    return [r for r in rows if r["sample"] in late]


def markdown(rows, meta) -> str:
    reference = pm.load_calibration()["reference_date"]
    subset = not_yet(rows, reference)
    n_sub = len({r["sample"] for r in subset})
    out = [
        "# Model B Monte Carlo",
        "",
        "Written by `montecarlo_b.py`. Do not edit by hand.",
        "",
        f"{meta['kept']} of {meta['drawn']} sampled trajectories "
        f"({meta['kept'] / meta['drawn']:.1%}) had a pace "
        f"of {meta['band'][0]:g}x to {meta['band'][1]:g}x on Nov 1, 2026 and are kept. "
        "Parameters are drawn from AI Futures' August 2026 distribution for "
        f"{meta['forecaster'].title()} "
        f"(`config/{CONFIGS[meta['forecaster']]}`), seed {meta['seed']}. "
        f"Median pace of the kept trajectories: {meta['median_pace']:.2f}x. "
        "Delays are paired: each trajectory under a scenario against the same trajectory with no "
        "pacing.",
        "",
        "## All kept trajectories",
        "",
    ]
    out += _table(summarize(rows))
    out += [
        "",
        f"## Trajectories with no superhuman AI researcher before Nov 1, 2026 ({n_sub} of "
        f"{meta['kept']})",
        "",
    ]
    out += _table(summarize(subset))
    out.append("")
    return "\n".join(out)


def figure(rows, meta) -> None:
    """Dot-and-interval chart for the trajectories consistent with no SAR on the reference date."""
    subset = not_yet(rows, pm.load_calibration()["reference_date"])
    summary = summarize(subset)
    kept = len({r["sample"] for r in subset})
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    surface, ink, ink2, grid, blue = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df", "#2a78d6"
    plt.rcParams["font.family"] = "DejaVu Sans"
    short = {
        "Human sign-off, no comprehension standard": "Human sign-off only",
        "Comprehension audits (central) + 3-month lag": "Central audits + 3-month lag",
        "Comprehension audits (central) + 9-month lag": "Central audits + 9-month lag",
        "Internal-use lag, 3 months": "3-month internal-use lag",
        "Internal-use lag, 9 months": "9-month internal-use lag",
    }
    hi = max(
        max((s["ted_ai_p75"] if s["ted_ai_p75"] == s["ted_ai_p75"] else T_END - 1) for s in summary)
        + 0.9,
        2029.0,
    )
    fig, ax = plt.subplots(figsize=(10.5, 0.52 * len(summary) + 1.9), facecolor=surface)
    ax.set_facecolor(surface)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(grid)
    ax.tick_params(colors=ink2, labelsize=9, length=0)
    ax.grid(True, axis="x", color=grid, linewidth=0.8)
    ax.set_axisbelow(True)
    for i, s in enumerate(summary):
        y = len(summary) - 1 - i
        lo_x = s["ted_ai_p25"]
        hi_x = s["ted_ai_p75"] if s["ted_ai_p75"] == s["ted_ai_p75"] else hi - 0.9
        med = s["ted_ai_median"]
        if lo_x == lo_x:
            ax.plot(
                [lo_x, hi_x], [y, y], color=blue, linewidth=3, alpha=0.35, solid_capstyle="round"
            )
        if med == med:
            ax.plot(
                med, y, "o", color=blue, markersize=9, markeredgecolor=surface, markeredgewidth=2
            )
        delay = s["ted_ai_delay_months_median"]
        label = date_text(med) + ("" if i == 0 else f"   {_delay(delay)}")
        ax.text(
            (hi_x if lo_x == lo_x else 2027.0) + 0.08, y, label, va="center", fontsize=9, color=ink
        )
    ax.set_yticks(range(len(summary)))
    ax.set_yticklabels(
        [short.get(s["scenario"], s["scenario"]) for s in reversed(summary)],
        fontsize=9.5,
        color=ink,
    )
    ax.set_ylim(-0.7, len(summary) - 0.3)
    ax.set_xlim(2027.0, hi)
    years = np.arange(2027, math.floor(hi) + 1)
    ax.set_xticks(years)
    ax.set_xticklabels([str(int(y)) for y in years])
    ax.set_title(
        "Median date of TED-AI under each pacing scenario",
        loc="left",
        fontsize=12,
        color=ink,
        pad=44,
    )
    ax.text(
        0.0,
        1.035,
        f"AI Futures Model, {kept} sampled trajectories with a pace of "
        f"{meta['band'][0]:g}x to {meta['band'][1]:g}x on Nov 1, 2026 and no superhuman AI "
        "researcher by "
        "then.\nDot: median. Bar: middle half of trajectories. Label: median date and median delay "
        "against no pacing.",
        transform=ax.transAxes,
        fontsize=9,
        color=ink2,
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig4_ted_ai_by_scenario.png", dpi=200, facecolor=surface)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=2000)
    ap.add_argument("--forecaster", choices=sorted(CONFIGS), default="daniel")
    ap.add_argument("--seed", type=int, default=20261110)
    ap.add_argument("--pace-low", type=float, default=1.5)
    ap.add_argument("--pace-high", type=float, default=2.0)
    ap.add_argument("--supervision", default="anthropic")
    ap.add_argument("--aifm-path", default=str(DEFAULT_AIFM_PATH))
    ap.add_argument("--workers", type=int, default=mp.cpu_count())
    ap.add_argument(
        "--scenarios", default="", help="scenario names separated by semicolons; default is all ten"
    )
    ap.add_argument("--tag", default="", help="suffix for output files, to keep runs apart")
    ap.add_argument(
        "--only",
        default="",
        help="comma-separated sample indices to run, skipping the rest. 'kept' reruns just the "
        "trajectories in the existing CSV: same results as a full run, in less time",
    )
    ap.add_argument(
        "--replot",
        action="store_true",
        help="rebuild the table and figure from results/model_b_montecarlo.csv",
    )
    args = ap.parse_args()
    if args.replot:
        with open(OUT / "model_b_montecarlo.csv") as f:
            lines = [line for line in f if not line.startswith("#")]
        rows = [
            dict(
                sample=int(r["sample"]),
                pace_nov_2026=float(r["pace_nov_2026"]),
                scenario=r["scenario"],
                sar=float(r["sar"]),
                ted_ai=float(r["ted_ai"]),
                asi=float(r["asi"]),
            )
            for r in csv.DictReader(lines)
        ]
        with open(OUT / "model_b_montecarlo_meta.json") as f:
            meta = json.load(f)
        meta["band"] = tuple(meta["band"])
        (OUT / "tables_montecarlo.md").write_text(markdown(rows, meta))
        figure(rows, meta)
        return
    path, band = Path(args.aifm_path), (args.pace_low, args.pace_high)
    scenarios = [x.strip() for x in args.scenarios.split(";") if x.strip()] or SCENARIOS
    tag = f"_{args.tag}" if args.tag else ""
    OUT.mkdir(exist_ok=True)
    t0 = time.time()
    samples = draw_samples(path, args.forecaster, args.samples, args.seed)
    jobs, drawn = list(enumerate(samples)), None
    if args.only == "kept":
        with open(OUT / f"model_b_montecarlo{tag}.csv") as f:
            wanted = {
                int(r["sample"])
                for r in csv.DictReader(line for line in f if not line.startswith("#"))
            }
        with open(OUT / f"model_b_montecarlo{tag}_meta.json") as f:
            drawn = json.load(f)["drawn"]
        jobs = [j for j in jobs if j[0] in wanted]
    elif args.only:
        wanted = {int(x) for x in args.only.split(",")}
        jobs = [j for j in jobs if j[0] in wanted]
    print(
        f"[{time.time() - t0:5.0f}s] drew {len(samples)} parameter sets, running {len(jobs)}",
        flush=True,
    )
    rows, paces = [], []
    with mp.Pool(
        args.workers, initializer=_init, initargs=(path, band, args.supervision, scenarios)
    ) as pool:
        for done, (_index, pace, got) in enumerate(
            pool.imap_unordered(_work, jobs, chunksize=4), 1
        ):
            paces.append(pace)
            rows.extend(got)
            if done % (10 if drawn else 100) == 0 or done == len(jobs):
                print(
                    f"[{time.time() - t0:5.0f}s] {done} run, {len(rows) // len(scenarios)} kept",
                    flush=True,
                )
    rows.sort(key=lambda r: (r["sample"], SCENARIOS.index(r["scenario"])))
    valid = [p for p in paces if p == p]
    kept = [r["pace_nov_2026"] for r in rows if r["scenario"] == "No pacing"]
    meta = dict(
        drawn=drawn or len(valid),
        kept=len(kept),
        band=band,
        forecaster=args.forecaster,
        seed=args.seed,
        median_pace=float(np.median(kept)) if kept else float("nan"),
    )
    with open(OUT / f"model_b_montecarlo{tag}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    with open(OUT / f"model_b_montecarlo{tag}_meta.json", "w") as f:
        json.dump(meta, f, indent=1)
    (OUT / f"tables_montecarlo{tag}.md").write_text(markdown(rows, meta))
    if not tag:
        figure(rows, meta)
    shares = {
        f"{a:g}-{b:g}": sum(1 for p in valid if a <= p < b) / max(len(valid), 1)
        for a, b in ((0, 1.25), (1.25, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 1e9))
    }
    print(
        f"[{time.time() - t0:5.0f}s] done. pace on Nov 1, 2026 across the draws run: {shares}",
        flush=True,
    )


if __name__ == "__main__":
    main()
