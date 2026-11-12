"""Probability of a superhuman AI researcher and of TED-AI by date, by pacing scenario,
under two models of how fast AI research judgment ("research taste") improves.

Both taste models start from AI Futures' base case in "Research taste linear
extrapolation" (2026-11-10): AI research taste of -3.5 SD on Sep 25, 2026.

    baseline   +3 SD per year of 2025 progress (AI Futures' base case)
    slow       +1 SD per year of 2025 progress

Every other parameter is drawn with AI Futures' own sampler and August 2026
configuration. A draw is kept if its pace of progress on Nov 1, 2026 is in the
band METR measured. With taste that low on the reference date, AI judgment adds
nothing to the pace by then, so the same draws are kept under both taste models
and the pace has to come from coding.

Each kept trajectory runs under every pacing scenario with the link from
comprehension to human judgment switched on (pacing_model.lab_choice), and
under two scenarios with the link off for comparison.

Usage:
    python montecarlo_taste.py --samples 8000        # about an hour on 4 cores
    python montecarlo_taste.py --replot              # rebuild tables and figures from the CSV

Writes results/model_b_taste.csv, results/tables_taste.md,
results/fig5_probability_by_date_gates.png and
results/fig6_probability_by_date_other.png.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import math
import multiprocessing as mp
import time
from pathlib import Path

import numpy as np

import pacing_model as pm
from aifm_adapter import DEFAULT_AIFM_PATH, Aifm
from montecarlo_b import draw_samples

OUT = pm.HERE / "results"
SCENARIOS = ["No pacing", "Human sign-off, no comprehension standard", "Comprehension audits, light",
             "Comprehension audits, central", "Comprehension audits, strict",
             "Internal-use lag, 3 months", "Internal-use lag, 9 months", "R&D compute cut 3x",
             "Comprehension audits (central) + 3-month lag",
             "Comprehension audits (central) + 9-month lag"]
UNLINKED = ["No pacing", "Comprehension audits, central"]     # also run with the link off
T_END = 2040.0               # a milestone not reached by then is recorded as later than this
TASTE_AT_AC = "ai_research_taste_at_coding_automation_anchor_sd"
SLOPE = "ai_research_taste_slope"
_STATE = {}


def taste_models(cal: dict) -> dict[str, float]:
    t = cal["taste_models"]
    return {"baseline": float(t["slope_baseline"]), "slow": float(t["slope_slow"])}


def pinned(params: dict, first: Aifm, slope_per_2025_year: float, level_sd: float, date: float,
           aifm_path: Path, t_ref: float) -> Aifm:
    """The model with AI research taste at `level_sd` on `date`, improving by
    `slope_per_2025_year` SD per year of progress at the 2024 to mid-2025 rate.

    `first` is the same draw run with negligible taste. It supplies the progress
    on `date`, the progress at the automated coder anchor and the 2025 rate.
    """
    slope = slope_per_2025_year / first.rate0                 # SD per unit of progress
    if params.get("taste_schedule_type", "SDs per progress-year") == "SDs per progress-year":
        # AIFM divides the input by the progress rate at its anchor date. Undo that.
        slope_input = slope * params[SLOPE] / first.params.ai_research_taste_slope
    else:
        slope_input = slope
    at_ac = level_sd + slope * (first.params.progress_at_aa - first.capability_at(date))
    return Aifm(dict(params, **{SLOPE: slope_input, TASTE_AT_AC: at_ac}), aifm_path, t_ref, horizon=2030.0)


def _init(aifm_path, band, supervision):
    import warnings
    warnings.filterwarnings("ignore")     # AIFM overflows harmlessly on extreme draws
    np.seterr(all="ignore")
    logging.disable(logging.WARNING)
    cal = pm.load_calibration()
    _STATE.update(path=aifm_path, band=band, supervision=supervision, cal=cal,
                  policies={p.name: p for p in pm.standard_policies(cal)})


def _work(job):
    """Run one sampled parameter set. Returns (index, pace, rows); rows is empty unless kept."""
    index, params = job
    cal = _STATE["cal"]
    t_ref, spec = cal["reference_date"], cal["taste_models"]
    try:
        first = Aifm(dict(params, **{TASTE_AT_AC: -30.0}), _STATE["path"], t_ref, horizon=2030.0)
        pace = first.base_pace(t_ref)
    except Exception:
        return index, float("nan"), []
    lo, hi = _STATE["band"]
    if not lo <= pace <= hi:
        return index, pace, []
    rows = []
    try:
        for name, slope in taste_models(cal).items():
            m = pinned(params, first, slope, spec["level_sd"], spec["date"], _STATE["path"], t_ref)
            common = dict(sample=index, pace_nov_2026=m.base_pace(t_ref), taste_model=name,
                          taste_sd_on_date=m.taste_sd(m.capability_at(spec["date"])),
                          slope_per_2025_year=m.params.ai_research_taste_slope * m.rate0,
                          ac_date=m.milestones.get("AC", (float("nan"),))[0])
            m.fit_supervision(_STATE["supervision"], cal)
            for link, names in ((True, SCENARIOS), (False, UNLINKED)):
                m.use_calibration(cal, link=link)
                for scenario in names:
                    run = m.simulate(_STATE["policies"][scenario], t_end=T_END, step=0.006, stop_at="TED-AI")
                    s = m.summarize(run)
                    rows.append(dict(common, link=int(link), scenario=scenario,
                                     sar=s.get("t_sar", float("nan")), ted_ai=s.get("t_ted_ai", float("nan"))))
    except Exception:
        return index, pace, []
    return index, pace, rows


# --------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------
def quantile(values, q: float) -> float:
    """Quantile where a missing date means later than T_END. nan if the quantile is missing."""
    v = sorted(math.inf if x != x else x for x in values)
    x = v[min(len(v) - 1, int(math.floor(q * (len(v) - 1) + 0.5)))]
    return float("nan") if x == math.inf else x


def by_date(values, date: float) -> float:
    """Share of trajectories that reach the milestone before `date`."""
    return sum(1 for x in values if x == x and x < date) / max(len(values), 1)


def date_text(x: float) -> str:
    return f"after {T_END - 1:.0f}" if x != x else pm.fmt_date(x)


def delay_text(x: float) -> str:
    return f"past {T_END - 1:.0f}" if x != x else f"{x:+.0f} mo"


def select(rows, model: str, link: int, scenario: str) -> dict[int, dict]:
    return {r["sample"]: r for r in rows
            if r["taste_model"] == model and r["link"] == link and r["scenario"] == scenario}


def delays(rows_by_sample: dict, base_by_sample: dict, key: str) -> list[float]:
    """Paired delay in months over trajectories that reach the milestone with no pacing."""
    out = []
    for sample, r in rows_by_sample.items():
        b = base_by_sample[sample][key]
        if b == b:
            out.append(math.nan if r[key] != r[key] else (r[key] - b) * 12.0)
    return out


def _days(xs) -> str:
    xs = [x for x in xs if x == x]
    return "n/a" if not xs else f"{float(np.median(xs)) * 365.25:+.0f} days"


def markdown(rows, meta) -> str:
    cal = pm.load_calibration()
    spec = cal["taste_models"]
    out = ["# Probability of each milestone by date, by taste model and pacing scenario", "",
           "Written by `montecarlo_taste.py`. Do not edit by hand.", "",
           f"{meta['kept']} of {meta['drawn']} sampled trajectories ({meta['kept'] / meta['drawn']:.1%}) had a pace "
           f"of {meta['band'][0]:g}x to {meta['band'][1]:g}x on Nov 1, 2026 with AI research taste too low to "
           "contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 "
           f"distribution for {meta['forecaster'].title()}, seed {meta['seed']}. "
           f"Median pace of the kept trajectories: {meta['median_pace']:.2f}x. "
           f"Both taste models put AI research taste at {spec['level_sd']:+g} SD on {pm.fmt_date(spec['date'])}. "
           "Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same "
           f"trajectory with no pacing. A milestone not reached by the end of {T_END - 1:.0f} counts as later "
           "than that. The link from comprehension to human judgment is on except where a table says otherwise.",
           ""]
    years = {"baseline": (2028.0, 2029.0, 2030.0), "slow": (2029.0, 2031.0, 2035.0)}
    milestones = (("sar", "Superhuman AI researcher"), ("ted_ai", "TED-AI"))
    models = taste_models(cal)
    head = " | ".join(f"{slope:+g} SD: median {label}" + (f" | {slope:+g} SD: median delay" if True else "")
                      for slope in models.values() for label in ("superhuman AI researcher", "TED-AI"))
    out += ["## Summary", "", f"| Scenario | {head} |", "|---|" + "---|" * (4 * len(models))]
    for name in SCENARIOS:
        cells = []
        for model in models:
            base = select(rows, model, 1, "No pacing")
            got = select(rows, model, 1, name)
            for key, _ in milestones:
                cells.append(date_text(quantile([r[key] for r in got.values()], 0.5)))
                cells.append("" if name == "No pacing" else delay_text(quantile(delays(got, base, key), 0.5)))
        out.append(f"| {name} | " + " | ".join(cells) + " |")
    out.append("")
    for model, slope in taste_models(cal).items():
        base = select(rows, model, 1, "No pacing")
        out += [f"## Taste improves {slope:+g} SD per year of 2025 progress ({model})", ""]
        for key, label in milestones:
            ys = years[model]
            out += [f"### {label}", "",
                    "| Scenario | Median date | Middle half of trajectories | "
                    + " | ".join(f"By start of {y:.0f}" for y in ys) + " | Median delay | Delay, upper quartile |",
                    "|---|---|---|" + "---|" * len(ys) + "---|---|"]
            for name in SCENARIOS:
                got = select(rows, model, 1, name)
                v = [r[key] for r in got.values()]
                d = delays(got, base, key)
                first = name == "No pacing"
                out.append(f"| {name} | {date_text(quantile(v, 0.5))} | {date_text(quantile(v, 0.25))} to "
                           f"{date_text(quantile(v, 0.75))} | "
                           + " | ".join(f"{by_date(v, y):.0%}" for y in ys) + " | "
                           + ("" if first else delay_text(quantile(d, 0.5))) + " | "
                           + ("" if first else delay_text(quantile(d, 0.75))) + " |")
            out.append("")
        # What the link changes
        off = select(rows, model, 0, "No pacing")
        audit_on = select(rows, model, 1, "Comprehension audits, central")
        audit_off = select(rows, model, 0, "Comprehension audits, central")
        out += ["### What the link from comprehension to judgment changes", "",
                "| | Link off | Link on |", "|---|---|---|"]
        for key, label in milestones:
            out.append(f"| No pacing: median date of {label[0].lower() + label[1:] if key == 'sar' else label} | "
                       f"{date_text(quantile([r[key] for r in off.values()], 0.5))} | "
                       f"{date_text(quantile([r[key] for r in base.values()], 0.5))} |")
        for key, label in milestones:
            out.append(f"| Central audits: median delay to {label[0].lower() + label[1:] if key == 'sar' else label} | "
                       f"{delay_text(quantile(delays(audit_off, off, key), 0.5))} | "
                       f"{delay_text(quantile(delays(audit_on, base, key), 0.5))} |")
        shift = {key: [base[k][key] - off[k][key] for k in base] for key, _ in milestones}
        out += ["", f"Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher "
                f"by a median of {_days(shift['sar'])} and TED-AI by {_days(shift['ted_ai'])}.", ""]
        # Split by whether coding was already automated on the reference date
        early = {k for k, r in base.items() if r["ac_date"] <= cal["reference_date"]}
        out += ["### Split by when coding is fully automated", "",
                "| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median "
                "TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay "
                "to TED-AI | 3-month lag: median delay to TED-AI |", "|---|---|---|---|---|---|---|"]
        lag3 = select(rows, model, 1, "Internal-use lag, 3 months")
        for label, keys in (("Before Nov 1, 2026", early), ("Nov 1, 2026 or later", set(base) - early)):
            if not keys:
                continue
            sub = lambda d: {k: d[k] for k in keys}
            out.append(f"| {label} | {len(keys)} | {date_text(quantile([base[k]['sar'] for k in keys], 0.5))} | "
                       f"{date_text(quantile([base[k]['ted_ai'] for k in keys], 0.5))} | "
                       f"{delay_text(quantile(delays(sub(audit_on), base, 'sar'), 0.5))} | "
                       f"{delay_text(quantile(delays(sub(audit_on), base, 'ted_ai'), 0.5))} | "
                       f"{delay_text(quantile(delays(sub(lag3), base, 'ted_ai'), 0.5))} |")
        out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SHORT = {"Human sign-off, no comprehension standard": "Human sign-off only",
         "Comprehension audits, light": "Audits, light",
         "Comprehension audits, central": "Audits, central",
         "Comprehension audits, strict": "Audits, strict",
         "Internal-use lag, 3 months": "3-month internal-use lag",
         "Internal-use lag, 9 months": "9-month internal-use lag",
         "Comprehension audits (central) + 3-month lag": "Central audits + 3-month lag",
         "Comprehension audits (central) + 9-month lag": "Central audits + 9-month lag"}
# name -> (color, dash). One hue per mechanism; audit strictness and lag length by dash.
# Hues are the first three slots of the dataviz reference palette, which pass its
# all-pairs colorblind check together. Ink and gray carry the two reference lines.
STYLE_GATES = {
    "No pacing": (INK, "-"),
    "Human sign-off, no comprehension standard": ("#7a7974", "-"),
    "Comprehension audits, light": ("#2a78d6", (0, (1, 1.6))),
    "Comprehension audits, central": ("#2a78d6", "-"),
    "Comprehension audits, strict": ("#2a78d6", (0, (5, 2))),
}
STYLE_OTHER = {
    "No pacing": (INK, "-"),
    "R&D compute cut 3x": ("#7a7974", "-"),
    "Comprehension audits, central": ("#2a78d6", "-"),
    "Internal-use lag, 3 months": ("#eb6834", "-"),
    "Internal-use lag, 9 months": ("#eb6834", (0, (5, 2))),
    "Comprehension audits (central) + 3-month lag": ("#1baf7a", "-"),
    "Comprehension audits (central) + 9-month lag": ("#1baf7a", (0, (5, 2))),
}


def _curve(values, lo: float, hi: float):
    """Step curve of the share of trajectories that have reached the milestone."""
    v = np.sort(np.array([x for x in values if x == x and x <= hi]))
    n = max(len(values), 1)
    x = np.concatenate([[lo], np.maximum(v, lo), [hi]])
    y = np.concatenate([[0.0], np.arange(1, len(v) + 1) / n, [len(v) / n]])
    return x, y


def figure(rows, meta, styles: dict, path: Path, title: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    cal = pm.load_calibration()
    plt.rcParams["font.family"] = "DejaVu Sans"
    models = taste_models(cal)
    span = {"baseline": (2027.0, 2031.0), "slow": (2027.0, T_END)}
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.2), facecolor=SURFACE)
    for i, (model, slope) in enumerate(models.items()):
        lo, hi = span[model]
        for j, (key, label) in enumerate((("sar", "Superhuman AI researcher"), ("ted_ai", "TED-AI"))):
            ax = axes[i, j]
            ax.set_facecolor(SURFACE)
            for side in ("top", "right", "left"):
                ax.spines[side].set_visible(False)
            ax.spines["bottom"].set_color(GRID)
            ax.tick_params(colors=INK2, labelsize=9, length=0)
            ax.tick_params(axis="x", pad=7)
            ax.grid(True, axis="y", color=GRID, linewidth=0.8)
            ax.set_axisbelow(True)
            for name, (color, dash) in styles.items():
                got = select(rows, model, 1, name)
                x, y = _curve([r[key] for r in got.values()], lo, hi)
                ax.step(x, y, where="post", color=color, linestyle=dash, linewidth=2.0,
                        zorder=3 if name == "No pacing" else 2)
            ax.set_xlim(lo, hi)
            ax.set_ylim(-0.02, 1.03)
            years = np.arange(int(lo), int(hi) + 1, 1 if hi - lo <= 6 else 2)
            ax.set_xticks(years)
            ax.set_xticklabels([str(int(y)) for y in years])
            ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
            ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"] if j == 0 else [""] * 5)
            ax.set_title(f"{label}, taste {slope:+g} SD a year", loc="left", fontsize=10.5, color=INK, pad=8)
    handles = [Line2D([0], [0], color=c, linestyle=d, linewidth=2.2) for c, d in styles.values()]
    fig.legend(handles, [SHORT.get(n, n) for n in styles], loc="lower center", ncol=len(styles) if len(styles) <= 5 else 4,
               frameon=False, fontsize=9.5, labelcolor=INK, handlelength=3.2, columnspacing=2.2)
    fig.suptitle(title, x=0.045, y=0.985, ha="left", fontsize=13, color=INK)
    fig.text(0.045, 0.94,
             f"Share of {meta['kept']} sampled AI Futures Model trajectories that have reached each milestone "
             f"by the date shown. Pace {meta['band'][0]:g}x to {meta['band'][1]:g}x on Nov 1, 2026.\n"
             f"AI research taste {cal['taste_models']['level_sd']:+g} SD in Sep 2026, improving per year of 2025 "
             "progress as each panel says. Pacing starts Jan 1, 2027. Top row ends 2031, bottom row 2040.",
             fontsize=9, color=INK2, va="top")
    fig.tight_layout(rect=(0.02, 0.085 if len(styles) > 5 else 0.055, 1.0, 0.91), h_pad=2.0)
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def report(rows, meta) -> None:
    (OUT / "tables_taste.md").write_text(markdown(rows, meta))
    figure(rows, meta, STYLE_GATES, OUT / "fig5_probability_by_date_gates.png",
           "Probability of each milestone by date: sign-off and comprehension audits")
    figure(rows, meta, STYLE_OTHER, OUT / "fig6_probability_by_date_other.png",
           "Probability of each milestone by date: lags, compute cuts and combinations")


def load() -> tuple[list[dict], dict]:
    with open(OUT / "model_b_taste.csv") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["sample"], r["link"] = int(r["sample"]), int(r["link"])
        for k in ("pace_nov_2026", "taste_sd_on_date", "slope_per_2025_year", "ac_date", "sar", "ted_ai"):
            r[k] = float(r[k])
    with open(OUT / "model_b_taste_meta.json") as f:
        meta = json.load(f)
    meta["band"] = tuple(meta["band"])
    return rows, meta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=8000)
    ap.add_argument("--forecaster", choices=("daniel", "eli"), default="daniel")
    ap.add_argument("--seed", type=int, default=20261110)
    ap.add_argument("--pace-low", type=float, default=1.5)
    ap.add_argument("--pace-high", type=float, default=2.0)
    ap.add_argument("--supervision", default="anthropic")
    ap.add_argument("--aifm-path", default=str(DEFAULT_AIFM_PATH))
    ap.add_argument("--workers", type=int, default=mp.cpu_count())
    ap.add_argument("--only", default="",
                    help="'kept' reruns just the trajectories in the existing CSV, skipping the pace filter "
                         "over all draws. Same results as a full run, in less time")
    ap.add_argument("--replot", action="store_true", help="rebuild tables and figures from the CSV")
    args = ap.parse_args()
    if args.replot:
        report(*load())
        return
    path, band = Path(args.aifm_path), (args.pace_low, args.pace_high)
    OUT.mkdir(exist_ok=True)
    t0 = time.time()
    samples = draw_samples(path, args.forecaster, args.samples, args.seed)
    print(f"[{time.time() - t0:5.0f}s] drew {len(samples)} parameter sets", flush=True)
    jobs, drawn = list(enumerate(samples)), None
    if args.only == "kept":
        old_rows, old_meta = load()
        wanted, drawn = {r["sample"] for r in old_rows}, old_meta["drawn"]
        jobs = [j for j in jobs if j[0] in wanted]
    rows, paces = [], []
    per = len(taste_models(pm.load_calibration())) * (len(SCENARIOS) + len(UNLINKED))
    with mp.Pool(args.workers, initializer=_init, initargs=(path, band, args.supervision)) as pool:
        for done, (index, pace, got) in enumerate(pool.imap_unordered(_work, jobs, chunksize=2), 1):
            paces.append(pace)
            rows.extend(got)
            if done % (10 if drawn else 200) == 0 or done == len(jobs):
                print(f"[{time.time() - t0:5.0f}s] {done} run, {len(rows) // per} kept", flush=True)
    order = {name: i for i, name in enumerate(SCENARIOS)}
    rows.sort(key=lambda r: (r["sample"], r["taste_model"], -r["link"], order[r["scenario"]]))
    valid = [p for p in paces if p == p]
    kept = sorted({r["sample"] for r in rows})
    kept_pace = [r["pace_nov_2026"] for r in rows
                 if r["taste_model"] == "baseline" and r["link"] == 1 and r["scenario"] == "No pacing"]
    meta = dict(drawn=drawn or len(valid), kept=len(kept), band=band, forecaster=args.forecaster, seed=args.seed,
                median_pace=float(np.median(kept_pace)) if kept_pace else float("nan"))
    with open(OUT / "model_b_taste.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    with open(OUT / "model_b_taste_meta.json", "w") as f:
        json.dump(meta, f, indent=1)
    report(rows, meta)
    print(f"[{time.time() - t0:5.0f}s] done", flush=True)


if __name__ == "__main__":
    main()
