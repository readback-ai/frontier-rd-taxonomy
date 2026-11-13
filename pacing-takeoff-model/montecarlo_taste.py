"""Probability of a superhuman AI researcher and of TED-AI by date, by pacing scenario,
under four models of how fast AI research judgment ("research taste") improves.

All four start from AI Futures' base case in "Research taste linear
extrapolation" (2026-11-10): AI research taste of -3.5 SD on Sep 25, 2026.

    baseline    +3 SD per year of 2025 progress (AI Futures' base case)
    slow        +1 SD per year of 2025 progress
    split_C_F   research split into supervisable tasks at +C SD and HTS fuzzy tasks at +F SD,
                for C in 3 and 2.1 and F in 1 and 0.5

In the split models the two classes are complements (calibration.yml,
taste_split), so effort shifts to HTS fuzzy work as supervisable work gets cheap.

Every other parameter is drawn with AI Futures' own sampler and August 2026
configuration. A draw is kept if its pace of progress on Nov 1, 2026 is in the
band METR measured. With taste that low on the reference date, AI judgment adds
nothing to the pace by then, so the same draws are kept under every taste model
and the pace has to come from coding.

Each kept trajectory runs under every pacing scenario with the link from
comprehension to human judgment switched on (pacing_model.lab_choice), and
under two scenarios with the link off for comparison.

Usage:
    python montecarlo_taste.py --samples 10000       # several hours on 4 cores
    python montecarlo_taste.py --samples 10000 --only kept --models split_3_1,split_3_0.5
    python montecarlo_taste.py --replot              # rebuild tables and figures from the CSV
    python montecarlo_taste.py --samples 10000 --only kept --models split_3_1,split_3_0.5 \\
        --crisp-share 0.7 --substitution 0.5 --tag share0.7_sub0.5

Writes results/model_b_taste.csv, results/tables_taste.md and figures 5, 6 and 8 to 11. A
tagged run writes results/model_b_taste_<tag>.csv and results/tables_taste_<tag>.md only.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import math
import multiprocessing as mp
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pacing_model as pm
from aifm_adapter import DEFAULT_AIFM_PATH, Aifm
from montecarlo_b import draw_samples

OUT = pm.HERE / "results"
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
UNLINKED = ["No pacing", "Comprehension audits, central"]  # also run with the link off
T_END = 2040.0  # a milestone not reached by then is recorded as later than this
TASTE_AT_AC = "ai_research_taste_at_coding_automation_anchor_sd"
SLOPE = "ai_research_taste_slope"
_STATE = {}


@dataclass(frozen=True)
class TasteModel:
    name: str  # key in the CSV
    crisp: float  # SD per year of 2025 progress. The only slope when `fuzzy` is None
    fuzzy: float | None  # slope of the HTS fuzzy class, or None for a single taste
    years: tuple  # dates for the probability columns
    until: float  # right edge of the figure panel

    @property
    def short(self) -> str:
        return (
            f"{self.crisp:+g} SD"
            if self.fuzzy is None
            else f"Supervisable {self.crisp:+g}, HTS fuzzy {self.fuzzy:+g} SD"
        )

    @property
    def panel(self) -> str:
        return (
            f"taste {self.crisp:+g} SD a year"
            if self.fuzzy is None
            else f"supervisable {self.crisp:+g} SD, HTS fuzzy {self.fuzzy:+g} SD a year"
        )

    @property
    def heading(self) -> str:
        return (
            f"Taste improves {self.crisp:+g} SD per year of 2025 progress"
            if self.fuzzy is None
            else f"Supervisable tasks improve {self.crisp:+g} SD and HTS fuzzy tasks "
            f"{self.fuzzy:+g} SD per year of 2025 progress"
        )


def taste_models(cal: dict) -> list[TasteModel]:
    t, sp = cal["taste_models"], cal["taste_split"]
    out = [
        TasteModel("baseline", float(t["slope_baseline"]), None, (2028.0, 2029.0, 2030.0), 2031.0),
        TasteModel("slow", float(t["slope_slow"]), None, (2029.0, 2031.0, 2035.0), T_END),
    ]
    for crisp in sp["crisp_slopes"]:
        for fuzzy in sp["fuzzy_slopes"]:
            out.append(
                TasteModel(
                    f"split_{crisp:g}_{fuzzy:g}",
                    float(crisp),
                    float(fuzzy),
                    (2029.0, 2031.0, 2035.0),
                    T_END,
                )
            )
    return out


def build(
    params: dict,
    first: Aifm,
    model: TasteModel,
    cal: dict,
    aifm_path: Path,
    share: float | None = None,
    substitution: float | None = None,
    crisp_level: float | None = None,
) -> Aifm:
    """The model under `model`. `first` is the same draw run with negligible taste."""
    t, sp, t_ref = cal["taste_models"], cal["taste_split"], cal["reference_date"]
    m = pinned(params, first, model.crisp, t["level_sd"], t["date"], aifm_path, t_ref)
    if model.fuzzy is not None:
        # The supervisable class keeps the schedule AIFM holds for the single taste. The HTS
        # fuzzy class passes through the same level on the date and climbs at fuzzy / crisp of
        # the rate. Field and key names keep the earlier labels: crisp is the supervisable
        # class and fuzzy is the HTS fuzzy class.
        at = m.capability_at(t["date"])
        level, slope = m.taste_sd(at), m.params.ai_research_taste_slope
        share = sp["crisp_share"] if share is None else share
        m.set_taste_classes(
            [
                dict(
                    share=share,
                    slope=slope,
                    at=at,
                    level=level if crisp_level is None else crisp_level,
                ),
                dict(
                    share=1.0 - share, slope=slope * model.fuzzy / model.crisp, at=at, level=level
                ),
            ],
            sp["substitution"] if substitution is None else substitution,
        )
    return m


def pinned(
    params: dict,
    first: Aifm,
    slope_per_2025_year: float,
    level_sd: float,
    date: float,
    aifm_path: Path,
    t_ref: float,
) -> Aifm:
    """The model with AI research taste at `level_sd` on `date`, improving by
    `slope_per_2025_year` SD per year of progress at the 2024 to mid-2025 rate.

    `first` is the same draw run with negligible taste. It supplies the progress
    on `date`, the progress at the automated coder anchor and the 2025 rate.
    """
    slope = slope_per_2025_year / first.rate0  # SD per unit of progress
    if params.get("taste_schedule_type", "SDs per progress-year") == "SDs per progress-year":
        # AIFM divides the input by the progress rate at its anchor date. Undo that.
        slope_input = slope * params[SLOPE] / first.params.ai_research_taste_slope
    else:
        slope_input = slope
    at_ac = level_sd + slope * (first.params.progress_at_aa - first.capability_at(date))
    return Aifm(
        dict(params, **{SLOPE: slope_input, TASTE_AT_AC: at_ac}), aifm_path, t_ref, horizon=2030.0
    )


def _init(aifm_path, band, supervision, models, split=None, residue=False):
    import warnings

    warnings.filterwarnings("ignore")  # AIFM overflows harmlessly on extreme draws
    np.seterr(all="ignore")
    logging.disable(logging.WARNING)
    cal = pm.load_calibration()
    _STATE.update(
        path=aifm_path,
        band=band,
        supervision=supervision,
        residue=residue,
        cal=cal,
        models=[m for m in taste_models(cal) if m.name in models],
        split=dict(split or {}),
        policies={p.name: p for p in pm.standard_policies(cal)},
    )


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
        for model in _STATE["models"]:
            m = build(params, first, model, cal, _STATE["path"], **_STATE["split"])
            common = dict(
                sample=index,
                pace_nov_2026=m.base_pace(t_ref),
                taste_model=model.name,
                taste_sd_on_date=m.taste_sd(m.capability_at(spec["date"])),
                slope_per_2025_year=m.params.ai_research_taste_slope * m.rate0,
                ac_date=m.milestones.get("AC", (float("nan"),))[0],
            )
            m.fit_supervision(_STATE["supervision"], cal)
            for link, names in ((True, SCENARIOS), (False, UNLINKED)):
                m.use_calibration(cal, link=link, residue=_STATE["residue"])
                for scenario in names:
                    run = m.simulate(
                        _STATE["policies"][scenario], t_end=T_END, step=0.006, stop_at="TED-AI"
                    )
                    s = m.summarize(run)
                    rows.append(
                        dict(
                            common,
                            link=int(link),
                            scenario=scenario,
                            sar=s.get("t_sar", float("nan")),
                            ted_ai=s.get("t_ted_ai", float("nan")),
                        )
                    )
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
    return {
        r["sample"]: r
        for r in rows
        if r["taste_model"] == model and r["link"] == link and r["scenario"] == scenario
    }


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


def _in_sentence(key: str, label: str) -> str:
    """A milestone label as it reads mid-sentence. TED-AI keeps its capitals."""
    return label[0].lower() + label[1:] if key == "sar" else label


def _subset(by_sample: dict, keys) -> dict:
    return {k: by_sample[k] for k in keys}


def real_research_note(meta: dict) -> str:
    """What a run changed to follow the labs' own usage data (calibration.yml, real_research)."""
    out = ""
    if meta.get("supervision") == "gdm":
        out += (
            " The supervision schedule is fitted to Google DeepMind's share of fully delegated "
            "pull requests."
        )
    if meta.get("residue"):
        out += (
            f" {meta['residue']:.0%} of work needs a person on Nov 1, 2026, and that share falls "
            "with the share of researchers whose judgment is still better than the AI's."
            + (
                f" A person spends {meta['residue_supervision_time']:.1%} of that work's time "
                "supervising it."
                if "residue_supervision_time" in meta
                else ""
            )
        )
    return out


def markdown(rows, meta) -> str:
    cal = pm.load_calibration()
    spec, sp = cal["taste_models"], cal["taste_split"]
    present = {r["taste_model"] for r in rows}
    models = [m for m in taste_models(cal) if m.name in present]
    out = [
        "# Probability of each milestone by date, by taste model and pacing scenario",
        "",
        "Written by `montecarlo_taste.py`. Do not edit by hand.",
        "",
        f"{meta['kept']} of {meta['drawn']} sampled trajectories "
        f"({meta['kept'] / meta['drawn']:.1%}) had a pace "
        f"of {meta['band'][0]:g}x to {meta['band'][1]:g}x on Nov 1, 2026 with AI research taste "
        "too low to "
        "contribute, and are kept. Parameters other than taste are drawn from AI Futures' August "
        "2026 "
        f"distribution for {meta['forecaster'].title()}, seed {meta['seed']}. "
        f"Median pace of the kept trajectories: {meta['median_pace']:.2f}x. "
        f"Every taste model puts AI research taste at {spec['level_sd']:+g} SD on "
        f"{pm.fmt_date(spec['date'])}, "
        "in both classes of task where there are two. In the split models supervisable tasks take "
        f"{meta.get('crisp_share', sp['crisp_share']):.0%} of research effort while judgment is "
        "equal across the classes, and the "
        "elasticity of substitution between the classes is "
        f"{meta.get('substitution', sp['substitution']):g}. "
        "Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against "
        "the same "
        f"trajectory with no pacing. A milestone not reached by the end of {T_END - 1:.0f} counts "
        "as later "
        "than that. The link from comprehension to human judgment is on except where a table says "
        "otherwise." + real_research_note(meta),
        "",
    ]
    milestones = (("sar", "Superhuman AI researcher"), ("ted_ai", "TED-AI"))
    out += ["## Summary", ""]
    groups = [
        ("one taste", [m for m in models if m.fuzzy is None]),
        ("supervisable and HTS fuzzy tasks", [m for m in models if m.fuzzy is not None]),
    ]
    for key, label in milestones:
        for group, members in groups:
            if not members:
                continue
            out += [
                f"### {label}, {group}: median date and median delay",
                "",
                "| Scenario | "
                + " | ".join(f"{m.short}: median date | {m.short}: median delay" for m in members)
                + " |",
                "|---|" + "---|" * (2 * len(members)),
            ]
            for name in SCENARIOS:
                cells = []
                for m in members:
                    base = select(rows, m.name, 1, "No pacing")
                    got = select(rows, m.name, 1, name)
                    cells.append(date_text(quantile([r[key] for r in got.values()], 0.5)))
                    cells.append(
                        ""
                        if name == "No pacing"
                        else delay_text(quantile(delays(got, base, key), 0.5))
                    )
                out.append(f"| {name} | " + " | ".join(cells) + " |")
            out.append("")
    for model in models:
        base = select(rows, model.name, 1, "No pacing")
        out += [f"## {model.heading} ({model.name})", ""]
        for key, label in milestones:
            ys = model.years
            out += [
                f"### {label}",
                "",
                "| Scenario | Median date | Middle half of trajectories | "
                + " | ".join(f"By start of {y:.0f}" for y in ys)
                + " | Median delay | Delay, upper quartile |",
                "|---|---|---|" + "---|" * len(ys) + "---|---|",
            ]
            for name in SCENARIOS:
                got = select(rows, model.name, 1, name)
                v = [r[key] for r in got.values()]
                d = delays(got, base, key)
                first = name == "No pacing"
                out.append(
                    f"| {name} | {date_text(quantile(v, 0.5))} | {date_text(quantile(v, 0.25))} to "
                    f"{date_text(quantile(v, 0.75))} | "
                    + " | ".join(f"{by_date(v, y):.0%}" for y in ys)
                    + " | "
                    + ("" if first else delay_text(quantile(d, 0.5)))
                    + " | "
                    + ("" if first else delay_text(quantile(d, 0.75)))
                    + " |"
                )
            out.append("")
        # What the link changes
        off = select(rows, model.name, 0, "No pacing")
        audit_on = select(rows, model.name, 1, "Comprehension audits, central")
        audit_off = select(rows, model.name, 0, "Comprehension audits, central")
        out += [
            "### What the link from comprehension to judgment changes",
            "",
            "| | Link off | Link on |",
            "|---|---|---|",
        ]
        for key, label in milestones:
            out.append(
                f"| No pacing: median date of {_in_sentence(key, label)} | "
                f"{date_text(quantile([r[key] for r in off.values()], 0.5))} | "
                f"{date_text(quantile([r[key] for r in base.values()], 0.5))} |"
            )
        for key, label in milestones:
            out.append(
                f"| Central audits: median delay to {_in_sentence(key, label)} | "
                f"{delay_text(quantile(delays(audit_off, off, key), 0.5))} | "
                f"{delay_text(quantile(delays(audit_on, base, key), 0.5))} |"
            )
        shift = {key: [base[k][key] - off[k][key] for k in base] for key, _ in milestones}
        out += [
            "",
            "Paired across trajectories, the link moves the no-pacing date of the superhuman AI "
            "researcher "
            f"by a median of {_days(shift['sar'])} and TED-AI by {_days(shift['ted_ai'])}.",
            "",
        ]
        # Split by whether coding was already automated on the reference date
        early = {k for k, r in base.items() if r["ac_date"] <= cal["reference_date"]}
        out += [
            "### Split by when coding is fully automated",
            "",
            "| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No "
            "pacing: median "
            "TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: "
            "median delay "
            "to TED-AI | 3-month lag: median delay to TED-AI |",
            "|---|---|---|---|---|---|---|",
        ]
        lag3 = select(rows, model.name, 1, "Internal-use lag, 3 months")
        for label, keys in (
            ("Before Nov 1, 2026", early),
            ("Nov 1, 2026 or later", set(base) - early),
        ):
            if not keys:
                continue
            out.append(
                f"| {label} | {len(keys)} | "
                f"{date_text(quantile([base[k]['sar'] for k in keys], 0.5))} | "
                f"{date_text(quantile([base[k]['ted_ai'] for k in keys], 0.5))} | "
                f"{delay_text(quantile(delays(_subset(audit_on, keys), base, 'sar'), 0.5))} | "
                f"{delay_text(quantile(delays(_subset(audit_on, keys), base, 'ted_ai'), 0.5))} | "
                f"{delay_text(quantile(delays(_subset(lag3, keys), base, 'ted_ai'), 0.5))} |"
            )
        out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SHORT = {
    "Human sign-off, no comprehension standard": "Human sign-off only",
    "Comprehension audits, light": "Audits, light",
    "Comprehension audits, central": "Audits, central",
    "Comprehension audits, strict": "Audits, strict",
    "Internal-use lag, 3 months": "3-month internal-use lag",
    "Internal-use lag, 9 months": "9-month internal-use lag",
    "Comprehension audits (central) + 3-month lag": "Central audits + 3-month lag",
    "Comprehension audits (central) + 9-month lag": "Central audits + 9-month lag",
}
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


def figure(rows, meta, styles: dict, path: Path, title: str, models: list[TasteModel]) -> None:
    """One row of panels per taste model: superhuman AI researcher left, TED-AI right."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    cal = pm.load_calibration()
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, axes = plt.subplots(
        len(models), 2, figsize=(11.5, 0.6 + 3.8 * len(models)), facecolor=SURFACE, squeeze=False
    )
    for i, model in enumerate(models):
        lo, hi = 2027.0, model.until
        for j, (key, label) in enumerate(
            (("sar", "Superhuman AI researcher"), ("ted_ai", "TED-AI"))
        ):
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
                got = select(rows, model.name, 1, name)
                x, y = _curve([r[key] for r in got.values()], lo, hi)
                ax.step(
                    x,
                    y,
                    where="post",
                    color=color,
                    linestyle=dash,
                    linewidth=2.0,
                    zorder=3 if name == "No pacing" else 2,
                )
            ax.set_xlim(lo, hi)
            ax.set_ylim(-0.02, 1.03)
            years = np.arange(int(lo), int(hi) + 1, 1 if hi - lo <= 6 else 2)
            ax.set_xticks(years)
            ax.set_xticklabels([str(int(y)) for y in years])
            ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
            ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"] if j == 0 else [""] * 5)
            ax.set_title(f"{label}, {model.panel}", loc="left", fontsize=10.5, color=INK, pad=8)
    handles = [Line2D([0], [0], color=c, linestyle=d, linewidth=2.2) for c, d in styles.values()]
    fig.legend(
        handles,
        [SHORT.get(n, n) for n in styles],
        loc="lower center",
        ncol=len(styles) if len(styles) <= 5 else 4,
        frameon=False,
        fontsize=9.5,
        labelcolor=INK,
        handlelength=3.2,
        columnspacing=2.2,
    )
    fig.suptitle(title, x=0.045, y=0.985, ha="left", fontsize=13, color=INK)
    ends = ", ".join(
        f"{word} row ends {m.until:.0f}" for word, m in zip(("top", "bottom"), models, strict=False)
    )
    split = any(m.fuzzy is not None for m in models)
    classes = (
        " Supervisable tasks take "
        f"{meta.get('crisp_share', cal['taste_split']['crisp_share']):.0%} of research effort "
        "at first, and supervisable and HTS fuzzy work are complements."
        if split
        else ""
    )
    fig.text(
        0.045,
        0.94,
        f"Share of {meta['kept']} sampled AI Futures Model trajectories that have reached each "
        f"milestone by the date shown. Pace {meta['band'][0]:g}x to {meta['band'][1]:g}x on "
        "Nov 1, 2026.\n"
        f"AI research taste {cal['taste_models']['level_sd']:+g} SD in Sep 2026, improving per "
        "year of 2025 progress as each panel says.\n"
        f"Pacing starts Jan 1, 2027. {ends[0].upper() + ends[1:]}.{classes}",
        fontsize=9,
        color=INK2,
        va="top",
    )
    fig.tight_layout(rect=(0.02, 0.085 if len(styles) > 5 else 0.055, 1.0, 0.895), h_pad=2.0)
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def report(rows, meta, tag: str = "") -> None:
    """Write the tables, and for an untagged run the figures."""
    (OUT / f"tables_taste{tag}.md").write_text(markdown(rows, meta))
    if tag:
        return
    present = {r["taste_model"] for r in rows}
    models = [m for m in taste_models(pm.load_calibration()) if m.name in present]
    gates = "Probability of each milestone by date: sign-off and comprehension audits"
    other = "Probability of each milestone by date: lags, compute cuts and combinations"
    single = [m for m in models if m.fuzzy is None]
    if single:
        figure(rows, meta, STYLE_GATES, OUT / "fig5_probability_by_date_gates.png", gates, single)
        figure(rows, meta, STYLE_OTHER, OUT / "fig6_probability_by_date_other.png", other, single)
    # One pair of figures per rate on supervisable tasks: figures 8 and 9, then 10 and 11.
    crisp_rates = sorted({m.crisp for m in models if m.fuzzy is not None}, reverse=True)
    for number, crisp in zip((8, 10), crisp_rates, strict=False):
        members = [m for m in models if m.fuzzy is not None and m.crisp == crisp]
        suffix = "" if number == 8 else f"_crisp_{crisp:g}"
        for offset, (styles, kind, title) in enumerate(
            ((STYLE_GATES, "gates", gates), (STYLE_OTHER, "other", other))
        ):
            figure(
                rows,
                meta,
                styles,
                OUT / f"fig{number + offset}_probability_by_date_{kind}_split{suffix}.png",
                title + ", supervisable and HTS fuzzy tasks",
                members,
            )


FLOATS = ("pace_nov_2026", "taste_sd_on_date", "slope_per_2025_year", "ac_date", "sar", "ted_ai")


def read_rows(path: Path) -> list[dict]:
    with open(path) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["sample"], r["link"] = int(r["sample"]), int(r["link"])
        for k in FLOATS:
            r[k] = float(r[k])
    return rows


def checkpoint(path: Path, rows: list[dict]) -> None:
    """Append finished trajectories, so a run that is cut short can pick up where it stopped."""
    new = not path.exists()
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new:
            w.writeheader()
        w.writerows(rows)


def load(tag: str = "") -> tuple[list[dict], dict]:
    rows = read_rows(OUT / f"model_b_taste{tag}.csv")
    with open(OUT / f"model_b_taste{tag}_meta.json") as f:
        meta = json.load(f)
    meta["band"] = tuple(meta["band"])
    return rows, meta


def save(rows, meta, tag: str = "") -> None:
    with open(OUT / f"model_b_taste{tag}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    with open(OUT / f"model_b_taste{tag}_meta.json", "w") as f:
        json.dump(meta, f, indent=1)
    report(rows, meta, tag)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=8000)
    ap.add_argument("--forecaster", choices=("daniel", "eli"), default="daniel")
    ap.add_argument("--seed", type=int, default=20261110)
    ap.add_argument("--pace-low", type=float, default=1.5)
    ap.add_argument("--pace-high", type=float, default=2.0)
    ap.add_argument(
        "--supervision", default="anthropic", help="'anthropic' or 'gdm' (calibration.yml)"
    )
    ap.add_argument(
        "--residue",
        action="store_true",
        help="a share of work needs a person and falls as AI judgment rises (real_research)",
    )
    ap.add_argument("--aifm-path", default=str(DEFAULT_AIFM_PATH))
    ap.add_argument("--workers", type=int, default=mp.cpu_count())
    ap.add_argument(
        "--models",
        default="",
        help="comma-separated taste models to run; default is all. With "
        "--only kept, results for the other models are kept from the CSV",
    )
    ap.add_argument(
        "--only",
        default="",
        help="'kept' reruns just the trajectories in the existing CSV, skipping the pace filter "
        "over all draws. Same results as a full run, in less time",
    )
    ap.add_argument("--crisp-share", type=float, help="override taste_split.crisp_share")
    ap.add_argument("--substitution", type=float, help="override taste_split.substitution")
    ap.add_argument("--tag", default="", help="suffix for output files; needed with an override")
    ap.add_argument("--replot", action="store_true", help="rebuild tables and figures from the CSV")
    ap.add_argument(
        "--checkpoint",
        type=Path,
        help="CSV to append finished trajectories to. A rerun skips the trajectories in it",
    )
    args = ap.parse_args()
    tag = f"_{args.tag}" if args.tag else ""
    if args.replot:
        report(*load(tag), tag)
        return
    split = {}
    if args.crisp_share is not None:
        split["share"] = args.crisp_share
    if args.substitution is not None:
        split["substitution"] = args.substitution
    changed = split or args.residue or args.supervision != "anthropic"
    if changed and not tag:
        ap.error("an override of the inputs needs --tag, so the main results stay intact")
    path, band = Path(args.aifm_path), (args.pace_low, args.pace_high)
    OUT.mkdir(exist_ok=True)
    t0 = time.time()
    samples = draw_samples(path, args.forecaster, args.samples, args.seed)
    print(f"[{time.time() - t0:5.0f}s] drew {len(samples)} parameter sets", flush=True)
    every = [m.name for m in taste_models(pm.load_calibration())]
    models = [x.strip() for x in args.models.split(",") if x.strip()] or every
    jobs, drawn, carried = list(enumerate(samples)), None, []
    if args.only == "kept":
        old_rows, old_meta = load()
        wanted, drawn = {r["sample"] for r in old_rows}, old_meta["drawn"]
        jobs = [j for j in jobs if j[0] in wanted]
        # A tagged run holds only the models it ran. The main file keeps the others.
        carried = (
            [] if tag else [r for r in old_rows if r["taste_model"] in set(every) - set(models)]
        )
    rows, paces = [], []
    per = len(models) * (len(SCENARIOS) + len(UNLINKED))
    if args.checkpoint and args.checkpoint.exists():
        earlier = read_rows(args.checkpoint)
        count = {}
        for r in earlier:
            count[r["sample"]] = count.get(r["sample"], 0) + 1
        whole = {k for k, n in count.items() if n == per}
        rows = [r for r in earlier if r["sample"] in whole]
        jobs = [j for j in jobs if j[0] not in whole]
        print(
            f"[{time.time() - t0:5.0f}s] {len(whole)} trajectories from the checkpoint", flush=True
        )
    with mp.Pool(
        args.workers,
        initializer=_init,
        initargs=(path, band, args.supervision, models, split, args.residue),
    ) as pool:
        for done, (_index, pace, got) in enumerate(
            pool.imap_unordered(_work, jobs, chunksize=2), 1
        ):
            paces.append(pace)
            rows.extend(got)
            if args.checkpoint and got:
                checkpoint(args.checkpoint, got)
            if done % (10 if drawn else 200) == 0 or done == len(jobs):
                print(f"[{time.time() - t0:5.0f}s] {done} run, {len(rows) // per} kept", flush=True)
    rows += carried
    order = {name: i for i, name in enumerate(SCENARIOS)}
    rows.sort(
        key=lambda r: (r["sample"], every.index(r["taste_model"]), -r["link"], order[r["scenario"]])
    )
    valid = [p for p in paces if p == p]
    kept = sorted({r["sample"] for r in rows})
    kept_pace = [
        r["pace_nov_2026"]
        for r in rows
        if r["taste_model"] == rows[0]["taste_model"]
        and r["link"] == 1
        and r["scenario"] == "No pacing"
    ]
    meta = dict(
        drawn=drawn or len(valid),
        kept=len(kept),
        band=band,
        forecaster=args.forecaster,
        seed=args.seed,
        median_pace=float(np.median(kept_pace)) if kept_pace else float("nan"),
    )
    if args.supervision != "anthropic":
        meta["supervision"] = args.supervision
    if args.residue:
        rr = pm.load_calibration()["real_research"]
        meta["residue"] = rr["residue_today"]
        meta["residue_supervision_time"] = rr["residue_supervision_time"]
    if "share" in split:
        meta["crisp_share"] = split["share"]
    if "substitution" in split:
        meta["substitution"] = split["substitution"]
    save(rows, meta, tag)
    print(f"[{time.time() - t0:5.0f}s] done", flush=True)


if __name__ == "__main__":
    main()
