"""Run every scenario and write results/ (CSV tables, a Markdown summary, figures).

Usage:
    python run_all.py                      # Model A and Model B
    python run_all.py --skip-aifm          # Model A only
    python run_all.py --aifm-path PATH     # AIFM checkout at PATH

Model B needs a checkout of github.com/AI-Futures-Project/aifm-public
(commit 1c40ecd) and takes about five minutes. Model A takes under a minute.
"""
from __future__ import annotations

import argparse
import csv
import math
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

import pacing_model as pm

OUT = pm.HERE / "results"
REPORT_END = 2029.0          # results past this date are outside what the inputs support
CENTRAL = "Comprehension audits, central"
SIGNOFF = "Human sign-off, no comprehension standard"


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def at(run: dict, key: str, when: float) -> float:
    return pm.value_at(run["t"], run[key], when)


def kept(run: dict, when: float) -> float:
    """Research effort under the policy over effort with no gate at the same capability."""
    if when != when or when > run["t"][-1]:
        return float("nan")
    return at(run, "rd_uplift", when) / at(run, "rd_free", when)


def full_understanding_date(run: dict) -> float:
    """On a no-gate run: when understanding everything deployed would take all researcher time."""
    ok = ~np.isnan(run["comprehension_share"])
    return pm.first_crossing(run["t"][ok], run["comprehension_share"][ok], 1.0)


def write_csv(path: Path, rows: list[dict]) -> None:
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4g}" if isinstance(v, float) else v) for k, v in r.items()})


def months_between(a: float, b: float) -> float:
    return (b - a) * 12.0


def gate_snapshot(run: dict, when: float) -> dict:
    if when > run["t"][-1]:
        return dict(effort_kept=float("nan"), time_on_comprehension=float("nan"),
                    labor_used=float("nan"), deployed_per_year=float("nan"),
                    deployed_share_of_experiments=float("nan"))
    return dict(effort_kept=kept(run, when), time_on_comprehension=at(run, "comprehension_share", when),
                labor_used=at(run, "labor", when), deployed_per_year=at(run, "deployed", when),
                deployed_share_of_experiments=at(run, "deployed", when) / at(run, "experiments", when))


# --------------------------------------------------------------------------
def run_model_a(cal: dict):
    rows, runs = [], {}
    for kind in ("none", "anthropic", "openai", "openai_runtime"):
        m, _ = pm.build_a(cal, kind)
        base_sar = None
        for pol in pm.standard_policies(cal):
            r = m.simulate(pol, t_end=2032.0)
            s = pm.summarize_a(m, r)
            if pol.name == "No pacing":
                base_sar = s["t_sar"]
            row = dict(model="A", supervision=kind, mechanism=pol.name,
                       sar_capability_date=s["t_sar"],
                       sar_delay_months=months_between(base_sar, s["t_sar"]),
                       pace_mid_2027=s["pace_2027.5"], pace_jan_2028=s["pace_2028.0"],
                       pace_jan_2029=at(r, "pace", 2029.0),
                       date_pace_3x=s["t_pace_3x"], date_pace_10x=s["t_pace_10x"],
                       progress_by_jan_2029=at(r, "Y", 2029.0) - at(r, "Y", m.t_ref))
            row.update({f"{k}_jul_2027": v for k, v in gate_snapshot(r, 2027.5).items()})
            row.update({f"{k}_jan_2028": v for k, v in gate_snapshot(r, 2028.0).items()})
            rows.append(row)
            runs[(kind, pol.name)] = r
        log(f"Model A, supervision={kind}: u0={m.u0:.4f} D_U={m.D_U:.3f} labor uplift at ref "
            f"{m.labor_ref:.1f} done")
        runs[(kind, "_model")] = m
    return rows, runs


def sensitivity_a(cal: dict):
    """One change at a time, Model A with the Anthropic supervision fit, central gate."""
    g0 = pm.gate_from_calibration(cal)
    start = cal["policy_start"]
    cases = [
        ("Central case", {}, g0, start),
        ("AI-attributable pace today 1.25x (METR low end)", dict(pace_ref=1.25), g0, start),
        ("AI-attributable pace today 2.6x (METR high end)", dict(pace_ref=2.6), g0, start),
        ("Uplift slope from self-reports (0.32 baseline-years per doubling)", dict(D_U=0.32), g0, start),
        ("Labor exponent 1/3", dict(alpha=1 / 3), g0, start),
        ("Labor exponent 2/3", dict(alpha=2 / 3), g0, start),
        ("Software share of progress 0.5", dict(sigma=0.5), g0, start),
        ("Weaker diminishing returns (0.7 research-stock doublings per baseline-year)",
         dict(g_R=0.7 * pm.LN2), g0, start),
        ("Compute complements labor (CES, ceiling 60x)", dict(rho=-0.169), g0, start),
        ("Unsupervised work trails by 14 months", dict(al5_lag_months=14), g0, start),
        ("Unsupervised work capped at 90% of tasks", dict(al5_ceiling=0.9), g0, start),
        ("OpenAI intervention fit without January", dict(supervision="openai", openai_from=2026.1),
         g0, start),
        ("Gate: deployed changes grow slowly with AI labor (all elasticities 0.2)", {},
         pm.rescale(g0, elasticity=0.2), start),
        ("Gate: deployed changes grow fast with AI labor (all elasticities 0.7)", {},
         pm.rescale(g0, elasticity=0.7), start),
        ("Gate: deployed changes grow in proportion to AI labor (elasticity 1)", {},
         pm.rescale(g0, elasticity=1.0), start),
        ("Gate: one third as many deployed changes today (5% of researcher time)", {},
         pm.rescale(g0, counts=1 / 3), start),
        ("Gate: twice as many deployed changes today (30% of researcher time)", {},
         pm.rescale(g0, counts=2.0), start),
        ("Gate: value tail index 1.3 (heavier tail)", {}, replace(g0, tail=1.3), start),
        ("Gate: value tail index 3.0 (thinner tail)", {}, replace(g0, tail=3.0), start),
        ("Gate: all progress rides on training improvements", {},
         pm.rescale(g0, weights={"training_improvements": 1.0, "dataset_updates": 1e-9,
                                 "system_software_changes": 1e-9}), start),
        ("Gate: lab keeps 75% of deployed changes understood", {}, replace(g0, coverage=0.75), start),
        ("Gate: AI halves comprehension hours per baseline-year, floor 1/4", {},
         replace(g0, hours_halving=1.0, hours_floor=0.25), start),
        ("Gate: changes get harder to understand (hours double per baseline-year)", {},
         replace(g0, hours_doubling=1.0), start),
        ("Gate starts July 2027", {}, g0, 2027.5),
    ]
    rows = []
    for label, model_kw, g, begin in cases:
        kw = dict(supervision="anthropic")
        kw.update(model_kw)
        try:
            m, _ = pm.build_a(cal, **kw)
        except Exception as e:                      # calibration can fail at extremes
            log(f"sensitivity '{label}' skipped: {e}")
            continue
        m.changes = g
        free = m.simulate(pm.Policy("No pacing", start=begin))
        gated = m.simulate(pm.Policy("gate", start=begin, gate=g))
        sf, sg = pm.summarize_a(m, free), pm.summarize_a(m, gated)
        rows.append(dict(case=label, uplift_today=m.labor_ref,
                         nopacing_sar=sf["t_sar"], nopacing_pace_jan_2028=sf["pace_2028.0"],
                         nopacing_full_understanding_impossible=full_understanding_date(free),
                         gate_sar=sg["t_sar"],
                         gate_sar_delay_months=months_between(sf["t_sar"], sg["t_sar"]),
                         gate_pace_jan_2028=sg["pace_2028.0"], gate_pace_jan_2029=at(gated, "pace", 2029.0),
                         gate_date_pace_10x=sg["t_pace_10x"],
                         gate_effort_kept_jan_2028=kept(gated, 2028.0),
                         gate_time_on_comprehension_jan_2028=at(gated, "comprehension_share", 2028.0)))
    return rows


def run_model_b(cal: dict, aifm_path: Path):
    from aifm_adapter import Aifm, published_example
    rows, runs = [], {}
    m = published_example(aifm_path, cal["reference_date"])
    log(f"Model B (AI Futures' Nov 10 example on the public code): pace May {m.base_pace(2026.33):.2f}, "
        f"Nov {m.base_pace(cal['reference_date']):.2f}; milestones "
        f"{ {k: pm.fmt_date(v[0]) for k, v in m.milestones.items()} }")
    published = Aifm({}, aifm_path, cal["reference_date"])
    short = [p for p in pm.standard_policies(cal) if p.name in ("No pacing", CENTRAL)]
    variants = [("Nov 10 example", m, ("anthropic", "openai", "none"), pm.standard_policies(cal)),
                ("as published Aug 2026", published, ("anthropic",), short)]
    for label, model, kinds, policies in variants:
        model.use_calibration(cal)
        for kind in kinds:
            model.fit_supervision(kind, cal)
            base = None
            for pol in policies:
                r = model.simulate(pol, t_end=2032.0)
                s = model.summarize(r)
                if pol.name == "No pacing":
                    base = s
                row = dict(model="B", variant=label, supervision=kind, mechanism=pol.name,
                           ac_date=s.get("t_ac", float("nan")), sar_date=s.get("t_sar", float("nan")),
                           sar_delay_months=months_between(base["t_sar"], s["t_sar"]),
                           ted_ai_date=s.get("t_ted_ai", float("nan")),
                           asi_date=s.get("t_asi", float("nan")),
                           asi_delay_months=months_between(base["t_asi"], s["t_asi"]),
                           pace_mid_2027=s["pace_2027.5"], pace_jan_2028=s["pace_2028.0"],
                           pace_jan_2029=at(r, "pace", 2029.0),
                           date_pace_3x=s["t_pace_3x"], date_pace_10x=s["t_pace_10x"])
                row.update({f"{k}_jul_2027": v for k, v in gate_snapshot(r, 2027.5).items()})
                row.update({f"{k}_jan_2028": v for k, v in gate_snapshot(r, 2028.0).items()})
                rows.append(row)
                runs[(label, kind, pol.name)] = r
                log(f"Model B [{label}, {kind}] {pol.name}: SAR {pm.fmt_date(s.get('t_sar', float('nan')))}"
                    f", ASI {pm.fmt_date(s.get('t_asi', float('nan')))}, pace Jan 2028 {s['pace_2028.0']:.2f}")
    runs["_base"] = m
    return rows, runs


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]   # fixed order, never cycled
FIG_MECHANISMS = ["No pacing", SIGNOFF, CENTRAL, "Internal-use lag, 9 months", "R&D compute cut 3x",
                  "Internal-use lag, 3 months"]
SHORT = {"No pacing": "No pacing", SIGNOFF: "Human sign-off only", CENTRAL: "Comprehension audits",
         "Internal-use lag, 9 months": "9-month internal-use lag",
         "R&D compute cut 3x": "R&D compute cut 3x",
         "Internal-use lag, 3 months": "3-month internal-use lag"}
B_BASE = ("Nov 10 example", "anthropic")


def _style(ax, title):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    ax.grid(True, axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=10)


def _ticks(ax, lo, hi):
    """Year ticks, with half-year ticks when the span is short."""
    ax.set_xlim(lo, hi)
    step = 0.5 if hi - lo <= 2.0 else 1.0
    first = math.ceil(lo / step) * step
    xs = np.arange(first, hi + 1e-9, step)
    ax.set_xticks(xs)
    ax.set_xticklabels([str(int(x)) if abs(x - round(x)) < 1e-9 else f"Jul {int(x)}" for x in xs])


def _percent(v, _=None) -> str:
    if v <= 0:
        return "0%"
    if v >= 0.01:
        return f"{v * 100:,.0f}%"
    return f"{v * 100:.3f}".rstrip("0").rstrip(".") + "%"


def figures(cal, runs_a, runs_b):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
    plt.rcParams["font.family"] = "DejaVu Sans"
    start = cal["policy_start"]
    ref = cal["reference_date"]

    # ---- Figure 1: pace by mechanism ------------------------------------
    panels = [("Model A: Cobb-Douglas with human time", lambda n: runs_a[("anthropic", n)], None)]
    if runs_b:
        panels.append(("Model B: AI Futures Model, Nov 10 example",
                       lambda n: runs_b[B_BASE + (n,)], runs_b["_base"]))
    fig, axes = plt.subplots(1, len(panels), figsize=(6.4 * len(panels), 5.0), sharey=True,
                             facecolor=SURFACE)
    axes = np.atleast_1d(axes)
    for ax, (title, get, aifm) in zip(axes, panels):
        _style(ax, title)
        for name, color in zip(FIG_MECHANISMS, SERIES):
            r = get(name)
            t, pace = r["t"], r["pace"]
            if aifm is not None:                    # show AIFM's own history before the reference date
                past = aifm.base["t"] < t[0]
                t = np.concatenate([aifm.base["t"][past], t])
                pace = np.concatenate([aifm.base["rate"][past] / aifm.rate0, pace])
            keep = (t >= 2026.5) & (t <= REPORT_END) & (pace <= 100.0)
            ax.plot(t[keep], pace[keep], color=color, linewidth=2, label=SHORT[name],
                    solid_capstyle="round")
            if r["t"][-1] < REPORT_END:             # the run ended inside the window
                ax.plot(t[keep][-1], pace[keep][-1], "o", color=color, markersize=6,
                        markeredgecolor=SURFACE, markeredgewidth=1.5)
        ax.set_yscale("log")
        ax.set_ylim(0.5, 100)
        ax.yaxis.set_major_locator(FixedLocator([0.5, 1, 2, 3, 5, 10, 30, 100]))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}x"))
        _ticks(ax, 2026.5, REPORT_END + 0.02)
        ax.axvline(start, color=INK2, linewidth=0.8, linestyle=(0, (3, 3)))
        ax.text(start + 0.03, 75, "pacing starts", fontsize=8, color=INK2, va="center")
    axes[0].set_ylabel("Pace of AI progress (1x = rate before Oct 2025)", fontsize=9, color=INK2)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=6, frameon=False, fontsize=9,
               labelcolor=INK, bbox_to_anchor=(0.5, 0.035), columnspacing=1.6)
    fig.text(0.5, 0.012, "A dot marks where a run ends: pace above 100x (Model A) or progress past "
             "AIFM's ASI level (Model B). Model B's pace peaks near that level and then falls. "
             "That is the AI Futures Model's own behavior.", ha="center", fontsize=8, color=INK2)
    fig.suptitle("Pace of AI progress under each pacing mechanism", x=0.012, ha="left",
                 fontsize=12, color=INK, y=0.975)
    fig.tight_layout(rect=(0, 0.09, 1, 0.94))
    fig.savefig(OUT / "fig1_pace_by_mechanism.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)

    # ---- Figure 2: human time per unit of work ---------------------------
    # Every schedule is evaluated along the same path: Model A with no pacing and
    # no supervision requirement. Realized human time is the larger of the
    # capability limit and the schedule in use.
    fig, ax = plt.subplots(figsize=(7.8, 4.8), facecolor=SURFACE)
    _style(ax, "Human time to direct a unit of R&D work under four extrapolations, Model A path")
    path = runs_a[("none", "No pacing")]
    before = (path["t"] >= 2026.0) & (path["t"] <= 2027.75)
    after = (path["t"] >= ref) & (path["t"] <= 2027.75)
    ax.plot(path["t"][before], path["tau"][before], color=SERIES[0], linewidth=2,
            label="Capability limit (Cotra uplift curve)")
    curves = [("anthropic", "Anthropic automation levels"),
              ("openai", "OpenAI zero-intervention horizon"),
              ("openai_runtime", "OpenAI agent runtime per human workday")]
    for (kind, label), color in zip(curves, SERIES[1:]):
        sup = runs_a[(kind, "_model")].supervision
        ax.plot(path["t"][after], [sup.h(y) for y in path["Y"][after]], color=color,
                linewidth=2, label=label)
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 1.2)
    ax.yaxis.set_major_locator(FixedLocator([0.001, 0.01, 0.1, 1.0]))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    _ticks(ax, 2026.0, 2027.75)
    ax.set_ylabel("Share of unaided human time still needed", fontsize=9, color=INK2)
    ax.legend(frameon=False, fontsize=9, labelcolor=INK, loc="lower left")
    fig.tight_layout()
    fig.savefig(OUT / "fig2_human_time_per_unit_work.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)

    # ---- Figure 3: deployed changes and the comprehension load -----------
    series = [("Model A", runs_a[("anthropic", "No pacing")], runs_a[("anthropic", CENTRAL)])]
    if runs_b:
        series.append(("Model B", runs_b[B_BASE + ("No pacing",)], runs_b[B_BASE + (CENTRAL,)]))
    lo, hi = ref, 2028.25
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.9), facecolor=SURFACE)
    specs = [
        ("Deployed changes as a share\nof experiments (no pacing)",
         lambda free, gated: (free["t"], free["deployed"] / free["experiments"]), (1e-5, 0.1), True),
        ("Researcher time needed to understand\neverything deployed (no pacing)",
         lambda free, gated: (free["t"], free["comprehension_share"]), (0.1, 100.0), True),
        ("Research effort kept under\ncentral comprehension audits",
         lambda free, gated: (gated["t"], gated["rd_uplift"] / gated["rd_free"]), (0.0, 1.05), False),
    ]
    for ax, (title, fn, ylim, logy) in zip(axes, specs):
        _style(ax, title)
        for (label, free, gated), color in zip(series, SERIES):
            t, y = fn(free, gated)
            keep = (t >= lo) & (t <= hi) & ~np.isnan(y)
            if logy:
                keep &= (y <= ylim[1]) & (y >= ylim[0])
            ax.plot(t[keep], y[keep], color=color, linewidth=2, label=label)
        if logy:
            ax.set_yscale("log")
            ax.yaxis.set_minor_locator(NullLocator())
        ax.set_ylim(*ylim)
        ax.yaxis.set_major_formatter(FuncFormatter(_percent))
        _ticks(ax, lo, hi)
    axes[1].axhline(1.0, color=INK2, linewidth=0.8, linestyle=(0, (3, 3)))
    axes[1].text(lo + 0.03, 1.15, "all of a researcher's time", fontsize=8, color=INK2)
    axes[2].axvline(start, color=INK2, linewidth=0.8, linestyle=(0, (3, 3)))
    axes[0].legend(frameon=False, fontsize=9, labelcolor=INK, loc="lower left")
    fig.tight_layout()
    fig.savefig(OUT / "fig3_deployed_changes_and_gate.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


# --------------------------------------------------------------------------
# Markdown summary
# --------------------------------------------------------------------------
def d(x: float) -> str:
    return pm.fmt_date(x)


def pace(x: float) -> str:
    if x != x:
        return "off scale"
    return f"{x:.1f}x" if x < 100 else f"{x:.0f}x"


def pct(x: float) -> str:
    if x != x:
        return "n/a"
    if x > 1e3:
        return "off scale"
    if x >= 9.995:
        return f"{x:,.0f} researcher-years"
    return f"{x:.0%}" if x >= 0.01 else f"{x:.2%}"


def num(x: float) -> str:
    if x != x:
        return "n/a"
    return "off scale" if x > 1e7 else f"{x:,.0f}"


def markdown(cal, rows_a, sens, rows_b) -> str:
    g = pm.gate_from_calibration(cal)
    out = ["# Generated results", "",
           "Written by `run_all.py`. Do not edit by hand.", "",
           "\"Off scale\" means the run had already ended: pace had passed 300x (Model A) or "
           "progress had passed AIFM's ASI level by an order of magnitude (Model B).", "",
           f"Deployed changes per researcher-year at the reference date: {g.changes_at_reference:g}. "
           f"Hours to understand all of them: {g.hours_at_reference:g}, "
           f"{g.hours_at_reference / g.hours_per_year:.0%} of a researcher-year.", ""]

    def table_a(kind, title):
        out.extend([f"## {title}", "",
                    "| Mechanism | SAR-level capability | Delay | Pace mid-2027 | Pace Jan 2028 "
                    "| Pace Jan 2029 | Pace reaches 10x |",
                    "|---|---|---|---|---|---|---|"])
        for r in rows_a:
            if r["supervision"] != kind:
                continue
            out.append(f"| {r['mechanism']} | {d(r['sar_capability_date'])} | "
                       f"{r['sar_delay_months']:+.0f} mo | {pace(r['pace_mid_2027'])} | "
                       f"{pace(r['pace_jan_2028'])} | {pace(r['pace_jan_2029'])} | "
                       f"{d(r['date_pace_10x'])} |")
        out.append("")

    table_a("anthropic", "Model A, supervision fitted to Anthropic automation levels")
    table_a("openai", "Model A, supervision fitted to OpenAI zero-intervention horizon")
    table_a("openai_runtime", "Model A, supervision fitted to OpenAI agent runtime per human workday")
    table_a("none", "Model A, no supervision requirement (Cotra's model as published)")

    if rows_b:
        def table_b(variant, kind, title):
            out.extend([f"## {title}", "",
                        "| Mechanism | SAR | Delay | TED-AI | ASI | ASI delay | Pace mid-2027 | Pace Jan 2028 "
                        "| Pace reaches 10x |", "|---|---|---|---|---|---|---|---|---|"])
            for r in rows_b:
                if r["variant"] != variant or r["supervision"] != kind:
                    continue
                out.append(f"| {r['mechanism']} | {d(r['sar_date'])} | {r['sar_delay_months']:+.0f} mo | "
                           f"{d(r['ted_ai_date'])} | {d(r['asi_date'])} | {r['asi_delay_months']:+.0f} mo | "
                           f"{pace(r['pace_mid_2027'])} | {pace(r['pace_jan_2028'])} | {d(r['date_pace_10x'])} |")
            out.append("")
        table_b("Nov 10 example", "anthropic",
                "Model B (AI Futures Nov 10 example), supervision fitted to Anthropic automation levels")
        table_b("Nov 10 example", "openai",
                "Model B (AI Futures Nov 10 example), supervision fitted to OpenAI zero-intervention horizon")
        table_b("Nov 10 example", "none", "Model B (AI Futures Nov 10 example), no added supervision requirement")
        table_b("as published Aug 2026", "anthropic", "Model B (AIFM as published, August 2026 medians)")

    out.extend(["## Inside the gate", "",
                "| Model | Mechanism | Date | AI labor used | Deployed changes per researcher-year "
                "| Share of experiments deployed | Researcher time on comprehension | Research effort kept |",
                "|---|---|---|---|---|---|---|---|"])
    pick = [("A", r) for r in rows_a if r["supervision"] == "anthropic"]
    pick += [("B", r) for r in rows_b if r["variant"] == "Nov 10 example" and r["supervision"] == "anthropic"]
    for model, r in pick:
        if r["mechanism"] not in ("No pacing", SIGNOFF, CENTRAL, "Comprehension audits, strict"):
            continue
        for tag, label in (("jul_2027", "Jul 2027"), ("jan_2028", "Jan 2028")):
            comp = r[f"time_on_comprehension_{tag}"]
            comp_text = (pct(comp) + (" if all were understood" if r["mechanism"] == "No pacing" else ""))
            labor = num(r[f"labor_used_{tag}"])
            out.append(f"| {model} | {r['mechanism']} | {label} | {labor + ('x' if labor[0].isdigit() else '')} | "
                       f"{num(r[f'deployed_per_year_{tag}'])} | {pct(r[f'deployed_share_of_experiments_{tag}'])} | "
                       f"{comp_text} | {pct(r[f'effort_kept_{tag}'])} |")
    out.append("")

    out.extend(["## Sensitivity, Model A (one change at a time, central gate)", "",
                "| Case | No pacing: SAR-level capability | No pacing: pace Jan 2028 "
                "| No pacing: full understanding takes all researcher time from | Gate: SAR-level capability "
                "| Gate: pace Jan 2028 | Gate: pace Jan 2029 | Gate: pace reaches 10x | Gate: effort kept Jan 2028 |",
                "|---|---|---|---|---|---|---|---|---|"])
    for r in sens:
        out.append(f"| {r['case']} | {d(r['nopacing_sar'])} | {pace(r['nopacing_pace_jan_2028'])} | "
                   f"{d(r['nopacing_full_understanding_impossible'])} | {d(r['gate_sar'])} | "
                   f"{pace(r['gate_pace_jan_2028'])} | {pace(r['gate_pace_jan_2029'])} | "
                   f"{d(r['gate_date_pace_10x'])} | {pct(r['gate_effort_kept_jan_2028'])} |")
    out.append("")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-aifm", action="store_true")
    ap.add_argument("--aifm-path", default=None)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    cal = pm.load_calibration()

    rows_a, runs_a = run_model_a(cal)
    write_csv(OUT / "model_a_scenarios.csv", rows_a)
    sens = sensitivity_a(cal)
    write_csv(OUT / "model_a_sensitivity.csv", sens)
    log("Model A done")

    rows_b, runs_b = [], {}
    if not args.skip_aifm:
        from aifm_adapter import DEFAULT_AIFM_PATH
        path = Path(args.aifm_path) if args.aifm_path else DEFAULT_AIFM_PATH
        if path.exists():
            rows_b, runs_b = run_model_b(cal, path)
            write_csv(OUT / "model_b_scenarios.csv", rows_b)
        else:
            log(f"AIFM checkout not found at {path}; skipping Model B")

    figures(cal, runs_a, runs_b)
    (OUT / "tables.md").write_text(markdown(cal, rows_a, sens, rows_b))
    log("wrote results/")


if __name__ == "__main__":
    main()
