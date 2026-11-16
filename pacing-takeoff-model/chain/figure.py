"""Draw the pace of progress in the primary scenario under each pacing policy.

Writes results/pace.png. Needs matplotlib as well as numpy.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from chain_model import (
    CASES,
    MONTHS,
    PACE_MAY,
    PACE_REF,
    POLICIES,
    PRIMARY,
    T_MAY,
    T_REF,
    Params,
    fmt_date,
    simulate,
)
from matplotlib.ticker import FixedLocator, NullFormatter

SURFACE, INK, SECONDARY, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
# Policy, legend name and line color. No pacing is the reference and takes the ink. The four
# policies take the first four slots of a palette checked for color-blind separation.
SERIES = (
    ("No pacing", "No pacing", INK),
    ("Comprehension audits, central", "Comprehension audits, central", "#2a78d6"),
    ("Comprehension audits, strict", "Comprehension audits, strict", "#eb6834"),
    ("Internal-use lag, 9 months", "Internal-use lag, 9 months", "#1baf7a"),
    ("R&D compute at a third of baseline", "Compute at a third of baseline", "#eda100"),
)
START, TICKS = 2026.0, (1.0, 1.5, 2.0, 3.0, 5.0, 10.0)
OUT = Path(__file__).parent / "results" / "pace.png"


def main() -> None:
    p = replace(Params(), **dict(CASES)[PRIMARY])
    by_name = {policy.name: policy for policy in POLICIES}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(10.0, 5.6), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ends = []
    for name, label, color in SERIES:
        run = simulate(p, by_name[name])
        shown = run["t"] >= START
        ax.plot(
            run["t"][shown],
            run["pace"][shown],
            color=color,
            lw=2.0,
            label=label,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=3 if name == "No pacing" else 2,
        )
        ends.append((float(run["t"][-1]), float(run["pace"][-1]), color, run["dates"]["ted_ai"]))
    # End labels sit to the right of each end, except where two ends are close together.
    places = {
        0: dict(xytext=(-8, 0), ha="right", va="center"),
        1: dict(xytext=(0, 9), ha="center", va="bottom"),
    }
    for k, (when, pace, color, ted) in enumerate(ends):
        ax.plot(
            [when], [pace], "o", ms=8, color=color, mec=SURFACE, mew=2.0, zorder=4, clip_on=False
        )
        place = places.get(k, dict(xytext=(8, 0), ha="left", va="center"))
        ax.annotate(
            fmt_date(ted),
            (when, pace),
            textcoords="offset points",
            color=SECONDARY,
            fontsize=9,
            **place,
        )
    # The two measured paces the model is fitted to.
    ax.plot(
        [T_MAY, T_REF], [PACE_MAY, PACE_REF], "o", ms=5, mfc=SURFACE, mec=INK, mew=1.2, zorder=5
    )
    ax.annotate(
        "measured",
        (T_REF, PACE_REF),
        xytext=(-6, 8),
        textcoords="offset points",
        ha="right",
        color=MUTED,
        fontsize=9,
    )
    ax.axvline(2027.0, color=AXIS, lw=1.0, zorder=1)
    ax.annotate(
        "pacing starts",
        (2027.0, TICKS[-1]),
        xytext=(5, -2),
        textcoords="offset points",
        va="top",
        color=MUTED,
        fontsize=9,
    )
    ax.set_yscale("log")
    ax.set_ylim(0.9, 11.5)
    ax.yaxis.set_major_locator(FixedLocator(TICKS))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_yticklabels([f"{tick:g}x" for tick in TICKS])
    last = max(when for when, *_ in ends)
    ax.set_xlim(START, last + 0.45)
    years = range(int(START), int(last) + 2)
    ax.set_xticks([float(year) for year in years if year <= last + 0.45])
    ax.set_xticklabels([f"{MONTHS[0]} {year}" for year in years if year <= last + 0.45])
    ax.grid(axis="y", which="major", color=GRID, lw=0.8)
    ax.grid(axis="y", which="minor", visible=False)
    ax.tick_params(axis="both", which="both", length=0, colors=MUTED, labelsize=9)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.set_ylabel("Pace: years of progress per calendar year", color=SECONDARY, fontsize=9)
    fig.suptitle(
        "Pace of AI progress under four pacing policies",
        x=0.065,
        y=0.965,
        ha="left",
        color=INK,
        fontsize=14,
        fontweight="bold",
    )
    fig.text(
        0.065,
        0.895,
        "Primary scenario: AI ideas and transfer judgment improve 3 SD a year, metric judgment "
        "0.5 SD.\nEach line ends when TED-AI arrives, at the date shown.",
        ha="left",
        va="top",
        color=SECONDARY,
        fontsize=9.5,
        linespacing=1.4,
    )
    legend = ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.0, 0.80),
        frameon=False,
        fontsize=9,
        labelcolor=SECONDARY,
        handlelength=1.6,
        borderaxespad=0.6,
    )
    for line in legend.get_lines():
        line.set_linewidth(2.0)
    fig.subplots_adjust(left=0.065, right=0.955, top=0.80, bottom=0.085)
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, facecolor=SURFACE)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
